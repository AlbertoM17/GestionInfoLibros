import webapp2
from webapp2_extras import jinja2
from google.appengine.ext import ndb
from model.libroLiterario import libroLiterario
from google.appengine.api import users


class EditarLibroLiterarioHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            try:
                id_libroLiterario = self.request.GET["id_libroLiterario"]
            except:
                id_libroLiterario = "ERROR"
            libroLiterario = ndb.Key(urlsafe=id_libroLiterario).get()
            sust = {
                "libroLiterario": libroLiterario
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(
                jinja.render_template("librosLiterarios/editarLibroLiterario.html", **sust)
            )
        else:
            self.redirect("/")
            return

    def post(self):
        # Recupera del formulario
        titulo = self.request.get("edTitulo", "ERROR")
        autor = self.request.get("edAutor", "ERROR")
        genero = self.request.get("edGenero", "ERROR")

        id_libroLiterario = self.request.get("edIdLibroLiterario", "ERROR")

        # Guarda los datos
        libroLiterario = ndb.Key(urlsafe=id_libroLiterario).get()
        libroLiterario.titulo=titulo
        libroLiterario.autor = autor
        libroLiterario.genero = genero
        libroLiterario.put()

        url = "/verLibroLiterario?id_libroLiterario=" + libroLiterario.key.urlsafe()
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
    ('/editarLibroLiterario', EditarLibroLiterarioHandler)
], debug=True)