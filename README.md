# sendAFD
sendAFD is a command-line tool that emails the National Weather Service's Area Forecast Discussion for a chosen area. It provides a template system that defaults to a simple, readable email format, but also enables you to create and modify your own email templates. sendAFD is designed to be run automatically as a cronjob. Emails are sent via a SMTP server of your choice.

## Why use this?
The NWS publishes Area Forecast Discussions (AFDs) multiple times a day for regions across the U.S. The AFD is a summary of current weather patterns, written by a NWS meteorologist.

## Requirements
- Python 3.11 or greater.
- Internet connection
- Access to an SMTP server for sending emails


## Usage

```
sendafd [-ghlmpv] [-b COMMAND] [-t TEMPLATE] recipient email_server email_username email_password region

Emails a National Weather Service (United States) Area Forecast Discussion for the selected region.

positional arguments:
    recipient		Destination email address for the AFD
    email_server	Domain or IP of SMTP server used to send outgoing emails
    email_username	Username used when connecting to the SMTP server
    email_password	Password used when connecting to the SMPT server
    region      	Three-letter region code for the Area Forecast Discussion.
    
options:
    -b, --buildcmd COMMAND	Run this build command, passing the path to the email generated from the template as an argument. Then email the output of the build command. Intended for use with email tools/frameworks that require a build step.
    -g, --glossary		    Add links to meteorological terms
    -h, --help			    Show this help message and exit
    -l, --locations		    Print a list of valid region codes with descriptions and exit.
    -m, --monitor		    Run in monitor mode, where a cache of each AFD is stored after sending. Only send an email if the newest fetched AFD has changed. This is intended to be run at a shorter interval, such as every hour.
    -p, --plaintext		    Send the email in plaintext, without any template
    -t, --template TEMPLATE	Use the template at the path specified by TEMPLATE. Default: templates/default.html
    -v, --verbose		    Print debug messages.
    --version			    Display version information and exit
```

### Examples
Send the AFD for region "PSR" (Phoenix Sky Harbor) using the default email template to foo@bar.com, using the server email.server.com, with username "someuser" and password "somepassword":
`sendafd foo@bar.com email.server.com someuser somepassword PSR`

## License
sendAFD is licensed under the MIT License. See LICENSE.md for details.