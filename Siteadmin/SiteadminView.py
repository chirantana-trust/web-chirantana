#GAE modules
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
from datetime import datetime

#Application specific Modules
from ExtraModules.gettemplate import gettemplate
from Home.HomeModel import HomePagePhoto
from DataModels.model import Event, Holiday, Uploads,  Requests
from Teachers.TeachersView import Teachers


# Login Page
class Login(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'page': "Login",
        }
        template_values['login_url'] = users.create_login_url('/Siteadmin')
        self.response.out.write(template.render(gettemplate('Login'), template_values))
        
class SubmitRequest(webapp2.RequestHandler):
    def post(self):
        fields=['request', 'mygroup', 'email', 'description']
        fields_dict = dict.fromkeys(fields)
        request = Requests()
        for key in fields_dict:
            exec getKeyValue(key, 'request')
        print request
        try:
            request.put()
            sent_status='YES'
            message="Request sent successfully"
        except:
            sent_status="NO"
            message="Could not send request. One of the reason could be  the database is not running or internet connection is lost."
               
        self.redirect('/Login?title='+ request.request+ '&sent_status='+ sent_status + '&msg=' + message)

            
        
            
# sibmitting Event
class Siteadmin(webapp2.RequestHandler):
    def get(self):
        
        template_values = {
                           'page':"Siteadmin",
                           'title':None,
                           'sent_status':None,
                           'msg':None,
                        }
        
        user = users.get_current_user()
        template_values['name'] =  user.nickname()
        if user and users.is_current_user_admin():
            template_values['logout_url'] = users.create_logout_url('/Login') # redirecting to Login Page After successfull logout.
            self.response.out.write(template.render(gettemplate('Siteadmin'), template_values))
        else:
            template_values['logout_url'] = users.create_logout_url('/Login')
            self.response.out.write(template.render(gettemplate('Login'), template_values))



############## event related upload section ###############

def BrochureFileTypeSupported(uploadedfiletype):
    supportedTypes=['application/pdf', 'image/jpeg', 'image/png', 'image/bmp']
    if uploadedfiletype in supportedTypes:
        print "returning True"
        return True
    else:
        print "returning False"
        return False 
def getKeyValue(keyName, objName):
    return objName+"."+keyName+"=self.request.get('"+keyName+"')"

def parseSentStatus(obj):
    parsed = {
              'title': obj.request.get('title'),
              'sent_status': obj.request.get('sent_status'),
              'msg': obj.request.get('msg'),
    }    
    return parsed

