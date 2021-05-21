import webapp2
from webapp2_extras import jinja2
from model.libroLiterario import libroLiterario
from google.appengine.api import users


class listarLibrosLiterariosHandler(webapp2.RequestHandler):
    def get(self):
        lista_librosliterarios = libroLiterario.query()

        sust = {
            "users": users,
            "lista_librosLiterarios": lista_librosliterarios
        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(
            jinja.render_template("librosLiterarios/listadoLibrosLiterarios.html", **sust)
        )



    def post(self):
        # Recupera del formulario
        titulo = self.request.get("edTitulo", "ERROR")
        autor = self.request.get("edAutor", "ERROR")
        genero = self.request.get("edGenero", "ERROR")


        # Guarda los datos
        datoslibroliterario = libroLiterario(titulo=titulo, autor=autor, genero=genero)
        datoslibroliterario.put()

        url = "/listarLibrosLiterarios"
        mensaje = "Su libro '" + titulo + "' ha sido guardado con exito"

        sust = {
            "mensaje": mensaje,
            "url": url
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(
            jinja.render_template("mensajeConfirmacion.html", **sust)
        )


app = webapp2.WSGIApplication([
    ('/listarLibrosLiterarios', listarLibrosLiterariosHandler)
], debug=True)
