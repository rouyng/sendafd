import argparse
import logging

from . import apiclient, emailclient, renderer

VERSION = "0.1.0"

logger = logging.getLogger("sendafd")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s',
                              datefmt='%d-%b-%y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

# initialize command line argument parser
parser = argparse.ArgumentParser(description="sendAFD emails the NWS's Area Forecast Discussion for "
                                             "a chosen area. For more details, see README.md",
                                 prog="sendafd")

# add command line arguments/options/flags
parser.add_argument('-l', '--locations',
                    action='store_true',
                    help="Print a list of valid location IDs and descriptions for Area Forecast "
                         "Discussions and exit")
parser.add_argument('-v', '--verbose',
                    action='store_true',
                    help="Print debug messages.")
parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')

args = parser.parse_args()

# set the logging level according to command line flags(s)
if args.verbose:
    logger.setLevel("DEBUG")
    logger.warning("Log level set to debug")
else:
    logger.setLevel("INFO")

try:
    if args.locations:
        apiclient.print_region_codes()
    else:
        logger.info("Starting sendAFD...")
        pass
        # TODO: fetch AFD from NWS API
        # TODO: parse raw API response into text ready to insert into template
        # TODO: generate email from template and AFD text
        # TODO: send email using SMTP server
        logger.info("sendAFD finished")
except KeyboardInterrupt:
    logger.critical("Received keyboard interrupt, exiting!")
