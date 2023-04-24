# sendAFD
sendAFD is a command-line tool that emails the National Weather Service's Area Forecast Discussion for a chosen area.  sendAFD is designed to be run automatically as a cronjob. Emails are sent via a SMTP server of your choice.

The National Weather Service publishes area forecast discussions (AFDs) multiple times a day for multiple regions across the U.S. The AFD is a text summary of current weather patterns in the region, written by a NWS meteorologist. This publication is usually accessed by visiting a web page hosted by the local NWS forecast office. sendAFD fetches the Area Forecast Discussion from the NWS API and sends it directly to your inbox. It can compare the fetched AFD to the last fetched one, sending it only if it has changed. It can also reformat the AFD using a jinja template, allowing the user to customize the presentation style. This template defaults to a simple, readable email format, but also enables you to create and modify your own email templates.

Additionally, instead of formatting the area forecast discussion

## Requirements
- Python 3.11 or greater.
- Internet connection
- (optional) Access to an SMTP server for sending emails

## Usage

```
usage: sendafd [-h] [-l] [-d] [-f FILE] [-w WEB] [-i] [-m] [-p] [-s [SENDER_ADDRESS]] [-t [TEMPLATE]] [-v] [--version] recipient email_server email_username email_password region

sendAFD emails the NWS Area Forecast Discussion for a chosen area. For more details, see README.md

positional arguments:
  recipient             Destination email address.
  email_server          Domain or IP of SMTP server used to send outgoing emails.
  email_username        Username used when connecting to the SMTP server.
  email_password        Password used when connecting to the SMTP server.
  region                Three-letter region code for the Area Forecast Discussion.

options:
  -h, --help            show this help message and exit
  -l, --locations       Print a list of valid region codes with descriptions and exit.
  -d, --dry-run         Do not connect to SMTP server, just print email to stdout
  -f FILE, --file FILE  Do not connect to SMTP server, just output rendered email to the specified path. Default: output.msg
  -w WEB, --web WEB     Do not connect to SMTP server, output rendered template to the specified path, without adding email header or doing any email-specific formatting. Default output path: output.html
  -i, --ignore-region-validation
                        Do not validate supplied region code and attempt to fetch AFD from NWS anyway.
  -m, --monitor         Run in monitor mode, where a cache of each AFD is stored after sending. Only send an email if the newest fetched AFD has changed. This is intended to be run at a shorter interval, such as every hour.
  -p, --plaintext       Send the email in plaintext as formatted by the NWS, without any template.
  -s [SENDER_ADDRESS], --sender-address [SENDER_ADDRESS]
                        Sender's email address, if different from email_username.
  -t [TEMPLATE], --template [TEMPLATE]
                        Filename of template to use when rendering email. Searches in 'templates' subdirectory. Defaults to 'default_email_template.html'
  -v, --verbose         Print debug messages.
  --version             show program's version number and exit
```

### Examples
Print a list of the region codes for which the NWS publishes Area Forecast Discussions. Do this first to find the three-letter code for the desired region:
`sendafd -l`

Send the AFD for region "PSR" (Phoenix Sky Harbor) using the default email template to foo@bar.com, using the server email.emailserver.com, with username/sender email "someuser@emailserver.com" and password "somepassword":
`sendafd foo@bar.com email.emailserver.com someuser@emailserver.com somepassword PSR`

Send the PSR AFD with the same sender and recipient, using plaintext only and no template:
`sendafd -p foo@bar.com email.emailserver.com someuser@emailserver.com somepassword PSR`

Send the PSR AFD as plaintext in monitor mode, which will only send an email if the AFD changes:
`sendafd -pm foo@bar.com email.emailserver.com someuser@emailserver.com somepassword PSR`

Send the PSR AFD using the custom template located at `templates/my_template.html`:
`sendafd -t my_template.html foo@bar.com email.emailserver.com someuser@emailserver.com somepassword PSR`

Generate a html file using the custom template located at `templates/sample_web_template.html`. Does not email the output. Used when serving the output as a web page:
`sendafd -w sample_web_template.html foo@bar.com email.emailserver.com someuser@emailserver.com somepassword PSR`

## Templating
sendAFD generates html email messages using a [jinja](https://jinja.palletsprojects.com/en/3.1.x/) template. See TEMPLATES.md and the default template at `templates/default_email_template.html` for more details.

## License
sendAFD is licensed under the MIT License. See LICENSE.md for details.