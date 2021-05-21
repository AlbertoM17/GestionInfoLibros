import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.libroCientifico import libroCientifico
from model.comentario import Comentario


class eliminarComentarioLibroCientificoHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
                try:
                    id_comentario = self.request.GET["id_comentario"]
                except:
                    id_comentario = "ERROR"
                comentario = ndb.Key(urlsafe=id_comentario).get()
                libroCientificoSeleccionado = libroCientifico.query(libroCientifico.titulo == comentario.libro)
                for libro in libroCientificoSeleccionado:
                    id_libroCientifico = libro.key.urlsafe()
                sust = {
                    "comentario" : comentario,
                    "id_libroCientifico" : id_libroCientifico
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("librosCientificos/eliminarComentarioLibroCientifico.html", **sust))
        else:
            self.redirect("/")
            return

    def post(self):
        user = users.get_current_user()

        if user:
            if not users.is_current_user_admin():
                id_libroCientifico = self.request.get("edIdLibroCientifico", "ERROR")
                id_comentario = self.request.get("edIdComentario", "ERROR")
                comentario = ndb.Key(urlsafe=id_comentario).get()
                url = "/verLibroCientifico?id_libroCientifico="+id_libroCientifico
                mensaje = "El comentario para el libro: "+comentario.libro+" ha sido eliminado con exito"
                comentario.key.delete()
                sust = {
                    "mensaje": mensaje,
                    "url": url
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("mensajeConfirmacion.html", **sust))
            else:
                self.redirect("/")
                return
        else:
            self.redirect("/")
            return

app = webapp2.WSGIApplication([
    ('/eliminarComentarioLibroCientifico', eliminarComentarioLibroCientificoHandler),
], debug=True)