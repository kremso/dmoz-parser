#!/usr/bin/env python

from parser import DmozParser
from handlers import CSVWriter

parser = DmozParser()
parser.add_handler(CSVWriter('output.txt'))
parser.run()
