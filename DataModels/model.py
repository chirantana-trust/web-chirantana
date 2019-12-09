from google.appengine.ext import ndb


class Requests(ndb.Model):
    request = ndb.StringProperty(required=True) # Admin, Teacher, Student, Trustee etc...
    mygroup = ndb.StringProperty()
    email = ndb.StringProperty() #
    
    description = ndb.TextProperty()
    
    
    
class Uploads(ndb.Model):
    ''' 
    Native tags like, HomePage, Event, TeachersPage, Profile, etc...
    There can be custom tags also. (to be done)
    '''
    tag = ndb.StringProperty()
    file = ndb.BlobKeyProperty()
    

class WebPagePhotos(ndb.Model): 
    title = ndb.StringProperty(required=True) # 
    photos = ndb.KeyProperty(kind='Uploads', repeated=True)
    
class DateTime(ndb.Model):
    title = ndb.StringProperty(required=True) #  sdt(Start Date Time), edt(End Date Time), odt(On Date Time)
    date_time = ndb.DateTimeProperty()

class Date(ndb.Model):
    title = ndb.StringProperty(required=True) #day
    date = ndb.DateProperty()

class HalfDay(ndb.Model):
    title = ndb.StringProperty(required=True) # fh(First Half), sh(Second Half)
    date = ndb.DateProperty()
    
    
class Event(ndb.Model):
    title = ndb.StringProperty(required=True) # short title of the event
    
    # cultural, seminar, show, sport, social, meeting, functions
    category = ndb.StringProperty(required=True) 
    
    #  For a day or range of days with time or for single day with just few hours. 
    dateTime = ndb.KeyProperty(kind='DateTime', repeated=True)
    
    sdt = ndb.DateTimeProperty();
    edt = ndb.DateTimeProperty();
     
    venue = ndb.TextProperty()
    
    description = ndb.TextProperty()
    
    created_on=ndb.DateTimeProperty(auto_now_add=True)
    updated_on=ndb.DateTimeProperty(auto_now=True)
  
    #link to brochures
    brochure = ndb.KeyProperty(kind='Uploads', repeated=True)


    
class Holiday(ndb.Model):
    title = ndb.StringProperty(required=True) #  reason for holiday
    
    #govt, private,
    category = ndb.StringProperty(required=True)
    
    # Just date
    fullday = ndb.KeyProperty(kind='Date')
    
    # fh or sh with date
    halfday = ndb.KeyProperty(kind='DateTime')
    
    # range of days  for summer holidays etc...
    daterange = ndb.KeyProperty(kind='Date', repeated=True)
    
    description = ndb.TextProperty()
    
    
    
class UserType(ndb.Model):
    user_type = ndb.StringProperty()    
    
class Teacher(ndb.Model):
    basic_details = ndb.KeyProperty(kind='UserBasicDetails')
    pass
class Trustee(ndb.Model):
    basic_details = ndb.KeyProperty(kind='UserBasicDetails')
    pass
class Student(ndb.Model):
    basic_details = ndb.KeyProperty(kind='UserBasicDetails')
    pass
class Parent(ndb.Model):
    basic_details = ndb.KeyProperty(kind='UserBasicDetails')
    pass
class Admin(ndb.Model):
    basic_details = ndb.KeyProperty(kind='UserBasicDetails')
    pass

class Address(ndb.Model):
    address = ndb.StringProperty()
    city_district = ndb.StringProperty()
    locality = ndb.StringProperty()
    pincode = ndb.IntegerProperty()
    state = ndb.StringProperty()
    Country = ndb.StringProperty()
 
class PhoneEmail(ndb.Model):
    landline = ndb.StringProperty()
    mobile = ndb.StringProperty()
    altNumber = ndb.StringProperty()
    email = ndb.StringProperty()

class ExtraDetails(ndb.Model):
    '''
    This model includes all the details required for BEO office.
    This model can have  reference to teachers resume.
    Student details like caste, religion etc...
    Yet to be done..
    '''
    pass


class UserBasicDetails(ndb.Model):
    '''
    
    This includes basic details like, full name and user photo and contact details
    This is common for  any user.  So This will becomes the parent entity
    This parent entity has 1:1 mapping for address and userID.
    User ID may not be present for all users. only requested user will get access.
    Only students, teachers  and trustee will have user IDs. 
    Parents can access the details  from the  student ID.
    
    '''
    id = ndb.IntegerProperty()
    prefix = ndb.StringProperty()
    firstname = ndb.StringProperty(required=True)
    middlename =  ndb.StringProperty()
    lastname = ndb.StringProperty()
    photo = ndb.BlobProperty()
    
    userID = ndb.StringProperty(required=True)
    password =  ndb.StringProperty(required=True)

    user_type = ndb.KeyProperty(kind='UserType')
    
    current_address =  ndb.KeyProperty(kind='Address')
    perm_address = ndb.KeyProperty(kind='Address')
    phone_email = ndb.KeyProperty(kind='PhoneEmail')
    extra_details = ndb.KeyProperty(kind='ExtraDetails')


    
    
    
