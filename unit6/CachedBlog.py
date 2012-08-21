#!/usr/bin/env python

import webapp2
import os
import jinja2
import json
import time
from google.appengine.api import memcache
from google.appengine.ext import db

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '.')))

    
class Post(db.Model):
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    cdate = db.DateTimeProperty(auto_now_add=True)

    
class CBlog(webapp2.RequestHandler):
    def get_blogs(self, update=False):
        blogs = memcache.get('blogs_front')
        if not blogs or update:
            b = db.GqlQuery("SELECT * FROM Post ORDER BY cdate DESC limit 10")
            blogs = list(b)
            memcache.set('blogs_front', blogs)
            memcache.set('last_updated', time.time())
        return blogs
    
    def get(self):
        template = jinja_environment.get_template('/templates/cached_blog.htm')
        b = self.get_blogs()
        t = memcache.get('last_updated')
        s = 0
        if t:
            s = int(time.time() - t)
        self.response.out.write(template.render({'blogs':b, 'secs':s}))

"""        
class CBlogJSON(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "application/json"
        json_list = []
        blog_entries = db.GqlQuery("SELECT * FROM Post ORDER BY cdate DESC limit 10")
        for entry in blog_entries:
            json_list.append({'content':entry.content,'subject':entry.subject,'created':entry.cdate.strftime("%A %d %B %Y")})
        self.response.out.write(json.dumps(json_list))
"""


class CNewPost(webapp2.RequestHandler):
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
            cb = CBlog()
            cb.get_blogs(True)
            self.redirect("/unit6/blog/" + str(id))
        else:
            self.my_renderer("Both Subject and Content are mandatory",subject,content)


class CSinglePost(webapp2.RequestHandler):
    def get(self, post_id):
        s = 0
        post = memcache.get(post_id)
        if not post:
            post = Post.get_by_id(int(post_id)) 
            memcache.set(post_id,post)
            memcache.set("T"+post_id,time.time())
        else:
            t = memcache.get("T"+post_id)
            if t:
                s = int(time.time() - t)
        template = jinja_environment.get_template('/templates/cached_single_post.htm')
        self.response.out.write(template.render({'x':post,'secs':s}))

"""        
class CSinglePostJSON(webapp2.RequestHandler):
    def get(self, post_id):
        self.response.headers['Content-Type'] = "application/json"
        entry = Post.get_by_id(int(post_id))
        json_post = {}
        if entry:
            json_post['content']=entry.content
            json_post['subject']=entry.subject
            json_post['created']=entry.cdate.strftime("%A %d %B %Y")
        self.response.out.write(json.dumps(json_post))
"""


class CFlush(webapp2.RequestHandler):
    def get(self):
        flushed = memcache.flush_all()
        if flushed:
            self.redirect('/unit6/blog')
        else:
            self.redirect('/error?message=Memcache flush failed!')