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
from unit2.signup import *
from unit2.rot13 import *
from unit3.achan import *
from unit3.blog import *
from unit3.newpost import *
from unit4.unit4 import *
from unit5.acloc import *
from unit5.JsonBlog import *
from unit5.Authentication import *
from unit6.AsciiChan import *
from unit6.CachedBlog import *
from unit6.Authentication import *
from final.Wiki import *

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), '.')))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello, Udacity!')
        #self.response.out.write(welcomeform)


class UnexpectedErrorHandler(webapp2.RequestHandler):
    def get(self):
        msg = self.request.get('message')
        self.response.out.write('Error message: '+ msg)


class Custom404(webapp2.RequestHandler):
    def get(self, path):
        self.response.status_int = 404
        template = jinja_environment.get_template('/404/index.htm')
        self.response.out.write(template.render())


WIKI_ROOT = r'(/final/(?:[a-zA-Z0-9_-]+/?)*)'
PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'
app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/unit2/rot13', ROT13),
                               ('/unit2/signup', SignUp),
                               ('/unit2/welcome', Welcome),
                               ('/unit3/achan', AChan),
                               ('/unit3/blog', Blog),
                               ('/unit3/blog/newpost', NewPost),
                               (r'/unit3/blog/(\d+)', SinglePost),
                               ('/unit4/signup', U4SignUp),
                               ('/unit4/welcome', U4Welcome),
                               ('/unit4/login', U4Login),
                               ('/unit4/logout', U4Logout),
                               ('/unit5/gachan', AChanGMaps),
                               ('/unit5/blog/signup', U5SignUp),
                               ('/unit5/blog/login', U5Login),
                               ('/unit5/blog/logout', U5Logout),
                               ('/unit5/blog/welcome', U5Welcome),
                               ('/unit5/blog', JBlog),
                               ('/unit5/blog/.json', JBlogJSON),
                               ('/unit5/blog/newpost', JNewPost),
                               (r'/unit5/blog/(\d+)', JSinglePost),
                               (r'/unit5/blog/(\d+).json', JSinglePostJSON),
                               ('/unit6/machan', CachedChan),
                               ('/unit6/blog/signup', U6SignUp),
                               ('/unit6/blog/login', U6Login),
                               ('/unit6/blog/logout', U6Logout),
                               ('/unit6/blog/welcome', U6Welcome),
                               ('/unit6/blog', CBlog),
                               ('/unit6/blog/newpost', CNewPost),
                               (r'/unit6/blog/(\d+)', CSinglePost),
                               ('/unit6/blog/flush', CFlush),

                               ('/final/', WikiHandler),
                               ('/final/signup', SignupHandler),
                               ('/final/login', LoginHandler),
                               ('/final/logout', LogoutHandler),
                               ('/final/_edit' + PAGE_RE, EditHandler),
                               ('/final/_history' + PAGE_RE, HistoryHandler),
                               (WIKI_ROOT, ViewHandler),

                               ('/error', UnexpectedErrorHandler),
                               ('/(.+)', Custom404)], 
                               debug=True)

                              