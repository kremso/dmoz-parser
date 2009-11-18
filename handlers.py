class CSVWriter:
  def __init__(self, name):
    self._file = open(name, 'w')

  def page(self, page, topic):
    self._file.write('%(page)s; %(topic)s\n' % {'page': page, 'topic': topic})

  def finish(self):
    self._file.close()

