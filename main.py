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
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
</head>
<body>
    <h1>User Signup</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

def build_page(user_error="", password_error="", verify_error="", email_error="", username="", email=""):


    username_label = "<label>Username</label>"
    username_input = "<input type='text' name='username' value='" + username+ "'/ >"

    password_label = "<label>Password</label>"
    password_input = "<input type='password' name='password'/>"

    verify_label = "<label>Verify Password</label>"
    verify_input = "<input type='password' name='verify'/>"

    email_label = "<label>Email (optional)</label>"
    email_input = "<input type='text' name='email' value ='"+ email + "'/>"

    submit = "<input type='submit'/>"

    form = "<form action='/' method='post'>" + username_label + username_input + user_error + "<br>" + password_label + password_input + password_error + "<br>" + verify_label + verify_input + verify_error + "<br>" + email_label + email_input + email_error + "<br>" + submit + "</form>"

    header = "<h2>Signup</h2>"

    return page_header + header + form + page_footer




class MainHandler(webapp2.RequestHandler):

    def get(self):
        content = build_page("")

        self.response.write(content)

    def post(self):
        USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        def valid_username(username):
            return username and USER_RE.match(username)

        PASSWORD_RE = re.compile(r"^.{3,20}$")
        def valid_password(password):
            return password and PASSWORD_RE.match(password)

        EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
        def valid_email(email):
            return not email or EMAIL_RE.match(email)

        error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        user_error = ""
        password_error = ""
        verify_error = ""
        email_error = ""

        if not valid_username(username):
            error = True
            user_error = "That username isn't valid"

        if not valid_password(password):
            error = True
            password_error = "That password isn't valid"
        elif password != verify:
            error = True
            verify_error = "Password does not match"

        if not valid_email(email):
            error = True
            email_error = "That email is invalid"

        if error:
            #rerender the page with the username and email, if they were typed

            content = build_page(user_error=user_error, password_error=password_error, verify_error=verify_error,
            email_error=email_error, username=username, email=email)
            self.response.write(content)
        else:
            self.redirect('/thanks?username=' + username)



class ThanksHandler(webapp2.RequestHandler):

    def get(self):
        user = self.request.get("username")
        escaped_user = cgi.escape(user) #escapes content
        page = page_header + "Thanks for signing up, " + escaped_user + page_footer
        self.response.write(page) #prints content to page

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks', ThanksHandler)
], debug=True)
