#!/usr/bin/env python

from testtool import suitebuilder

import unittest


def main():
    suite = suitebuilder.createSuite(dirs=['units', 'stations'])
    runner = unittest.TextTestRunner()
    runner.run(suite)
    

if __name__ == '__main__':
    main()
