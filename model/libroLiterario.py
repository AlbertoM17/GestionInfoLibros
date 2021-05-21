from google.appengine.ext import ndb


class libroLiterario(ndb.Model):
    titulo = ndb.StringProperty(required=True)
    autor = ndb.StringProperty(required=True)
    genero = ndb.StringProperty(required=True)
