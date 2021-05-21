import webapp2
from webapp2_extras import jinja2
from model.libroCientifico import libroCientifico
from google.appengine.api import users


class listarLibrosCientificosHandler(webapp2.RequestHandler):
    def get(self):
        lista_librosCientificos = libroCientifico.query()

        sust = {
            "users": users,
            "lista_librosCientificos": lista_librosCientificos
        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(
            jinja.render_template("librosCientificos/listadoLibrosCientificos.html", **sust)
        )



    def post(self):
        # Recupera del formulario
        titulo = self.request.get("edTitulo", "ERROR")
        autor = self.request.get("edAutor", "ERROR")
        campo = self.request.get("edCampo", "ERROR")


        # Guarda los datos
        datoslibroCientifico = libroCientifico(titulo=titulo, autor=autor, campo=campo)
        datoslibroCientifico.put()

        url = "/listarLibrosCientificos"
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
    ('/listarLibrosCientificos', listarLibrosCientificosHandler)
], debug=True)
