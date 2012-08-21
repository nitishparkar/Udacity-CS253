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
import re

signupform= """
<!DOCTYPE html>
<html>
  <head>
    <title>Unit 2 Signup Form</title>
  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <label>Username
          <input type="text" name="username" value="%(unvalue)s"><span style="color: red">%(unerror)s</span>
      </label>
      <br>
      <label>Password
          <input type="password" name="password" value=""><span style="color: red">%(pwerror)s</span>
      </label>
      <br>
      <label>Verify Password
          <input type="password" name="verify" value=""><span style="color: red">%(vererror)s</span>
      </label>
      <br>
      <label>Email (optional)
          <input type="text" name="email" value="%(emvalue)s"><span style="color: red">%(emailerror)s</span>
      </label>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""


welcomeform = """
<!DOCTYPE html>

<html>
  <head>
    <title>Unit 2 Welcome</title>
  </head>

  <body>
    <h2>Welcome, %s!</h2>
  </body>

</html>
"""

class Welcome(webapp2.RequestHandler):
    def get(self):
        un = self.request.get("username")
        self.response.out.write(welcomeform %un)

class SignUp(webapp2.RequestHandler):
    def write_form(self, usn="",eml="",un="", pw="", vp="", em=""):    
        self.response.out.write(signupform %{'unvalue':usn, 'emvalue':eml,'unerror':un,'pwerror':pw,'vererror':vp,'emailerror':em})
        
    def post(self):
        un = self.request.get("username")
        pw = self.request.get("password")
        vp = self.request.get("verify")
        em = self.request.get("email")
        
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        unb=USER_RE.match(un)
        unerror=""
        if not unb:
            unerror="That's not a valid username."
        
        PASSWD_RE = re.compile(r"^.{3,20}$")
        pwb=PASSWD_RE.match(pw)
        pwerror=""
        if not pwb:
            pwerror="That wasn't a valid password."
        
        vperror=""
        vpb=True
        if pwb:
            if pw != vp:
                vpb=False
                vperror="Your passwords didn't match."
        
        emerror=""
        emb=True
        if em:
            EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
            emb=EMAIL_RE.match(em)
            if not emb:
                emerror="That's not a valid email."
        
        if unb and pwb and vpb and emb:
            self.redirect("/unit2/welcome?username=%s" %un)
        else:
            self.write_form(un, em, unerror, pwerror, vperror, emerror)

    def get(self):
        self.write_form()
        
