#GAE modules
import webapp2

#Application specific Modules
from Home import HomeView
from About import AboutView
from Courses import CoursesView
from Teachers import TeachersView
from Events import EventsView
from Contact import ContactView
from Siteadmin import SiteadminView

"""
List of Links.
Each html file or  href link should be listed here.
"""
config = {}
config["webapp2_extras.sessions"] = {
    "secret_key": "key",
}    
application = webapp2.WSGIApplication(
                                      [('/', HomeView.Home),
                                       ('/Home', HomeView.Home),
                                       ('/About', AboutView.About),
                                       ('/Courses', CoursesView.Courses),
                                       ('/Teachers', TeachersView.Teachers),
                                       ('/Events', EventsView.Events),
                                       ('/Contact', ContactView.Contact),
                                       ('/SubmitMessage', ContactView.SubmitMessage),
                                       
                                       ('/Siteadmin', SiteadminView.Siteadmin),
                                       
                                       ('/Login', SiteadminView.Login),
                                       
                                       ('/Login/SubmitRequest', SiteadminView.SubmitRequest),
                                       
                                       ('/Siteadmin/CreateHoliday', SiteadminView.CreateHoliday),
                                       ('/Siteadmin/SubmitHoliday', SiteadminView.SubmitHoliday),
                                       
                                       ('/Siteadmin/CreateEvent', SiteadminView.CreateEvent),
                                       ('/Siteadmin/SubmitEvent', SiteadminView.SubmitEvent),
                                       
                                       ('/Siteadmin/CreateTeacher', SiteadminView.CreateTeacher),
                                       ('/Siteadmin/SubmitTeacher', SiteadminView.SubmitTeacher),
                                       
                                       ('/Siteadmin/CreateUpload', SiteadminView.CreateUpload),
                                       ('/Siteadmin/SubmitHomePagePhotos', SiteadminView.SubmitHomePagePhotos),
                                       
                                       ('/images/([^/]+)?', EventsView.ImageHandler),
                                       ('/homephotos/([^/]+)?', HomeView.HomeImageHandler),
                                       
                                       ],
                                      config = config,
                                      debug=True)
