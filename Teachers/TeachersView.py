#GAE modules
import webapp2
from google.appengine.ext.webapp import template

#Application specific Modules
from ExtraModules.gettemplate import gettemplate
from DataModels.model import Teacher

class Teachers(webapp2.RequestHandler):
    """
    Rendering the Teachers web page
    """
    
    def get(self):
        query = Teacher.query()
        teachers = query.fetch()
        
        template_values = {
                           'page':"Teachers",
                           'msg_sent_status':False,
                           'teachers':teachers,
                                                     
        }
        
        self.response.out.write(template.render(gettemplate('Teachers'), template_values))
    