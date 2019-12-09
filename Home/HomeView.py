#GAE modules
import webapp2
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore

#Application specific Modules
from ExtraModules.gettemplate import gettemplate
from HomeModel import HomePagePhoto

class HomeImageHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, brochure_key):
        if not blobstore.get(brochure_key):
            self.error(404)
        else:
            self.send_blob(brochure_key)
      
class Home(webapp2.RequestHandler):
    def get(self):
        # Home page photos 
        query = HomePagePhoto.query()  
        photos = query.fetch()
        #
        template_values = {
                           'page':"Home",
                           'msg_sent_status':False,
                           'photos': photos,
                                                  
        }
        self.response.out.write(template.render(gettemplate('Home'), template_values))