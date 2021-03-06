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
from google.appengine.ext import ndb
from google.appengine.api import users
import jinja2
JINJA_ENVIRONMENT = jinja2.Environment(
     loader=jinja2.FileSystemLoader(searchpath="./templates"))

class User(ndb.Model):
     id_user = ndb.StringProperty(required=True)
     name = ndb.StringProperty(required=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect("/paginaPrincipal")
            return
        else:
            labels = {
                "user_login": users.create_login_url("/")
            }
            template = JINJA_ENVIRONMENT.get_template("index.html")
            self.response.write(template.render(labels))


app = webapp2.WSGIApplication([
 ('/', MainHandler)
], debug=True)
