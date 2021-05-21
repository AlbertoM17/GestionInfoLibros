import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from model.libroLiterario import libroLiterario
from model.comentario import Comentario

class verLibroLiterarioHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
                try:
                    id_libroLiterario = self.request.GET["id_libroLiterario"]
                except:
                    id_libroLiterario = "ERROR"
                libroLiterario = ndb.Key(urlsafe=id_libroLiterario).get()
                lista_comentarios = Comentario.query(Comentario.libro == libroLiterario.titulo)
                user_name = user.nickname()
                sust = {
                    "users": users,
                    "libroLiterario": libroLiterario,
                    "lista_comentarios": lista_comentarios,
                    "user_name": user_name
                }

                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(
                    jinja.render_template("librosLiterarios/detalleLibroLiterario.html", **sust)
                )
        else:
            self.redirect("/")
            return

    def post(self):
        user = users.get_current_user()

        id_libroLiterario = self.request.get("edIdLibroLiterario", "ERROR")
        textoComentario = self.request.get("edComentario", "ERROR")

        libroLiterario = ndb.Key(urlsafe=id_libroLiterario).get()
        comentario = Comentario(user_name=user.nickname(), texto=textoComentario, libro=libroLiterario.titulo)
        comentario.put()
        url = "/verLibroLiterario?id_libroLiterario=" + libroLiterario.key.urlsafe()
        mensaje = "Su comentario para el libro '" + libroLiterario.titulo + "' ha sido guardado con exito"
        template_values = {
            "mensaje": mensaje,
            "url": url
        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("mensajeConfirmacion.html", **template_values))

app = webapp2.WSGIApplication([
    ('/verLibroLiterario', verLibroLiterarioHandler),
], debug=True)