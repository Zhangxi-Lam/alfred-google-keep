import unittest

from gkeepapi.node import ColorValue

from google_keep_util import parse_query


class KpUtilTest(unittest.TestCase):
    def testParseQuerySuccess(self):
        query = '@title_1 :content_1 #label_1 &red'
        res = parse_query(query)
        expect = {
            'title': 'title_1',
            'content': 'content_1',
            'label': 'label_1',
            'color': 'red'
        }
        self.assertEqual(expect, res)

        query = '&WHITE@title_1'
        res = parse_query(query)
        expect = {
            'title': 'title_1',
            'content': None,
            'label': None,
            'color': 'white'
        }
        self.assertEqual(expect, res)

        query = '&Pink@title_1   :label is \#label1, color is \&Red, title is \@title_2 and escape is \\\\.'  # pylint: disable=W1401
        res = parse_query(query)
        expect = {
            'title': 'title_1',
            'content': 'label is #label1, color is &Red, title is @title_2 and escape is \\.',
            'label': None,
            'color': 'pink'
        }
        self.assertEqual(expect, res)

        query = ''
        res = parse_query(query)
        expect = {
            'title': None,
            'content': None,
            'label': None,
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
        with self.assertRaises(ValueError):
            query = '@title&not_a_color'
            parse_query(query)
