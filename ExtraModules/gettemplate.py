import os
from settings import rootPath

class custom:
    def __init__(self):
        self.data = {
                    'msg_sent_status':False
                    }
TEMPLATE_BASE_PATH = os.path.join(rootPath(), "static_asset", "templates")

htmls = {
         
        'Home':'site/index.html',
        'About': 'site/about.html',
        'Courses': 'site/courses.html',
        'Teachers':'site/teachers.html',
        'Events':'site/events.html',
        'Contact': 'site/contact.html',
        'Siteadmin':'site/siteadmin.html',
        'Login':'site/login.html',
        'CreateEvent': 'site/submit_event.html',
        'CreateHoliday': 'site/submit_holiday.html',
        'CreateUpload':'site/submit_upload.html',
        'CreateTeacher':'site/submit_teacher.html',
    }

def gettemplate(page):
    return os.path.join(TEMPLATE_BASE_PATH, htmls[page])