import webapp2
from webapp2_extras import jinja2
from google.appengine.ext import ndb
from model.libroCientifico import libroCientifico
from google.appengine.api import users


class EditarLibroCientificoHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            try:
                id_libroCientifico = self.request.GET["id_libroCientifico"]
            except:
                id_libroCientifico = "ERROR"
            libroCientifico = ndb.Key(urlsafe=id_libroCientifico).get()
            sust = {
                "libroCientifico": libroCientifico
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(
                jinja.render_template("librosCientificos/editarLibroCientifico.html", **sust)
            )
        else:
            self.redirect("/")
            return

    def post(self):
        # Recupera del formulario
        titulo = self.request.get("edTitulo", "ERROR")
        autor = self.request.get("edAutor", "ERROR")
        campo = self.request.get("edCampo", "ERROR")

        id_libroCientifico = self.request.get("edIdLibroCientifico", "ERROR")

        # Guarda los datos
        libroCientifico = ndb.Key(urlsafe=id_libroCientifico).get()
        libroCientifico.titulo=titulo
        libroCientifico.autor = autor
        libroCientifico.campo = campo
        libroCientifico.put()

        url = "/verLibroCientifico?id_libroCientifico=" + libroCientifico.key.urlsafe()
        mensaje = "El libro '" + titulo + "' ha sido editado con exito"

        sust = {
            "mensaje": mensaje,
            "url": url
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(
            jinja.render_template("mensajeConfirmacion.html", **sust)
        )


app = webapp2.WSGIApplication([
    ('/editarLibroCientifico', EditarLibroCientificoHandler)
], debug=True)