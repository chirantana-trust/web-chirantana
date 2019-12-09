#GAE modules
import webapp2
from google.appengine.ext.webapp import template

#Application specific Modules
from ExtraModules.gettemplate import gettemplate

class Courses(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'page':"Contact",
            'msg_sent_status':False,
                                                     
        }
        self.response.out.write(template.render(gettemplate('Courses'), template_values))