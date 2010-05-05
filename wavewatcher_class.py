from google.appengine.ext import db

ACCESS_LEVELS = {'OWNER':1, 'MEMBER':2, 'TRUSTED':3, 'ROBOT':4}
VILLAIN_LEVELS = {'BLACKLIST':1, 'GREYLIST':2}

class WaveWatchers(db.Model):
  userid = db.StringProperty(required=True)
  fullname = db.StringProperty(required=False)
  level = db.IntegerProperty(required=True)
  when = db.DateTimeProperty(auto_now_add=True)

class Villain(db.Model):
  userid = db.StringProperty(required=True)
  fullname = db.StringProperty(required=False)
  level = db.IntegerProperty(required=True)
  when = db.DateTimeProperty(auto_now_add=True)
