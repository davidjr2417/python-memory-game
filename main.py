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
import os
import MySQLdb 
# pip install MySQL-python, sudo pip install mysql-connector,sudo pip install --user jupyterlab
import jinja2
import webapp2


from google.appengine.ext import db
import gc
from MySQLdb import *

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader =jinja2.FileSystemLoader(template_dir))

class Handler (webapp2.RequestHandler):
	def write (self, *a, **kw):
 		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))



def connection():
    # Edited out actual values
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="root",
                           db = "users")
    c = conn.cursor()

    return c, conn

class User(db.Model):
	name = db.StringProperty(required=True)
	email = db.EmailProperty(required=True)
	created = db.DateTimeProperty(auto_now_add = True)

class MainHandler(Handler):
    def get(self):
        self.render('index.html')





class Login(Handler):
	def render_login(self, name="",email="", error=""):
		# users = db.GqlQuery(
		# "Select * From User "
		# "ORDER BY created DESC")
		c, conn = connection()
		query = "Select * from users.account"
		c.execute(query)
		users = c.fetchall()
		conn.close()
		# return users
		self.render('login.html', name=name, email=email, error=error, users=users)

	def get(self):
		self.render_login() 

	def post(self):
		name = self.request.get("name")
		email = self.request.get("email")
		error=""
		if name and email:
			user = User(name =name, email = email)
			user.put()
			self.render_login(name, email, error)
		else:
			error = "no name or email"
			self.render_login("", "", error)



class Game (Handler):
    def get(self):
        self.render('matching_game.html')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login.html', Login),
    ('/matching_game.html', Game)
], debug=True)








# #!/usr/bin/env python
# #
# # Copyright 2007 Google Inc.
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.
# #
# import os
# import jinja2

# import webapp2

# template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# jinja_env = jinja2.Environment(loader =jinja2.FileSystemLoader(template_dir))


# class Handler (webapp2.RequestHandler):
# 	def write(self, *a, **kw):
# 	 		self.response.out.write(*a, **kw)

# 	def render_str(self, template, **params):
# 		t = jinja_env.get_template(template)
# 		return t.render(params)

# 	def render(self, template, **kw):
# 		self.write(self.render_str(template, **kw))




# class MainPage(Handler):
#     def get(self):
#         self.render("index.html")



# app = webapp2.WSGIApplication([
#     ('/', MainPage)
# ], debug=True)

