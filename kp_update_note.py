# -*- coding: utf-8 -*-
import logging
import sys

from workflow import Workflow, ICON_WEB

from util.kp_util import parse_query, serialize

logging.basicConfig(
    format='[%(asctime)s.%(msecs)d %(levelname)-8s %(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG,
    filename='log/kp.log',
    filemode='w'
)


def main(wf):
    # Get query from Alfred
    try:
        logging.debug("args: %s", wf.args)
        note = parse_query(wf.args[0])
        logging.debug("note: %s", note)
        wf.add_item(
            title="Type a Note",
            subtitle=serialize(note),
            arg=serialize(note),
            valid=True,
            icon=ICON_WEB)
        wf.send_feedback()
    except ValueError as e:
        logging.debug("exception: %s", e)
        return 0


if __name__ == u"__main__":
    wf = Workflow(libraries=['./lib'])
    sys.exit(wf.run(main))
