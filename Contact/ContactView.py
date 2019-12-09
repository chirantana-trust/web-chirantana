#GAE modules
import webapp2
from google.appengine.ext.webapp import template

from google.appengine.ext import ndb

#Application specific Modules
from ExtraModules.gettemplate import gettemplate
from ExtraModules import phonenumbers
from model import Messages


def checkPhoneNumber(number, country_code):
    try:
        numobj = phonenumbers.parse(number, country_code)
        if phonenumbers.is_valid_number(numobj):
            return True
        else:
            return False
    except:
        return False


class getMsgValues:
    def __init__(self, obj):
        self.namevalue = obj.request.get('name')
        self.emailvalue = obj.request.get('email')
        self.phonevalue = obj.request.get('phone')
        self.subjectvalue = obj.request.get('subject')
        self.completemessage = obj.request.get('message')
        self.countrycode = obj.request.get('countrycode')

class Contact(webapp2.RequestHandler):
    def get(self):
        template_values = {
                           'page':"Contact",
                           'msg_sent_status':False,              
        }
        self.response.out.write(template.render(gettemplate('Contact'), template_values))
 
 
class SubmitMessage(webapp2.RequestHandler): 
    def post(self):
        template_values = {
            'page':"Contact",
            'msg_sent_status':False,                                     
        }
        msg = getMsgValues(self)
            
        if not checkPhoneNumber(msg.phonevalue, msg.countrycode):
            template_values['msg_sent_status'] = False
            template_values['msg'] = "Invalid Phone number"
            self.response.out.write(template.render(gettemplate('Contact'), template_values))
        template_values['msg'] = None 
        template_values['msg_sent_status'] = True
             
        msg = Messages(parent=ndb.Key("MSG", msg.emailvalue or "*notice*"),
                          name=msg.namevalue,
                          email=msg.emailvalue,
                          phone=msg.phonevalue,
                          subject=msg.subjectvalue,
                          message=msg.completemessage)
        msg.put()
        self.response.out.write(template.render(gettemplate('Contact'), template_values))
        

