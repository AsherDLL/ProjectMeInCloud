import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.api import mail
import cloudstorage
import mimetypes
import json
import os
import jinja2

from models import Proyecto
from models import Empresa
from models import Team
from models import Servicio
from models import Portafolio


jinja_env = jinja2.Environment(
 loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class DemoClass(object):
 pass

def MyClass(obj):
 return obj.__dict__

# el que regresa la info de title de proyecto 

class getProjectHeaderHandler(webapp2.RequestHandler):

    def get(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     id_empresa = self.request.get('empresa')
     objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()
     strKey = objemp.key.urlsafe() 
     myEmpKey = ndb.Key(urlsafe=strKey) 
     myTeam = Team.query(Team.empresa_key == myEmpKey)

     myList = []
     for i in myTeam:
      myObj = DemoClass()
      myObj.nombre = i.nombre
      myObj.puesto = i.puesto
      myObj.urlImage = i.urlImage
      myList.append(myObj)
       
     json_string = json.dumps(myList, default=MyClass)
     self.response.write(json_string)





#  El viejo solo para tener acceso a las funciones originales


class GetTeamHandler(webapp2.RequestHandler):

    def get(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     id_empresa = self.request.get('empresa')
     objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()
     strKey = objemp.key.urlsafe() 
     myEmpKey = ndb.Key(urlsafe=strKey) 
     myTeam = Team.query(Team.empresa_key == myEmpKey)

     myList = []
     for i in myTeam:
      myObj = DemoClass()
      myObj.nombre = i.nombre
      myObj.puesto = i.puesto
      myObj.urlImage = i.urlImage
      myList.append(myObj)
       
     json_string = json.dumps(myList, default=MyClass)
     self.response.write(json_string)


class GetProyectoHandler(webapp2.RequestHandler):

    def get(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*') # Permite que cualquier servicio lo invoque desde cualquier direccion 
     self.response.headers['Content-Type'] = 'application/json'  # Creo que asiga el tipo de respuesta a renguaje de objetos de javascript  JS-O-N

     id_empresa = self.request.get('empresa') # Obtengo de las variables get, la variable empresa
     objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()  # query a la base de datos, la tabla empresa WHERE 
     strKey = objemp.key.urlsafe()  # obtengo el key del objeto que me regreso, le aplico un urlsafe?... mehh....
     myEmpKey = ndb.Key(urlsafe=strKey)  # le hago algo a la llave para poder usarla en la query
     myTeam = Proyecto.query(Proyecto.empresa_key == myEmpKey) #query a la tabla Team con el WHERE en los parentesis  

     myList = []
     for i in myTeam:
      myObj = DemoClass()
      myObj.titulo = i.titulo
      myObj.contenido = i.contenido
      myObj.urlImage = i.urlImage
      myList.append(myObj)
       
     json_string = json.dumps(myList, default=MyClass)
     self.response.write(json_string)

class GetServiceHandler(webapp2.RequestHandler):

    def get(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*') # Permite que cualquier servicio lo invoque desde cualquier direccion 
     self.response.headers['Content-Type'] = 'application/json'  # Creo que asiga el tipo de respuesta a renguaje de objetos de javascript  JS-O-N

     id_empresa = self.request.get('empresa') # Obtengo de las variables get, la variable empresa
     objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()  # query a la base de datos, la tabla empresa WHERE 
     strKey = objemp.key.urlsafe()  # obtengo el key del objeto que me regreso, le aplico un urlsafe?... mehh....
     myEmpKey = ndb.Key(urlsafe=strKey)  # le hago algo a la llave para poder usarla en la query
     myTeam = Servicio.query(Servicio.empresa_key == myEmpKey) #query a la tabla Team con el WHERE en los parentesis  

     myList = []
     for i in myTeam:
      myObj = DemoClass()
      myObj.titulo = i.titulo
      myObj.descripcion = i.descripcion
      myObj.urlImage = i.urlImage
      myList.append(myObj)
       
     json_string = json.dumps(myList, default=MyClass)
     self.response.write(json_string)

class GetPortafolioHandler(webapp2.RequestHandler):

    def get(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*') # Permite que cualquier servicio lo invoque desde cualquier direccion 
     self.response.headers['Content-Type'] = 'application/json'  # Creo que asiga el tipo de respuesta a renguaje de objetos de javascript  JS-O-N

     id_empresa = self.request.get('empresa') # Obtengo de las variables get, la variable empresa
     objemp = Empresa.query(Empresa.codigo_empresa == id_empresa).get()  # query a la base de datos, la tabla empresa WHERE 
     strKey = objemp.key.urlsafe()  # obtengo el key del objeto que me regreso, le aplico un urlsafe?... mehh....
     myEmpKey = ndb.Key(urlsafe=strKey)  # le hago algo a la llave para poder usarla en la query
     myTeam = Portafolio.query(Portafolio.empresa_key == myEmpKey) #query a la tabla Team con el WHERE en los parentesis  

     myList = []
     for i in myTeam:
      myObj = DemoClass()
      myObj.urlImage = i.urlImage
      myList.append(myObj)
       
     json_string = json.dumps(myList, default=MyClass)
     self.response.write(json_string)



###########################################################################     


class UpHandler(webapp2.RequestHandler):
    def _get_urls_for(self, file_name):
        
     bucket_name = app_identity.get_default_gcs_bucket_name()
     path = os.path.join('/', bucket_name, file_name)
     real_path = '/gs' + path
     key = blobstore.create_gs_key(real_path)
     try:
      url = images.get_serving_url(key, size=0)
     except images.TransformationError, images.NotImageError:
      url = "http://storage.googleapis.com{}".format(path)

     return url


    def post(self):
     self.response.headers.add_header('Access-Control-Allow-Origin', '*')
     self.response.headers['Content-Type'] = 'application/json'

     bucket_name = app_identity.get_default_gcs_bucket_name()
     uploaded_file = self.request.POST.get('uploaded_file')
     file_name = getattr(uploaded_file, 'filename', None)
     file_content = getattr(uploaded_file, 'file', None)
     real_path = ''

     if file_name and file_content:
      content_t = mimetypes.guess_type(file_name)[0]
      real_path = os.path.join('/', bucket_name, file_name)

      with cloudstorage.open(real_path, 'w', content_type=content_t,
       options={'x-goog-acl': 'public-read'}) as f:
       f.write(file_content.read())

      key = self._get_urls_for(file_name)
      self.response.write(key)


      sender_address = "Proyectos <correo@ponerlo.com>"
      subject = "Evento nuevo"
      body = "Se ha registrado un nuevo evento"
      to = "Admin <davilasher@gmail.com>"

      mail.send_mail(sender_address, to, subject, body)


class LoginHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('login.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class MenuHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('menuAdmin.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

#=============
#
#==Proyecto
#
#=============

class editProyectoHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('editProyecto.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class displayProyectsHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('displayProyects.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)


class AdminHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('admin.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)
#=============
#
#==Services
#
#=============

class createServiceHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('createService.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class displayServicesHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('displayServices.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class editServiceHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('editService.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

#=============
#
#==Portafolio
#
#=============

class displayPortfolioHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('displayPortafolio.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

class createPortfolioHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('createPortfolio.html', template_context))

   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

#=============
#
#==Main
#
#=============

class MainHandler(webapp2.RequestHandler):

   def get(self):

    template_context = {}
    self.response.out.write(
      self._render_template('index.html', template_context))


   def _render_template(self, template_name, context=None):
    if context is None:
     context = {}

    template = jinja_env.get_template(template_name)
    return template.render(context)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/editProyecto', editProyectoHandler),
    ('/displayProyects', displayProyectsHandler),
    ('/displayServices', displayServicesHandler),
    ('/createService', createServiceHandler),
    ('/editService', editServiceHandler),
    ('/displayPortafolio', displayPortfolioHandler),
    ('/createPortfolio', createPortfolioHandler),
    ('/menu', MenuHandler),
    ('/admin', AdminHandler),
    ('/up', UpHandler),
    ('/getportafolio', GetPortafolioHandler),
    ('/getservice', GetServiceHandler),
    ('/getproyecto', GetProyectoHandler),
    ('/getteam', GetTeamHandler),
    ('/getprojectheader', getProjectHeaderHandler),

], debug = True)
