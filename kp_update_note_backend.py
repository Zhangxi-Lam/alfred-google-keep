import logging
import sys
import argparse

logging.basicConfig(
    format='[%(asctime)s.%(msecs)d %(levelname)-8s %(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG,
    filename='log/kp.log',
    filemode='w'
)

logging.debug("HERE!")

parser = argparse.ArgumentParser()
parser.add_argument('--query', type=str, default='')


# def main(wf):
#     try:
#         logging.debug("get args: %s", wf.args)
#     except Exception:
#         logging.debug("Exception!")
#         return 0


if __name__ == u"__main__":
    args = parser.parse_args()
    logging.debug(args)
    sys.stdout.write("test")
