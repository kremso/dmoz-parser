"""
USAGE: %(program)s origin_data_path data_destination

Load and explore the data.

Example:
    python parser.py ./data/content.rdf.u8 ./data/parsed.json
"""

from __future__ import division
from xml.sax import make_parser, handler
import os
import sys
import logging

from smart_open import smart_open

from handlers import JSONWriter, CSVWriter

logger = logging.getLogger(__name__)


class DmozHandler(handler.ContentHandler):

    def __init__(self, handler):
        self._handler = handler
        self._current_page = ''
        self._current_topic = ''
        self._capture_content = False
        self._current_content = {}
        self._capture_content_type = ''

    def startElement(self, name, attrs):
        if name == 'ExternalPage':
            # starting an external page entry. Set scene for capturing content
            self._current_page = attrs['about']
            self._current_content = {}
        elif name in ['d:Title', 'd:Description', 'priority', 'topic']:
            self._capture_content_type = name
            self._current_content[self._capture_content_type] = ''
            self._capture_content = True
        elif name == 'Topic':
            self._current_topic = attrs['r:id']
            # Example of such a Topic entry:
            #     < Topic r:id = "Top/Arts/Movies/Titles/1/10_Rillington_Place" >
            #       < catid > 205108 < /catid >
            #       < link r:resource = "http://us.imdb.com/Title?0066730" / >
            #       < link r:resource = "http://www.britishhorrorfilms.co.uk/rillington.shtml" / >
            #       < link r:resource = "http://www.shoestring.org/mmi_revs/10-rillington-place.html" / >
            #       < link r:resource = "http://www.tvguide.com/movies/database/ShowMovie.asp?MI=22983" / >
            #      < /Topic >

    def endElement(self, name):
        #if ending one of the supported blocks, end content capturing
        if name in ['d:Title', 'd:Description', 'priority', 'topic']:
            self._capture_content = False
        # if ending an ExternalPage, write the current entry in our content handler
        if name == 'ExternalPage':
            # first, check if we read a topic in the current ExternalPage entry.
            # older DMOZ dumps do not have this, so we will use the last Topic read
            if not 'topic' in self._current_content.keys():
                self._current_content['topic'] = self._current_topic
            # now save
            self._handler.page(self._current_page, self._current_content)

    def characters(self, content):
        if self._capture_content:
            # this bit of dark magic is to address content coming in two separate waves
            self._current_content[self._capture_content_type] = ''.join([self._current_content[self._capture_content_type], content.strip()])
            # An example for an ExternalPage entry. Note that <topic> might be missing in older dumps
            #   <ExternalPage about="http://www.awn.com/">
            #     <d:Title>Animation World Network</d:Title>
            #     <d:Description>Provides information resources to the international animation community. Features include searchable database archives, monthly magazine, web animation guide, the Animation Village, discussion forums and other useful resources.</d:Description>
            #     <priority>1</priority>
            #     <topic>Top/Arts/Animation</topic>
            #   </ExternalPage>

    def endDocument(self):
        self._handler.finish()


class DmozParser:
    def __init__(self, input_path='content.rdf.u8'):
        self._parser = make_parser()
        self.input_path = input_path

    def run(self):
        self._parser.setContentHandler(DmozHandler(self._handler))
        self._parser.parse(smart_open(self.input_path))

    def add_handler(self, handler):
        self._handler = handler


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(module)s:%(funcName)s:%(lineno)d : %(message)s',
        level=logging.INFO)
    logger.info("running %s", " ".join(sys.argv))

    # check and process cmdline input
    program = os.path.basename(sys.argv[0])

    if len(sys.argv) < 3:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    parser = DmozParser(input_path)

    foo, file_extension = os.path.splitext(output_path)
    # in case we ask directly for a zipped file
    if file_extension in [".bz2", ".gz"]:
        _, file_extension = os.path.splitext(foo)

    if file_extension == ".json":
        parser.add_handler(JSONWriter(output_path))
    elif file_extension == ".csv":
        parser.add_handler(CSVWriter(output_path))
    else:
        logger.info("Only .json or .csv output files are supported.")
        sys.exit(1)
    parser.run()

    logger.info("finished running %s", program)
