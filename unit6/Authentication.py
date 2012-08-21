#!/usr/bin/env python

import webapp2
import jinja2
import os
import re
import hashlib
from google.appengine.ext import db
import random
import string
import hmac

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), './templates')))
    

class Users(db.Model):
    username = db.StringProperty(required= True)
    password = db.StringProperty(required= True)
    saltval = db.StringProperty(required = True)
    email_id = db.StringProperty(required = False)
    
    
class U6SignUp(webapp2.RequestHandler):
    def my_renderer(self, **params):
        template = jinja_environment.get_template('sign_up.htm')
        self.response.out.write(template.render(params))
        
    def get(self):
        self.my_renderer()
        
    def create_salt(self):
        return ''.join(random.choice(string.letters) for x in xrange(5))

    def create_hash(self, name, pwd, salt):
        return hashlib.sha256(name+pwd+salt).hexdigest()
    
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
        else:
            u = db.GqlQuery("SELECT * FROM Users WHERE username=:1", un)
            if u.get():
                unb = False
                unerror="Username already exists"
        
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
            slt = self.create_salt()
            pw = hmac.new(slt,pw).hexdigest()
            nu = Users(username=un,password=pw,saltval=slt,email_id=em)
            nu.put()
            uid= nu.key().id()
            hsh = self.create_hash(un, pw, slt)
            cookie_hash = str(uid) +':'+hsh
            self.response.headers.add_header('Set-Cookie', 'user_id=%s;  Path=/' %cookie_hash)
            self.redirect("/unit6/blog/welcome")
        else:
            self.my_renderer(unvalue=un, emvalue=em, unerror=unerror, pwerror=pwerror, vererror=vperror, emailerror=emerror)


class U6Welcome(webapp2.RequestHandler):
    def verify_hash(self, hsh, u, p, s):
        if hsh == hashlib.sha256(u+p+s).hexdigest():
            return True
        else:
            return False
        
    def get(self):
        cook = self.request.cookies.get('user_id')
        if cook:
            csplit = cook.split(':')
            uid=csplit[0]
            hash=csplit[1]
            usr = Users.get_by_id(int(uid))
            if usr and self.verify_hash(hash, usr.username, usr.password, usr.saltval):
                self.response.out.write("Welcome, %s!" %usr.username)
            else:
                self.redirect('/unit6/blog/signup')
        else:
            self.redirect('/unit6/blog/signup')
    

class U6Login(webapp2.RequestHandler):
    def my_renderer(self,error1=""):
        template = jinja_environment.get_template('sign_in.htm')
        self.response.out.write(template.render({'errormsg':error1}))
        
    def get(self):
        self.my_renderer()
        
    def post(self):
        un = self.request.get('username')
        pw = self.request.get('password')
        if un and pw:
            q = db.GqlQuery("SELECT * FROM Users WHERE username='%s'" %un)
            qs = q.get()
            if qs:
                usrid = qs.key().id()
                dbpw = qs.password
                salt = qs.saltval
                newpw = hmac.new(str(salt), str(pw)).hexdigest()
                if dbpw == newpw:
                    hsh = hashlib.sha256(un+newpw+salt).hexdigest()
                    self.response.headers.add_header('Set-Cookie', 'user_id=%s:%s;  Path=/' %(str(usrid),hsh))
                    self.redirect("/unit6/blog/welcome")
        
        self.my_renderer("Invalid Login!")
            
    
class U6Logout(webapp2.RequestHandler):
    def get(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=;  Path=/')
        self.redirect('/unit6/blog/signup')    
