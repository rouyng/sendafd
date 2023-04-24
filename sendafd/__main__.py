import argparse
import logging
import sys

from requests import HTTPError

from . import apiclient, emailclient, renderer


VERSION = "0.1.0"

logger = logging.getLogger("sendafd")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s',
                              datefmt='%d-%b-%y %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

def main():
    """Main program functionality, called if the sendafd package is executed directly"""
    # initialize command line argument parser
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument('-l', '--locations',
                        required=False,
                        action='store_true',
                        help="Print a list of valid region codes with descriptions and exit.")
    pre_args, _ = pre_parser.parse_known_args()

    if pre_args.locations:
        try:
            apiclient.print_region_codes(apiclient.get_region_codes())
        except HTTPError:
            logger.critical("Error connecting to the NWS API", exc_info=True)
            sys.exit(1)
        except (ValueError, KeyError):
            logger.critical("Error parsing received location codes", exc_info=True)
            sys.exit(1)
        else:
            sys.exit()

    parser = argparse.ArgumentParser(description="sendAFD emails the NWS Area Forecast Discussion for "
                                                 "a chosen area. For more details, see README.md",
                                     prog="sendafd", parents=[pre_parser])

    # add command line arguments/options/flags
    # TODO: refactor command line arguments to not require placeholder email-related arguments
    #  when run with -w
    parser.add_argument('recipient',
                        help="Destination email address."
                        )
    parser.add_argument('email_server',
                        help="Domain or IP of SMTP server used to send outgoing emails."
                        )
    parser.add_argument('email_username',
                        help="Username used when connecting to the SMTP server."
                        )
    parser.add_argument('email_password',
                        help="Password used when connecting to the SMTP server."
                        )
    parser.add_argument('region',
                        help="Three-letter region code for the Area Forecast Discussion."
                        )
    parser.add_argument('-d', '--dry-run',
                        action='store_true',
                        help="Do not connect to SMTP server, just print email to stdout")
    parser.add_argument('-f', '--file',
                        action='store',
                        nargs=1,
                        help="Do not connect to SMTP server, just output rendered email to the specified path. Default: output.msg")
    parser.add_argument('-w', '--web',
                        action='store',
                        nargs=1,
                        help="Do not connect to SMTP server, output rendered template to the specified path, without adding email header or doing any email-specific formatting. Default output path: output.html")
    parser.add_argument('-i', '--ignore-region-validation',
                        action='store_true',
                        help="Do not validate supplied region code and attempt to fetch AFD from "
                             "NWS anyway.")
    parser.add_argument('-m', '--monitor',
                        action='store_true',
                        help="Run in monitor mode, where a cache of each AFD is stored after sending. "
                             "Only send an email if the newest fetched AFD has changed. This is "
                             "intended to be run at a shorter interval, such as every hour.")
    parser.add_argument('-p', '--plaintext',
                        action='store_true',
                        help="Send the email in plaintext as formatted by the NWS, without any template.")
    parser.add_argument('-s', '--sender-address',
                        nargs='?',
                        default="",
                        help="Sender's email address, if different from email_username.")
    parser.add_argument('-t', '--template',
                        nargs='?',
                        default='default_email_template.html',
                        help="Filename of template to use when rendering email. Searches in \'templates\' subdirectory. Defaults to 'default_email_template.html'")
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
        if args.monitor:
            logger.info("Starting sendAFD in monitor mode")
        else:
            logger.info("Starting sendAFD")
        raw_api_response = apiclient.fetch_afd(region=args.region,
                                               monitor=args.monitor,
                                               ignore_region_validation=args.ignore_region_validation)
        if raw_api_response['error'] is not None:
            logger.critical(f"Error fetching data from NWS API: {raw_api_response['error']}")
        elif raw_api_response['response'] is None and raw_api_response['error'] is None:
            logger.info("AFD has not changed, email will not be sent.")
        else:
            # parse afd into AreaForecastDiscussion object
            parsed_afd = apiclient.AreaForecastDiscussion(raw_api_response['response'])
            if args.plaintext:
                template = None
            else:
                template = args.template
            if args.sender_address:
                sender_email = args.sender_address
            else:
                sender_email = args.email_username
            # TODO: gracefully handle jinja2.exceptions.TemplateNotFound
            if args.web:
                rendered_html = renderer.render_web(parsed_afd=parsed_afd,
                                                    afd_json=raw_api_response['response'],
                                                    template_path=template)
                logger.info(f"File output for web enabled, printing html to {args.file}")
                with open(args.web[0], 'w', encoding='utf-8') as f:
                    f.write(rendered_html)
            else:
                rendered_email = renderer.build_email(afd=parsed_afd,
                                                  sender_email=sender_email,
                                                  recipient_email=args.recipient,
                                                  template_path=template
                                                  )
                if args.dry_run:
                    logger.info("Dry run enabled, printing email to stdout")
                    print(rendered_email.as_string())
                elif args.file:
                    logger.info(f"File output enabled, printing email to {args.file}")
                    with open(args.file[0], 'w', encoding='utf-8') as f:
                            f.write(rendered_email.as_string())
                else:
                    email_result = emailclient.send_email(smtp_server=args.email_server,
                                               smtp_username=args.email_username,
                                               smtp_pw=args.email_password,
                                               email=rendered_email,
                                               )
                    if not email_result:
                        logger.critical("Failed to send email")
        logger.info("sendAFD finished")
    except KeyboardInterrupt:
        logger.critical("Received keyboard interrupt, exiting!")

if __name__ == "__main__":
    main()