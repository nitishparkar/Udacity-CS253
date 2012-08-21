import webapp2
import jinja2
import os
from google.appengine.ext import db

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '.')))
    
class Blog(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('blogtemplate.htm')
        b = db.GqlQuery("SELECT * FROM Post ORDER BY cdate DESC limit 10")
        self.response.out.write(template.render({'blogs':b}))