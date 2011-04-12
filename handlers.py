class CSVWriter:
  def __init__(self, name):
    self._file = open(name, 'w')

  def page(self, page, content):
    if page != None and page != "":
      page = page.replace('"', '')
      page = page.replace('&quot;', '')

      self._file.write('"%(page)s"' % {'page': page})
#      for type in content:
      # For CSV, read only these fields, in only this order.
      for type in ['d:Title', 'd:Description', 'priority', 'topic']:
        content[type] = content[type].replace('"', '')
        content[type] = content[type].replace('&quot;', '')
        # TODO: Convert comma to something else? Otherwise, it will trip up the CSV parser.
        self._file.write(',"%s"' % content[type])

      self._file.write("\n")
    else:
      print "Skipping page, page attribute is missing"

  def finish(self):
    self._file.close()

