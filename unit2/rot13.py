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
import cgi

rot13form = """
<!DOCTYPE html>

<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""
class ROT13(webapp2.RequestHandler):
    def write_form(self, txt=""):
        txt = cgi.escape(txt, quote = True)
        self.response.out.write(rot13form %txt)
        
    def post(self):
        txt = self.request.get("text")
        if txt:
            res= []
            for i in range(0,len(txt)):
                o_val=ord(txt[i])
                if o_val>=65 and o_val<=90:
                    o_val += 13
                    if o_val>90:
                        o_val = 65 + (o_val-90-1)
                if o_val>=97 and o_val<=122:
                    o_val += 13
                    if o_val>122:
                        o_val = 97 + (o_val-122-1)
                res.append(chr(o_val))
            txt = ''.join(res)
        self.write_form(txt)
        
    def get(self):
        self.write_form()

        
