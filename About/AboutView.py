#GAE modules
import webapp2
from google.appengine.ext.webapp import template

#Application specific Modules
from ExtraModules.gettemplate import gettemplate

class About(webapp2.RequestHandler):
    def get(self):
        template_values = {
                           'page':"About",
                           'msg_sent_status':False,
                           
        }
        self.response.out.write(template.render(gettemplate('About'), template_values))