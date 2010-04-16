import logging
if __name__ == '__main__':
  print('Content-type: text/html\n\n')
  print "<h4>Enter your Wave username and choose a <u>new</u> password for wave watchers:</h4><form action='https://wave-watchers.appspot.com/registerTrans' method='POST'>Username: <input type='text' name='un' /><br />Password: <input type='password' name='pwd' /><br/><input type='submit' value='Go' /></form>" 