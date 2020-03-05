import argparse

from . import extract


def line_count(path):
    i = 0
    with open(path) as lines:
        for i, _ in enumerate(lines):
            pass
    return i + 1


def test_parse():
    extract(
        argparse.Namespace(
            carver='apsb', export=['bodyfile', 'files'], image='test/wsdf.dmg', log='INFO', method='parse', offset=40))

    # should extract 290 items
    assert line_count('wsdf.dmg.parse.bodyfile') == 26


def test_carve():
    extract(
        argparse.Namespace(
            carver='apsb', export=['bodyfile', 'files'], image='test/wsdf.dmg', log='INFO', method='carve', offset=40))

    # should extract 290 items
    assert line_count('wsdf.dmg.carve_apsb.bodyfile') == 290
