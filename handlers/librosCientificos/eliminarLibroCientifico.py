import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.libroCientifico import libroCientifico


class EliminarlibroCientificoHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
                try:
                    id_libroCientifico = self.request.GET["id_libroCientifico"]
                except:
                    id_libroCientifico = "ERROR"
                libroCientifico = ndb.Key(urlsafe=id_libroCientifico).get()
                sust = {
                    "libroCientifico" : libroCientifico
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("librosCientificos/eliminarLibroCientifico.html", **sust))
        else:
            self.redirect("/")
            return

    def post(self):
        user = users.get_current_user()

        if user:
                id_libroCientifico = self.request.get("edIdLibroCientifico", "ERROR")
                libroCientifico = ndb.Key(urlsafe=id_libroCientifico).get()
                url = "/listarLibrosCientificos"
                mensaje = "El libro: "+libroCientifico.titulo+" ha sido eliminado con exito"
                libroCientifico.key.delete()
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
    ('/eliminarLibroCientifico', EliminarlibroCientificoHandler),
], debug=True)