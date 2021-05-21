from google.appengine.ext import ndb

class Comentario(ndb.Model):
    texto = ndb.StringProperty(required=True)
    user_name = ndb.StringProperty(required=True)
    libro = ndb.StringProperty(required=True)