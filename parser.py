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

  def startElement(self, name, attrs):
    if name == 'ExternalPage':
      self._current_page = attrs['about']
    elif name == 'topic':
      self._capture_content = True

  def characters(self, content):
    if self._capture_content:
      self._handler.page(self._current_page.encode('utf-8'), content.encode('utf-8'))
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

class CSVWriter:
  def __init__(self, name):
    self._file = open(name, 'w')

  def page(self, page, topic):
    #print '%(page)s: %(topic)s' % {'page': page, 'topic': topic}
    self._file.write('%(page)s; %(topic)s\n' % {'page': page, 'topic': topic})

  def finish(self):
    self._file.close()

parser = DmozParser()
parser.add_handler(CSVWriter('output.txt'))
parser.run()
