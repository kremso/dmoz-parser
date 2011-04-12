Dmoz
====
[Dmoz](http://www.dmoz.org) is an open directory which lists and groups web pages into categories (directories). Their data is publicly available, but provided as an RDF file - a huge, funny XML file.

Dmoz Parser
========

This is a really simple python implementation of the Dmoz RDF parser. It does not try to be smart and process the parsed XML for you, you have to provide a handler implementation where YOU decide what to do with the data (store it in file, database, print, etc.).

This parser makes the assumption is the last entity in each dmoz page is _topic_:

     <ExternalPage about="http://www.awn.com/">
       <d:Title>Animation World Network</d:Title>
       <d:Description>Provides information resources to the international animation community. Features include searchable database archives, monthly magazine, web animation guide, the Animation Village, discussion forums and other useful resources.</d:Description>
       <priority>1</priority>
       <topic>Top/Arts/Animation</topic>
     </ExternalPage>

This assumption is strictly checked, and processing will abort if it is violated.

The RDF file needs to be downloaded and unpacked before running the parser. You can [download the RDF](http://rdf.dmoz.org/rdf/content.rdf.u8.gz) from Dmoz site. You should _gunzip_ it into this directory.

The RDF is pretty large, over 2G unpacked and parsing it takes some time, so there is a progress indicator.

Warnings
--------

This parser does not check for links between topics in the hierarchy, or any sophisticated parsing of the hierarchy.

The same URL might appear in multiple locations in the hierarchy.

Usage
-----
Instantiate the parser, provide the handler and run.

    #!/usr/bin/env python
    
    from parser import DmozParser
    from handlers import JSONWriter
    
    parser = DmozParser()
    parser.add_handler(JSONWriter('output.json'))
    parser.run()

JSONWriter is the builtin handler which outputs the pages, one JSON object per line.
(Note: This is different than saying that the entire file is a large JSON list.)

Requirements
------------

[simplejson](http://pypi.python.org/pypi/simplejson/) is necessary for writing JSON output.

Built-in handlers
-----------------
There are two builtin handlers so far - _JSONWriter_ and _CSVWriter_.
_CSVWriter_ is buggy (see "handler.py" to understand why), and we recommend the _JSONWriter_.

Handlers
--------
A handler must implement two methods:

    def page(self, page, content)

this method will be called every time a new page is extracted from the RDF, argument _page_ will contain the URL of the page and _content_ will contain a dictionary of page content.

    def finish(self)

The finish method will be called after the parsing is done. You may want to clean up here, close the files, etc.
