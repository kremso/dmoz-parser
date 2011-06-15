import copy
import simplejson
class JSONWriter:
  def __init__(self, name):
    self._file = open(name, 'w')

  def page(self, page, content):
    if page != None and page != "":
      newcontent = copy.copy(content)
      newcontent["url"] = page

      self._file.write(simplejson.dumps(newcontent) + "\n")
    else:
      print "Skipping page %s, page attribute is missing" % page

  def finish(self):
    self._file.close()

class CSVWriter:
  # Note: The CSVWriter has several bugs and assumptions, as documented below.
  def __init__(self, name):
    self._file = open(name, 'w')

  def page(self, page, content):
    if page != None and page != "":
      page = page.encode("utf-8")
      page = page.replace('"', '')
      page = page.replace('&quot;', '')

      self._file.write('"%(page)s"' % {'page': page})
#      for type in content:
      # For CSV, read only these fields, in only this order.
      newcontent = {}
      for type in ['d:Title', 'd:Description', 'priority', 'topic']:
        newcontent[type] = content[type].encode("utf-8")
        newcontent[type] = newcontent[type].replace('"', '')
        newcontent[type] = newcontent[type].replace('&quot;', '')
        # BUG: Convert comma to something else? Otherwise, it will trip up the CSV parser.
        self._file.write(',"%s"' % newcontent[type])

      self._file.write("\n")
    else:
      print "Skipping page %s, page attribute is missing" % page

  def finish(self):
    self._file.close()


