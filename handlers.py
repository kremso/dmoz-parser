class CSVWriter:
  def __init__(self, name):
    self._file = open(name, 'w')

  def page(self, page, topic):
    if page != None and page != "" and topic != None and topic != "":
      self._file.write('%(page)s,%(topic)s\n' % {'page': page, 'topic': topic})
    else:
      print "Skipping page, one of the attributes is missing"

  def finish(self):
    self._file.close()

