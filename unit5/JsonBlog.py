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
import json
from google.appengine.ext import db

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '.')))
    
class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    cdate = db.DateTimeProperty(auto_now_add=True)
    
class JBlog(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('/templates/json_blog.htm')
        b = db.GqlQuery("SELECT * FROM Post ORDER BY cdate DESC limit 10")
        self.response.out.write(template.render({'blogs':b}))
        
class JBlogJSON(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "application/json"
        json_list = []
        blog_entries = db.GqlQuery("SELECT * FROM Post ORDER BY cdate DESC limit 10")
        for entry in blog_entries:
            json_list.append({'content':entry.content,'subject':entry.subject,'created':entry.cdate.strftime("%A %d %B %Y")})
        self.response.out.write(json.dumps(json_list))

class JNewPost(webapp2.RequestHandler):
    def my_renderer(self, error="",subject="",content=""):
        template = jinja_environment.get_template('/templates/new_post.htm')
        self.response.out.write(template.render({'errormsg':error,'subject':subject,'content':content}))
        
    def get(self):
        self.my_renderer()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")
        if subject and content:
            p = Post(subject=subject,content=content)
            p.put()
            id = p.key().id()
            self.redirect("/unit5/blog/" + str(id))
        else:
            self.my_renderer("Both Subject and Content are mandatory",subject,content)
            
class JSinglePost(webapp2.RequestHandler):
    def get(self, post_id):
        post = Post.get_by_id(int(post_id)) 
        template = jinja_environment.get_template('/templates/single_post.htm')
        self.response.out.write(template.render({'x':post}))
        
class JSinglePostJSON(webapp2.RequestHandler):
    def get(self, post_id):
        self.response.headers['Content-Type'] = "application/json"
        entry = Post.get_by_id(int(post_id))
        json_post = {}
        if entry:
            json_post['content']=entry.content
            json_post['subject']=entry.subject
            json_post['created']=entry.cdate.strftime("%A %d %B %Y")
        self.response.out.write(json.dumps(json_post))
