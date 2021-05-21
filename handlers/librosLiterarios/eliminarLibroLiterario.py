import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.libroLiterario import libroLiterario


class EliminarlibroLiterarioHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
                try:
                    id_libroLiterario = self.request.GET["id_libroLiterario"]
                except:
                    id_libroLiterario = "ERROR"
                libroLiterario = ndb.Key(urlsafe=id_libroLiterario).get()
                sust = {
                    "libroLiterario" : libroLiterario
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("librosLiterarios/eliminarLibroLiterario.html", **sust))
        else:
            self.redirect("/")
            return

    def post(self):
        user = users.get_current_user()

        if user:
                id_libroLiterario = self.request.get("edIdLibroLiterario", "ERROR")
                libroLiterario = ndb.Key(urlsafe=id_libroLiterario).get()
                url = "/listarLibrosLiterarios"
                mensaje = "El libro: "+libroLiterario.titulo+" ha sido eliminado con exito"
                libroLiterario.key.delete()
                sust = {
                    "mensaje": mensaje,
                    "url": url
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("mensajeConfirmacion.html", **sust))
        else:
            self.redirect("/")
            return

app = webapp2.WSGIApplication([
    ('/eliminarLibroLiterario', EliminarlibroLiterarioHandler),
], debug=True)