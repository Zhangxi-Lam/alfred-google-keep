import unittest

from gkeepapi.node import ColorValue

from kp_util import parse_query


class KpUtilTest(unittest.TestCase):
    def testParseQuerySuccess(self):
        query = '@title_1 :content_1 #tag_1 &red'
        res = parse_query(query)
        expect = {
            'title': 'title_1',
            'content': 'content_1',
            'tag': 'tag_1',
            'color': ColorValue.Red
        }
        self.assertEqual(expect, res)

        query = '&WHITE@title_1'
        res = parse_query(query)
        expect = {
            'title': 'title_1',
            'content': None,
            'tag': None,
            'color': ColorValue.White
        }
        self.assertEqual(expect, res)

        query = '&Pink@title_1   :tag is \#tag1, color is \&Red, title is \@title_2 and escape is \\\\.'  # pylint: disable=W1401
        res = parse_query(query)
        expect = {
            'title': 'title_1',
            'content': 'tag is #tag1, color is &Red, title is @title_2 and escape is \\.',
            'tag': None,
            'color': ColorValue.Pink
        }
        self.assertEqual(expect, res)

        query = ''
        res = parse_query(query)
        expect = {
            'title': None,
            'content': None,
            'tag': None,
            'color': None
        }
        self.assertEqual(expect, res)

    def testParseQueryFail(self):
        with self.assertRaises(ValueError):
            query = '@title @title'
            parse_query(query)
        with self.assertRaises(ValueError):
            query = '@title\\'
            parse_query(query)
        with self.assertRaises(ValueError):
            query = '\\@title'
            parse_query(query)
        with self.assertRaises(ValueError):
            query = 'title@title'
            parse_query(query)
