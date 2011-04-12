#!/usr/bin/env python

from parser import DmozParser
from handlers import JSONWriter

parser = DmozParser()
parser.add_handler(JSONWriter('output.json'))
parser.run()
