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
import urllib2
from xml.dom import minidom
from google.appengine.ext import db

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), './templates/')))
    
class GMAArt(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    cdate = db.DateTimeProperty(auto_now_add=True)
    cords=db.GeoPtProperty()
    ip=db.StringProperty()

class AChanGMaps(webapp2.RequestHandler):
    def my_renderer(self, error="",title="",art=""):
        template = jinja_environment.get_template('ascii_chan_maps.htm')
        arts = db.GqlQuery("SELECT * FROM GMAArt ORDER BY cdate DESC")
        arts_list = list(arts)
        map_string = "http://maps.googleapis.com/maps/api/staticmap?&size=400x300&sensor=false"
        for x in arts_list:
            if x.cords:
                map_string += '&markers=%s' %(x.cords)
        self.response.out.write(template.render({'errormsg':error,'title':title,'art':art,'arts':arts_list,'location_map':map_string}))
        
    def get(self):
        self.my_renderer()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        user_ip = self.request.remote_addr
        #user_ip = "12.215.42.19"
        lat = None
        lon = None
        if user_ip:
            content = urllib2.urlopen('http://api.hostip.info/?ip='+user_ip).read()
            parsed_xml = minidom.parseString(content)
            coordinates = parsed_xml.getElementsByTagName('gml:coordinates')
            if coordinates:
                lon, lat = coordinates[0].firstChild.nodeValue.split(',')
        #self.debug_write("latlon"+coordinates[0].firstChild.nodeValue)
        if title and art:
            a = GMAArt(title=title,art=art)
            if user_ip:
                a.ip = user_ip
            if lat and lon:
                a.cords=lat+','+lon
            a.put()
            self.redirect("/unit5/gachan")
        else:
            self.my_renderer("Both Title and Art are mandatory",title,art)
