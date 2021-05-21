import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users


class PaginaPrincipalHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
                user_name = user.nickname()
                sust = {
                    "user_name": user_name,
                    "user_logout": users.create_logout_url("/")
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("paginaPrincipal.html", **sust))
        else:
            self.redirect("/")
            return


app = webapp2.WSGIApplication([
    ('/paginaPrincipal', PaginaPrincipalHandler),
], debug=True)
