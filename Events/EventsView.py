#GAE modules
import webapp2

from google.appengine.ext.webapp import template

#Application specific Modules
from ExtraModules.gettemplate import gettemplate
from DataModels.model import Event

from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore

class ImageHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, brochure_key):
        if not blobstore.get(brochure_key):
            self.error(404)
        else:
            self.send_blob(brochure_key)


class Events(webapp2.RequestHandler):
    def get(self):
        que = Event.query()
        events = que.order(Event.title).fetch()
        template_values = {
                           'page':"Events",
                           'msg_sent_status':False,
                           'events':events,
        }
        
        #res = dict(results[0])
        self.response.out.write(template.render(gettemplate('Events'), template_values))

class Calendar(webapp2.RequestHandler):
    def get(self):
        template_values ={
                          }
        self.response.out.write(template.render(gettemplate('Calendar'), template_values))
        
        