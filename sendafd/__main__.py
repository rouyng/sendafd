import argparse
import logging
from requests import HTTPError

from . import apiclient, emailclient, renderer


VERSION = "0.1.0"

logger = logging.getLogger("sendafd")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s',
                              datefmt='%d-%b-%y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

# initialize command line argument parser
parser = argparse.ArgumentParser(description="sendAFD emails the NWS Area Forecast Discussion for "
                                             "a chosen area. For more details, see README.md",
                                 prog="sendafd")

# add command line arguments/options/flags
parser.add_argument('region',
                    nargs='?',
                    help="Three-letter region code for the Area Forecast Discussion."
                    )
parser.add_argument('-l', '--locations',
                    action='store_true',
                    help="Print a list of valid region codes with descriptions and exit.")
parser.add_argument('-m', '--monitor',
                    action='store_true',
                    help="Run in monitor mode, where a cache of each AFD is stored after sending. "
                         "Only send an email if the newest fetched AFD has changed. This is "
                         "intended to be run at a shorter interval, such as every hour.")
parser.add_argument('-v', '--verbose',
                    action='store_true',
                    help="Print debug messages.")
parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')

args = parser.parse_args()

# set the logging level according to command line flags(s)
if args.verbose:
    logger.setLevel("DEBUG")
    logger.info("Log level set to debug")
else:
    logger.setLevel("INFO")

try:
    if args.locations:
        try:
            apiclient.print_region_codes(apiclient.get_region_codes())
        except HTTPError:
            logger.critical("Error connecting to the NWS API", exc_info=True)
    else:
        if args.monitor:
            logger.info("Starting sendAFD in monitor mode")
        else:
            logger.info("Starting sendAFD")
        raw_api_response = apiclient.fetch_afd(region=args.region, monitor=args.monitor)
        if raw_api_response['error'] is not None:
            logger.critical(f"Error fetching data from NWS API: {raw_api_response['error']}")
        elif raw_api_response['response'] is None and raw_api_response['error'] is None:
            logger.info("AFD has not changed, email will not be sent.")
        else:
            pass
            # TODO: parse raw API response into text ready to insert into template
            # TODO: generate email from template and AFD text
            # TODO: send email using SMTP server
        logger.info("sendAFD finished")
except KeyboardInterrupt:
    logger.critical("Received keyboard interrupt, exiting!")
