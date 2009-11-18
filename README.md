Dmoz
====
[Dmoz](http://www.dmoz.org) is an open directory which lists and groups web pages into categories (directories). Their data is publicly available, but provided as an RDF file - a huge, funny XML file.

Dmoz Parser
========

This is a really simple python implementation of the Dmoz RDF parser. It does not try to be smart and process the parsed XML for you, you have to provide a handler implementation where YOU decide what to do with the data (store it in file, database, print, etc.).

The RDF file needs to be downloaded and unpacked before running the parser. You can [download the RDF](http://rdf.dmoz.org/rdf/content.rdf.u8.gz) from Dmoz site.

The RDF is pretty large, over 2G unpacked and parsing it takes some time, so there is a progress indicator.

Usage
-----
Instantiate the parser, provide the handler and run.

    #!/usr/bin/env python
    
    from parser import DmozParser
    from handlers import CSVWriter
    
    parser = DmozParser()
    parser.add_handler(CSVWriter('output.txt'))
    parser.run()

CSVWriter is the builtin handler which stores the results into a comma separated file.

Handlers
--------
A handler must implement two methods:

    def page(self, page, topic)

this method will be called every time a new page is extracted from the RDF, argument _page_ will contain the URL of the page and _topic_ will contain the page category.

    def finish(self)

The finish method will be called after the parsing is done. You may want to clean up here, close the files, etc.


Built-in handlers
-----------------
There is only one builtin handler so far - _CSVWriter_ which stores the data in a CSV file.
