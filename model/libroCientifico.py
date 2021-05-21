from google.appengine.ext import ndb


class libroCientifico(ndb.Model):
    titulo = ndb.StringProperty(required=True)
    autor = ndb.StringProperty(required=True)
    campo = ndb.StringProperty(required=True)