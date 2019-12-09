from google.appengine.ext import ndb

class Messages(ndb.Model):
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    phone = ndb.StringProperty(required=True)
    subject = ndb.StringProperty()
    message = ndb.TextProperty(required=True)
    
    @classmethod
    def query_message(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key)


    