class CreateEvent(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        user = users.get_current_user()
        
        template_values.update(parseSentStatus(self)) # parsing the update status and updating the template_values
        
        self.request.get('sent_status')
        template_values['name'] =  user.nickname()
        if user and users.is_current_user_admin():
            template_values['logout_url'] = users.create_logout_url('/Login') # redirecting to Login Page After successfull logout.
            template_values['upload_url'] = blobstore.create_upload_url('/Siteadmin/SubmitEvent') # default upload url for blob store.
            self.response.out.write(template.render(gettemplate('CreateEvent'), template_values))
        else:
            template_values['logout_url'] = users.create_logout_url('/Login')
            self.response.out.write(template.render(gettemplate('Login'), template_values))
               
class SubmitEvent(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        
        fields=['title', 'category', 'venue', 'description']
        fields_dict = dict.fromkeys(fields)
        
        evt = Event()
        
        #All values except brochure and date and time
        for key in fields_dict:
            exec getKeyValue(key, 'evt')
        
        #Brochure
        uploads = Uploads()
        if len(self.get_uploads('brochure')) > 0:
            uploads.file = self.get_uploads('brochure')[0].key()
            uploads.tag = "Brochure"
        #else:
            #uploads.file= None
        uploads.put()
        evt.brochure.append(uploads.key)
        
        #DateTime property
        evt.sdt = datetime.strptime(str(self.request.get('sdt')),'%d/%m/%Y %H:%M %p')
        evt.edt = datetime.strptime(str(self.request.get('edt')),'%d/%m/%Y %H:%M %p')
             

        if evt.brochure[0].get().file and not BrochureFileTypeSupported(blobstore.BlobInfo(evt.brochure[0].get().file).content_type):
            sent_status = 'NO'
            message="Unsupported file format"
        else:
            try:
                
                evt.put()
                
                sent_status='YES'
                message="Event updated successfully"
            except:
                sent_status="NO"
                message="Could not upload the Event. One of the reason could be  the database is not running or internet connection is lost."
               
        self.redirect('/Siteadmin/CreateEvent?title='+ evt.title+ '&sent_status='+ sent_status + '&msg=' + message)


################ Holiday event ######################
class CreateHoliday(webapp2.RequestHandler):
        def get(self):
            template_values = {
                           'page':"Siteadmin",
                        }
            user = users.get_current_user()
            template_values.update(parseSentStatus(self))
            template_values['name'] =  user.nickname()
            if user and users.is_current_user_admin():
                template_values['logout_url'] = users.create_logout_url('/Login') # redirecting to Login Page After successfull logout.
                template_values['upload_url'] = blobstore.create_upload_url('/Siteadmin/SubmitHoliday') # default upload url for blob store.
                self.response.out.write(template.render(gettemplate('CreateHoliday'), template_values))
            else:
                template_values['logout_url'] = users.create_logout_url('/Login')
                self.response.out.write(template.render(gettemplate('Login'), template_values))

    
class SubmitHoliday(webapp2.RequestHandler):
    def post(self):
        
        sent_status=None
        title=self.request.get('title')
        description=self.request.get('description')
        if(self.request.get('howlong') =='fday'):
            fullday=self.request.get('fdate')
        elif(self.request.get('howlong') == 'rday'):
            holidays_range_start_date = self.request.get('start_date')
            holidays_range_end_date = self.request.get('end_date')
        elif(self.request.get('howlong') == 'hday'):
            halfday = self.request.get('hdate')
            if(self.request.get('optradio') == "first-half"):
                first_half=True
                second_half=False
            elif(self.request.get('optradio') == "second-half"):
                second_half=True
                first_half=False
            else:
                sent_status="NO"
                message = "Please select first Half/second Half"
        else:
            sent_status="NO"
            message="Please select one  out of Fullday/Halfday/RangeDays"      
           
        if (sent_status != "NO"):  
            holiday=Holiday(parent=ndb.Key("HOLIDAY", title or "*notice*"),
                            title=title,
                            description=description,
                            fullday=fullday if fullday else None,
                            holidays_range_start_date=holidays_range_start_date if holidays_range_start_date else None,
                            holidays_range_end_date=holidays_range_end_date if holidays_range_end_date else None,
                            halfday=halfday if halfday else None,
                            first_half=first_half if first_half else None,
                            second_half=second_half if second_half else None,
                            )
            try:
                holiday.put()
                sent_status='YES'
                message="Holiday Updated successfully"
            except:
                sent_status='NO'
                message="Failed : Holiday update"
        self.redirect('/Siteadmin?title='+title+'&sent_status='+sent_status+'&msg='+message)


################ Teacher  ######################
class CreateTeacher(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        user = users.get_current_user()
        template_values['name'] =  user.nickname()
        template_values.update(parseSentStatus(self))
        if user and users.is_current_user_admin():
            template_values['logout_url'] = users.create_logout_url('/Login') # redirecting to Login Page After successfull logout.
            template_values['upload_url'] = blobstore.create_upload_url('/Siteadmin/SubmitTeacher') # default upload url for blob store.
            self.response.out.write(template.render(gettemplate('CreateTeacher'), template_values))
        else:
            template_values['logout_url'] = users.create_logout_url('/Login')
            self.response.out.write(template.render(gettemplate('Login'), template_values))        
        
               
class SubmitTeacher(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        
        fields=['firstname', 'middlename', 'lastname', 'profile_photo']
        fields_dict = dict.fromkeys(fields)
        
        teacher = Teachers()
        
        for key in fields_dict:
            if key == 'profile_photo':
                uploads = Uploads()
                if len(self.get_uploads('profile_photo')) > 0:
                    uploads.file = self.get_uploads('profile_photo')[0].key()
                    uploads.tag = "ProfilePhoto"
                else:
                    uploads.file= None
                uploads.put()
                teacher.profile_photo(uploads.key)
            else:
                exec getKeyValue(key, 'teacher')
        teacher.title = teacher.firstname    
        print teacher.profile_photo
        if teacher.profile_photo[0].get().file and not BrochureFileTypeSupported(blobstore.BlobInfo(teacher.profile_photo[0].get().file).content_type):
            sent_status = 'NO'
            message="Unsupported file format"
        else:
            try:
                teacher.put()
                sent_status='YES'
                message="Event updated successfully"
            except:
                sent_status="NO"
                message="Could not upload the Event. One of the reason could be  the database is not running or internet connection is lost."
               
        self.redirect('/Siteadmin/CreateTeacher?title='+ teacher.title+ '&sent_status='+ sent_status + '&msg=' + message)


############### Photos Upload  ###############
class CreateUpload(webapp2.RequestHandler):
    def get(self):
        template_values = {
                           'page':"Siteadmin",
                        }
        template_values.update(parseSentStatus(self))
        user = users.get_current_user()
        template_values['name'] =  user.nickname()
        if user and users.is_current_user_admin():
            template_values['logout_url'] = users.create_logout_url('/Login') # redirecting to Login Page After successfull logout.
            template_values['upload_url'] = blobstore.create_upload_url('/Siteadmin/SubmitWebpage') # default upload url for blob store.
            self.response.out.write(template.render(gettemplate('CreateUpload'), template_values))
        else:
            template_values['logout_url'] = users.create_logout_url('/Login')
            self.response.out.write(template.render(gettemplate('Login'), template_values))


class SubmitHomePagePhotos(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        photos = HomePagePhoto() # creating blank object of HomePagePhoto data model
        #photoscount = HomePagePhoto.query().count()     
        if len(self.get_uploads('file')) > 0: # getting all the uploads from the form field 'file'
            photos.file = self.get_uploads('file')[0].key()
            photos.rank = 0
            photos.put()
            
        sent_status='YES'
        message="Successfull : Photo update"
        self.redirect('/Siteadmin/CreateUpload?title='+photos.file +'&sent_status='+sent_status+'&msg='+message)

