import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.libroCientifico import libroCientifico
from model.comentario import Comentario

class verLibroCientificoHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
                try:
                    id_libroCientifico = self.request.GET["id_libroCientifico"]
                except:
                    id_libroCientifico = "ERROR"
                libroCientifico = ndb.Key(urlsafe=id_libroCientifico).get()
                lista_comentarios = Comentario.query(Comentario.libro == libroCientifico.titulo)
                user_name = user.nickname()
                sust = {
                    "users": users,
                    "libroCientifico": libroCientifico,
                    "lista_comentarios": lista_comentarios,
                    "user_name": user_name
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(
                    jinja.render_template("librosCientificos/detalleLibroCientifico.html", **sust)
                )
        else:
            self.redirect("/")
            return

    def post(self):
        user = users.get_current_user()

        id_libroCientifico = self.request.get("edIdLibroCientifico", "ERROR")
        textoComentario = self.request.get("edComentario", "ERROR")

        libroCientifico = ndb.Key(urlsafe=id_libroCientifico).get()
        comentario = Comentario(user_name=user.nickname(), texto=textoComentario, libro=libroCientifico.titulo)
        comentario.put()
        url = "/verLibroCientifico?id_libroCientifico=" + libroCientifico.key.urlsafe()
        mensaje = "Su comentario para el libro '" + libroCientifico.titulo + "' ha sido guardado con exito"
        template_values = {
            "mensaje": mensaje,
            "url": url
        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("mensajeConfirmacion.html", **template_values))

app = webapp2.WSGIApplication([
    ('/verLibroCientifico', verLibroCientificoHandler),
], debug=True)