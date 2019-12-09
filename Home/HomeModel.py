from google.appengine.ext import ndb

class HomePagePhoto(ndb.Model):
    rank = ndb.IntegerProperty()
    photo = ndb.BlobKeyProperty()