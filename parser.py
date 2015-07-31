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
        self._capture_content = False
        self._current_content = {}
        self._expect_end = False

    def startElement(self, name, attrs):
        if name == 'ExternalPage':
            self._current_page = attrs['about']
            self._current_content = {}
        elif name in ['d:Title', 'd:Description', 'priority', 'topic']:
            self._capture_content = True
            self._capture_content_type = name

    def endElement(self, name):
        # Make sure that the only thing after "topic" is "/ExternalPage"
        if self._expect_end:
            assert name == 'topic' or name == 'ExternalPage'
            if name == 'ExternalPage':
                self._expect_end = False

    def characters(self, content):
        if self._capture_content:
            assert not self._expect_end
            self._current_content[self._capture_content_type] = content
            # print self._capture_content_type, self._current_content[self._capture_content_type]
            if self._capture_content_type == "topic":
                # This makes the assumption that "topic" is the last entity in each dmoz page:
                #   <ExternalPage about="http://www.awn.com/">
                #     <d:Title>Animation World Network</d:Title>
                #     <d:Description>Provides information resources to the international animation community. Features include searchable database archives, monthly magazine, web animation guide, the Animation Village, discussion forums and other useful resources.</d:Description>
                #     <priority>1</priority>
                #     <topic>Top/Arts/Animation</topic>
                #   </ExternalPage>
                    self._handler.page(self._current_page, self._current_content)
                    self._expect_end = True
            self._capture_content = False

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

    _, file_extension = os.path.splitext(output_path)

    if file_extension == ".json":
        parser.add_handler(JSONWriter(output_path))
    elif file_extension == ".csv":
        parser.add_handler(CSVWriter(output_path))
    else:
        logger.info("Currently are only supported output files with extension .json or .csv")
        sys.exit(1)
    parser.run()

    logger.info("finished running %s", program)
