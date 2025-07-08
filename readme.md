we will be using the general purpose imap, rather than any api as imap will allow us to access different types of email servers.

.env file structure

EMAIL_SERVER=  ## refer to https://www.systoolsgroup.com/imap/
EMAIL_USERNAME=
EMAIL_APP_PASSWORD=

cron-job syntax
 
min   hour  date  month  day_of_week command -> command to run,bash script
0-60  0-23  1-31   1-12   0-7(sunday:=0 or 7)