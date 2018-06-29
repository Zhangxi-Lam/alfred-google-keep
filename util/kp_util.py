# -*- coding: utf-8 -*-
from gkeepapi.node import ColorValue

_TITLE_CHAR = '@'
_CONTENT_CHAR = ':'
_TAG_CHAR = '#'
_COLOR_CHAR = '&'
_ESCAPE_CHAR = '\\'

_COLOR_DICT = {
    'white': ColorValue.White,
    'red': ColorValue.Red,
    'orange': ColorValue.Orange,
    'yellow': ColorValue.Yellow,
    'green': ColorValue.Green,
    'teal': ColorValue.Teal,
    'blue': ColorValue.Blue,
    'darkblue': ColorValue.DarkBlue,
    'purple': ColorValue.Purple,
    'pink': ColorValue.Pink,
    'brown': ColorValue.Brown,
    'gray': ColorValue.Gray
}


def parse_query(query):
    d = {
        _TITLE_CHAR: [],
        _CONTENT_CHAR: [],
        _TAG_CHAR: [],
        _COLOR_CHAR: []
    }
    parse_into_dict(query, 0, d, '')
    d = remove_trailing_spaces(d)
    return parse_dict(d)


def parse_into_dict(query, i, d, cur):
    # If reaches the end of the query
    if i == len(query):
        return

    c = query[i]

    if cur:
        if c in [_TITLE_CHAR, _CONTENT_CHAR, _TAG_CHAR, _COLOR_CHAR]:
            if c == cur or d[c] != []:
                raise ValueError("Multiple special character: {}.".format(c))
            return parse_into_dict(query, i + 1, d, c)
        elif c == _ESCAPE_CHAR:
            i += 1
            if i == len(query):
                raise ValueError(
                    "No character follows escape character: {}.".format(_ESCAPE_CHAR))
            d[cur].append(query[i])
            return parse_into_dict(query, i + 1, d, cur)
        else:
            if d[cur] == None:
                d[cur] = [c]
            else:
                d[cur].append(c)
            return parse_into_dict(query, i + 1, d, cur)
    else:
        # Initial state
        if c in [_TITLE_CHAR, _CONTENT_CHAR, _TAG_CHAR, _COLOR_CHAR]:
            return parse_into_dict(query, i + 1, d, c)
        else:
            raise ValueError("Character input before special character.")


def remove_trailing_spaces(d):
    res = {}
    for k in d.keys():
        if d[k]:
            v = ''.join(d[k])
            res[k] = v.rstrip()
    return res


def parse_dict(d):
    if d.get(_COLOR_CHAR, None):
        color_str = d[_COLOR_CHAR].lower()
        if not _COLOR_DICT.get(color_str, None):
            raise ValueError("Invalid Color value: {}".format(d[_COLOR_CHAR]))
        d[_COLOR_CHAR] = _COLOR_DICT[color_str]

    res = {}
    res['title'] = d.get(_TITLE_CHAR, None)
    res['content'] = d.get(_CONTENT_CHAR, None)
    res['tag'] = d.get(_TAG_CHAR, None)
    res['color'] = d.get(_COLOR_CHAR, None)
    return res
