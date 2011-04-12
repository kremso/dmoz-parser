from __future__ import division
from xml.sax import make_parser, handler
import os
import codecs

class FileWrapper(file):
  def __init__(self, name):
    self._name = name
    self._bytes = os.path.getsize(name)
    self._bytes_read = 0

    file.__init__(self, name)

  def read(self, size):
    print '\x1B[2F'
    print '\x1B[2K'
    print 'processed %d%%' % self.progress(),
    self._bytes_read += size

    return file.read(self, size)

  def progress(self):
    return (self._bytes_read / self._bytes) * 100

class DmozHandler(handler.ContentHandler):

  def __init__(self, handler):
    self._handler = handler
    self._current_page = ''
    self._capture_content = False
    self._current_content = {}

  def startElement(self, name, attrs):
    if name == 'ExternalPage':
      self._current_page = attrs['about']
    elif name in ['d:Title', 'd:Description', 'priority', 'topic']:
      self._capture_content = True
      self._capture_content_type = name

  def characters(self, content):
    if self._capture_content:
      self._current_content[self._capture_content_type] = content.encode('utf-8')
#      print self._capture_content_type, self._current_content[self._capture_content_type]
      if self._capture_content_type == "topic":
        # This makes the assumption that "topic" is the last entity in each dmoz page:
        #   <ExternalPage about="http://www.awn.com/">
        #     <d:Title>Animation World Network</d:Title>
        #     <d:Description>Provides information resources to the international animation community. Features include searchable database archives, monthly magazine, web animation guide, the Animation Village, discussion forums and other useful resources.</d:Description>
        #     <priority>1</priority>
        #     <topic>Top/Arts/Animation</topic>
        #   </ExternalPage>
          self._handler.page(self._current_page.encode('utf-8'), self._current_content)
      self._capture_content = False

  def endDocument(self):
    self._handler.finish()

class DmozParser:
  def __init__(self):
    self._parser = make_parser()

  def run(self):
    self._parser.setContentHandler(DmozHandler(self._handler))
    self._parser.parse(FileWrapper('content.rdf.u8'))

  def add_handler(self, handler):
    self._handler = handler

