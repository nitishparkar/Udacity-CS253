#!/usr/bin/env python

import webapp2
import os
import jinja2
import urllib2
import logging
import time
from xml.dom import minidom
from google.appengine.ext import db
from google.appengine.api import memcache

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), './templates/')))


class GMAArt(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    cdate = db.DateTimeProperty(auto_now_add=True)
    cords = db.GeoPtProperty()
    ip = db.StringProperty()


class CachedChan(webapp2.RequestHandler):
    def getArts(self, update=False):
        arts_list = memcache.get('front_page')
        if not arts_list or update:
            arts = db.GqlQuery("SELECT * FROM GMAArt ORDER BY cdate DESC")
            logging.error("DB read")
            arts_list = list(arts)
            memcache.set('front_page', arts_list)
            memcache.set('last_updated', time.time())
        return arts_list

    def myRenderer(self, error="",title="",art="",secs="0"):
        template = jinja_environment.get_template('cached_ascii_chan.htm')
        arts_list = self.getArts()        
        map_string = "http://maps.googleapis.com/maps/api/staticmap?&size=400x300&sensor=false"
        for x in arts_list:
            if x.cords:
                map_string += '&markers=%s' %(x.cords)
        t = memcache.get('last_updated')
        if t:
            secs = time.time() - t
            secs = str(int(secs)) 
        self.response.out.write(template.render({'errormsg':error,'title':title,'art':art,'arts':arts_list,'location_map':map_string,'secs':secs}))
        
    def get(self):
        self.myRenderer()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        user_ip = self.request.remote_addr
        #user_ip = "12.215.42.19"
        lat = None
        lon = None
        if user_ip:
            try:
                content = urllib2.urlopen('http://api.hostip.info/?ip='+user_ip).read()
                parsed_xml = minidom.parseString(content)
                coordinates = parsed_xml.getElementsByTagName('gml:coordinates')
                if coordinates:
                    lon, lat = coordinates[0].firstChild.nodeValue.split(',')
            except BaseException:
                pass
        if title and art:
            a = GMAArt(title=title,art=art)
            if user_ip:
                a.ip = user_ip
            if lat and lon:
                a.cords=lat+','+lon
            a.put()
            self.getArts(True)
            self.redirect("/unit6/machan")
        else:
            self.myRenderer("Both Title and Art are mandatory",title,art)
