#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2

from google.appengine.ext import db

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '.')))
    
class AArt(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    cdate = db.DateTimeProperty(auto_now_add=True)

class AChan(webapp2.RequestHandler):
    def my_renderer(self, error="",title="",art=""):
        template = jinja_environment.get_template('actemplate.htm')
        arts = db.GqlQuery("SELECT * FROM AArt ORDER BY cdate DESC")
        self.response.out.write(template.render({'errormsg':error,'title':title,'art':art,'arts':arts}))
        
    def get(self):
        self.my_renderer()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        if title and art:
            a = AArt(title=title,art=art)
            a.put()
            self.redirect("/unit3/achan")
        else:
            self.my_renderer("Both Title and Art are mandatory",title,art)
