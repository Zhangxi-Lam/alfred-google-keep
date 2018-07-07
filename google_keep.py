# -*- coding: utf-8 -*-
import argparse
import sys
import json

from workflow import Workflow, ICON_WEB, ICON_WARNING, PasswordNotFound

from util.kp_util import parse_query, parse_to_subtitle

logger = None


def main(wf):
    parser = argparse.ArgumentParser()
    parser.add_argument('--setemail', dest='email', nargs='?', default=None)
    parser.add_argument('--setpassword', dest='password',
                        nargs='?', default=None)
    parser.add_argument('--delsetting', dest='delsetting',
                        action='store_true', default=False)
    parser.add_argument('query', nargs='?', default=None)
    args = parser.parse_args(wf.args)
    if args.email:
        wf.save_password('google_keep_email', args.email)
        return 0
    if args.password:
        wf.save_password('google_keep_password', args.password)
        return 0
    if args.delsetting:
        wf.delete_password('google_keep_email', args.email)
        wf.delete_password('google_keep_password', args.password)
        return 0
    try:
        wf.get_password('google_keep_email')
    except PasswordNotFound:
        wf.add_item('no google account email set.',
                    'please use kpsetemail to set your google account email.',
                    valid=False,
                    icon=ICON_WARNING
                    )
        wf.send_feedback()
        return 0
    try:
        wf.get_password('google_keep_password')
    except PasswordNotFound:
        wf.add_item('no google account password set.',
                    'please use kpsetpassword to set your google account passwordpassword.',
                    valid=False,
                    icon=ICON_WARNING
                    )
        wf.send_feedback()
        return 0

    # Get query from Alfred
    query = args.query
    try:
        logger.debug("query: %s", query)
        note = parse_query(query)
        logger.debug("note: %s", note)
        wf.add_item(
            title="Type a Note",
            subtitle=parse_to_subtitle(note),
            arg=json.dumps(note),
            valid=True,
            icon=ICON_WEB)
        wf.send_feedback()
    except ValueError as e:
        logger.debug("exception: %s", e)
        return 0


if __name__ == u"__main__":
    wf = Workflow(libraries=['./lib'])
    logger = wf.logger
    sys.exit(wf.run(main))
