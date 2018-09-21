import argparse

from . import main, extract

def wc(path):
    with open(path) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def test_parse():
    extract(argparse.Namespace(carver='apsb', export=['bodyfile', 'files'], image='test/wsdf.dmg', log='INFO', method='parse', offset=40))

    # should extract 290 items
    assert 26 == wc('test/wsdf.dmg.parse.bodyfile')

def test_carve():
    extract(argparse.Namespace(carver='apsb', export=['bodyfile', 'files'], image='test/wsdf.dmg', log='INFO', method='carve', offset=40))

    # should extract 290 items
    assert 290 == wc('test/wsdf.dmg.carve_apsb.bodyfile')
