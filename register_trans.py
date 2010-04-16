import logging
import cgi
import hashlib
from google.appengine.api import mail

MAIL_TO = "nat.abbotts@googlemail.com"

if __name__ == '__main__':
  query= cgi.FieldStorage()
  us= query.getvalue('un')
  pw= query.getvalue('pwd')
  logging.info("user name is %s pwd is %s" % (us,pw))
  print('Content-type: text/html\n\n')
  print('Username and Password submitted. You may need to wait 1 or 2 days for the service to be updated.')
  #print('Your hashed password is %s' % hashlib.sha1(pw).hexdigest())
  # TODO - Save the username and hashed pwd in the datastore instead
  # Option 2: mail the username and password to the moderator (python email module)
  mail_body = "The username %s has chosen the password %s" % (us,hashlib.sha1(pw).hexdigest())
  mail.send_mail(sender="nat.abbotts@googlemail.com",to=MAIL_TO,subject="Addition to WW",body=mail_body) 