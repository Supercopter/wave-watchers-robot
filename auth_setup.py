#Setup code for wave-watchers breakwatery
import hashlib
import cgi
import simplejson
authDict = {"nat.abbotts":'5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8',
"Albonobo":'5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8'}

if __name__ == '__main__':
  query= cgi.FieldStorage()
  us= query.getvalue('username')
  pw= query.getvalue('password')
  #us_accept = 'guest'
  auth = "0"
  if us in authDict:
    us_accept = us
    pwd_accept = authDict[us]
    if pw = pwd_accept:
      auth = '1'
  json_body = {'auth':auth}
  json_str = simplejson.dumps(json_body)
  print "Content-type: application/json\n\n"
  print json_str 