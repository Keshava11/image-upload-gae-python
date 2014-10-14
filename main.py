import webapp2
from google.appengine.ext import ndb
from google.appengine.api import images
import mimetypes
import logging


HTML_POST_PAGE = \
"""
<!DOCTYPE HTML>
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Image Upload</title>
</head>
<body>
<form action="/file_upload" enctype="multipart/form-data" method="post">
    <div><input type="file" name="file"/></div>
    <div><input type="submit" value="Upload"></div>
   
</form>
</body>
</html>
"""


#Hardcoded value for Key name
email_id = "ryan@gmail.com"

#Updated Image Upload
class MyUser(ndb.Model):
    file_name = ndb.StringProperty()
    blob = ndb.BlobProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(HTML_POST_PAGE)

#Handler for image upload
class FileUpload(webapp2.RequestHandler):
    def post(self):
            #Creating entity with fixed id
            my_user = MyUser(id=email_id)

            #Below lines to be added in the main code to put image in datastore
            file_upload = self.request.POST.get("file", None)
            file_name = file_upload.filename
            my_user.file_name = file_name

            #For default version of the image
            my_user.blob = file_upload.file.read()
            my_user.put()

            #Navigating to other page to read image
            self.redirect('/multi_serve')


#Handler to read image into the <img> tag in the OUTPUT_HTML_PAGE 
class DynamicImageServe(webapp2.RequestHandler):
    def get(self):
        oldUser = MyUser.get_by_id(self.request.get('img_id'))
        if oldUser.blob:
            # Updating content type for all
            self.response.headers['Content-Type'] = 'image/*'
            self.response.out.write(oldUser.blob)
        else:
            self.response.out.write('No image')


#Handler for writing multiple images in the response
class MultipleImageServe(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<div><img src="/dyimg_serve?img_id=%s"></img></div>' % email_id)
        self.response.out.write('<div><img src="/dyimg_serve?img_id=%s"></img></div>' % email_id)
        

application = webapp2.WSGIApplication([('/',MainPage ),('/file_upload',FileUpload),('/dyimg_serve',DynamicImageServe),('/multi_serve',MultipleImageServe),], debug=True)         
