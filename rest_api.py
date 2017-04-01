import endpoints
from google.appengine.ext import ndb
from google.appengine.api import app_identity
from protorpc import remote

import jwt
import time

from CustomExceptions import NotFoundException

from messages import EmailPasswordMessage, TokenMessage, CodeMessage, Token, TokenKey,MessageNone
from messages import EmpresaInput, EmpresaUpdate, EmpresaList
from messages import TeamInput, TeamUpdate, TeamList 
from messages import UserInput, UserUpdate, UserList
from messages import ProyectoInput, ProyectoUpdate, ProyectoList
from messages import ServicioInput, ServicioUpdate, ServicioList
from messages import PortafolioInput, PortafolioUpdate, PortafolioList
from messages import ClienteInput, ClienteUpdate, ClienteList


from endpoints_proto_datastore.ndb import EndpointsModel

import models
from models import validarEmail
from models import Empresa, Usuarios, Team, Proyecto, Servicio, Portafolio


###############
# Usuarios
###############
@endpoints.api(name='usuarios_api', version='v1', description='usuarios endpoints')
class UsuariosApi(remote.Service):
###############get the info of one########
 @endpoints.method(TokenKey, UserList, path='users/get', http_method='POST', name='users.get')
 def users_get(cls, request):
  try:                 
   token = jwt.decode(request.tokenint, 'secret')  #checa token
   userentity = ndb.Key(urlsafe=request.entityKey)
   user = Usuarios.get_by_id(userentity.id()) #obtiene usuario
            #user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = []  #crea lista
   lstMessage = UserList(code=1) # crea objeto mensaje
   lista.append(UserUpdate(token='', 
    entityKey= user.entityKey,
    #empresa_key = user.empresa_key.urlsafe(),
    email = user.email))
   lstMessage.data = lista#ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = UserList(code=-1, data=[]) #token invalido
  except jwt.ExpiredSignatureError:
   message = UserList(code=-2, data=[]) #token expiro
  return message


########################## list###################
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, UserList, path='users/list', http_method='POST', name='users.list')
 def lista_usuarios(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')  #checa token
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = []  #crea lista
   lstMessage = UserList(code=1) # crea objeto mensaje
   lstBd = Usuarios.query().fetch() # recupera de base de datos
   for i in lstBd: # recorre
    lista.append(UserUpdate(token='',
     entityKey=i.entityKey,
     #empresa_key=user.empresa_key.urlsafe(),
     email=i.email)) # agrega a la lista
    
   lstMessage.data = lista # la manda al messa
   message = lstMessage #regresa
    
  except jwt.DecodeError:
   message = UserList(code=-1, data=[]) #token invalido
  except jwt.ExpiredSignatureError:
   message = UserList(code=-2, data=[]) #token expiro
  return message

# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='users/delete', http_method='POST', name='users.delete')
 #siempre lleva cls y request
 def user_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   usersentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   usersentity.delete()#BORRA
   message = CodeMessage(code=1, message='Succesfully deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(UserInput, CodeMessage, path='users/insert', http_method='POST', name='users.insert')
 def user_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])
   if validarEmail(request.email) == False: #checa si el email esta registrado
                       #empresakey = ndb.Key(urlsafe=request.empresa_key) #convierte el string dado a entityKey
    if user.usuario_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
     codigo=1
    else:
     codigo=-3
                       #la funcion josue_m puede actualizar e insertar
                       #depende de la ENTRADA de este endpoint method
    message = CodeMessage(code=codigo, message='Succesfully added')
   else:
    message = CodeMessage(code=-4, message='El email ya ha sido registrado')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message


##login##

 @endpoints.method(EmailPasswordMessage, TokenMessage, path='users/login', http_method='POST', name='users.login')
 def users_login(cls, request):
  try:
   user = Usuarios.query(Usuarios.email == request.email).fetch() #obtiene el usuario dado el email
   if not user or len(user) == 0: #si no encuentra user saca
    raise NotFoundException()
   user = user[0] 
   keye = user.empresa_key.urlsafe() # regresa como mensaje el empresa key
   if not user.verify_password(request.password): # checa la contrasena
    raise NotFoundException()

   token = jwt.encode({'user_id': user.key.id(), 'exp': time.time() + 43200}, 'secret') #crea el token
   message = TokenMessage(token=token, message=keye, code=1) # regresa token
  except NotFoundException:
   message = TokenMessage(token=None, message='Wrong username or password', code=-1)
  return message

##update##
# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(UserUpdate, CodeMessage, path='user/update', http_method='POST', name='user.update')
#siempre lleva cls y request
 def user_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   if user.usuario_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message


'''
'''

###########################
#### Empresa
###########################


## Google Cloud Endpoint
@endpoints.api(name='empresas_api', version='v1', description='empresas REST API')
class EmpresasApi(remote.Service):


# get one

 @endpoints.method(TokenKey, EmpresaList, path='empresa/get', http_method='POST', name='empresa.get')
#siempre lleva cls y request
 def empresa_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   empresaentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #empresaentity.get().empresa_key.urlsafe() para poder optener el EntityKey
     ##### ejemplo real
    ####### message = EmpresaList(code=1, data=[EmpresaUpdate(token='Succesfully get', nombre_empresa=empresaentity.get().nombre_empresa, empresa_key=empresaentity.get().empresa_key.urlsafe(), entityKey=empresaentity.get().entityKey)])
   message = EmpresaList(code=1, data = [EmpresaUpdate(token='Succesfully get',
    entityKey = empresaentity.get().entityKey,
    codigo_empresa=empresaentity.get().codigo_empresa, 
    nombre_empresa = empresaentity.get().nombre_empresa)])

  except jwt.DecodeError:
   message = EmpresaList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = EmpresaList(code=-2, data=[])
  return message




 @endpoints.method(TokenKey, CodeMessage, path='empresa/delete', http_method='POST', name='empresa.delete')
#siempre lleva cls y request
 def empresa_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   empresaentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   empresaentity.delete()#BORRA
   message = CodeMessage(code=1, message='Succesfully deleted')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message


# insert
 @endpoints.method(EmpresaInput, CodeMessage, path='empresa/insert', http_method='POST', name='empresa.insert')
#siempre lleva cls y request
 def empresa_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario models.py 
   myempresa = Empresa()
   if myempresa.empresa_m(request)==0: 
    codigo=1
   else:
		codigo=-3
      	      #la funcion josue_m puede actualizar e insertar
	      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Succesfully added')
      #else:
	    #  message = CodeMessage(code=-4, message='Succesfully added')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message



# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(EmpresaUpdate, CodeMessage, path='empresa/update', http_method='POST', name='empresa.update')
#siempre lleva cls y request
 def empresa_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN 
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
      #empresakey = ndb.Key(urlsafe=request.empresa_key)#convierte el string dado a entityKey
   myempresa = Empresa()
   if myempresa.empresa_m(request)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message



# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, EmpresaList, path='empresa/list', http_method='POST', name='empresa.list')
#siempre lleva cls y request
 def empresa_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   #if user.importante==1 or user.importante==2:
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = EmpresaList(code=1) #CREA el mensaje de salida
   lstBdEmpresa = Empresa.query().fetch() #obtiene de la base de datos
   for i in lstBdEmpresa: #recorre la base de datos
             #inserta a la lista creada con los elementos que se necesiten de la base de datos
             #i.empresa_key.urlsafe() obtiene el entityKey
	     #lista.append(ClientesUpdate(token='', nombre=i.nombre, status=i.status, empresa_key=i.empresa_key.urlsafe(), entityKey=i.entityKey))
    lista.append(EmpresaUpdate(token='', 
     entityKey = i.entityKey,
     codigo_empresa=i.codigo_empresa, 
     nombre_empresa = i.nombre_empresa))
      
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
      #else:
      #    message = EmpresaList(code=-3, data=[])
  except jwt.DecodeError:
   message = EmpresaList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = EmpresaList(code=-2, data=[])
  return message


###########################
#### Team
###########################

@endpoints.api(name='team_api', version='v1', description='team REST API')
class TeamApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, TeamList, path='team/get', http_method='POST', name='team.get')
#siempre lleva cls y request
 def team_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   teamentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = TeamList(code=1, data=[TeamUpdate(token='Succesfully get',
    entityKey=teamentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    nombre=teamentity.get().nombre, 
    puesto=teamentity.get().puesto, 
    urlImage=teamentity.get().urlImage)])
  except jwt.DecodeError:
   message = TeamList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = TeamList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='team/delete', http_method='POST', name='team.delete')
#siempre lleva cls y request
 def team_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   teamentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   teamentity.delete()#BORRA
   message = CodeMessage(code=0, message='Se ha eliminado el r.h.')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, TeamList, path='team/list', http_method='POST', name='team.list')
#siempre lleva cls y request
 def team_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = TeamList(code=1) #CREA el mensaje de salida
   lstBd = Team.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
	     
    lista.append(TeamUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     nombre=i.nombre, 
     puesto=i.puesto, 
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = TeamList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = TeamList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TeamInput, CodeMessage, path='team/insert', http_method='POST', name='team.insert')
#siempre lleva cls y request
 def team_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   myteam = Team()
   if myteam.team_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Su r.h. se ha sido registrado exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TeamUpdate, CodeMessage, path='team/update', http_method='POST', name='team.update')
#siempre lleva cls y request
 def team_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   myteam = Team()
   if myteam.team_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message


# ************
# *
# * Proyecto 
# *
# ************


@endpoints.api(name='proyecto_api', version='v1', description='proyecto REST API')
class ProyectoApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, ProyectoList, path='proyecto/get', http_method='POST', name='proyecto.get')
#siempre lleva cls y request
 def proyecto_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   proyectoentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = ProyectoList(code=1, data=[ProyectoUpdate(token='Succesfully get',
    entityKey=proyectoentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    titulo=proyectoentity.get().titulo, 
    contenido=proyectoentity.get().contenido, 
    urlImage=proyectoentity.get().urlImage)])
  except jwt.DecodeError:
   message = ProyectoList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = ProyectoList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='proyecto/delete', http_method='POST', name='proyecto.delete')
#siempre lleva cls y request
 def proyecto_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   proyectoentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   proyectoentity.delete()#BORRA
   message = CodeMessage(code=0, message='Se ha eliminado el proyecto')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, ProyectoList, path='proyecto/list', http_method='POST', name='proyecto.list')
#siempre lleva cls y request
 def proyecto_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = ProyectoList(code=1) #CREA el mensaje de salida
   lstBd = Proyecto.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
       
    lista.append(ProyectoUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     titulo=i.titulo, 
     contenido=i.contenido, 
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = ProyectoList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = ProyectoList(code=-2, data=[])
  return message

# insert
#  {
#   "titulo"   :    "",
#   "contenido":    "",
#   "token"    :    "",
#   "urlImage" :    ""
#   }


#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(ProyectoInput, CodeMessage, path='proyecto/insert', http_method='POST', name='proyecto.insert')
#siempre lleva cls y request
 def proyecto_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   myproyecto = Proyecto()
   if myproyecto.proyecto_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Su proyecto ha sido registrado exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(ProyectoUpdate, CodeMessage, path='proyecto/update', http_method='POST', name='proyecto.update')
#siempre lleva cls y request
 def proyecto_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   myproyecto = Proyecto()
   if myproyecto.proyecto_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message






# ***************
# *
# * Servicios 
# *
# ***************


@endpoints.api(name='servicio_api', version='v1', description='servicio REST API')
class ServicioApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, ServicioList, path='servicio/get', http_method='POST', name='servicio.get')
#siempre lleva cls y request
 def servicio_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   servicioentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = ServicioList(code=1, data=[ServicioUpdate(token='Succesfully get',
    entityKey=servicioentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    titulo=servicioentity.get().titulo, 
    descripcion=servicioentity.get().descripcion, 
    urlImage=servicioentity.get().urlImage)])
  except jwt.DecodeError:
   message = ServicioList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = ServicioList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='servicio/delete', http_method='POST', name='servicio.delete')
#siempre lleva cls y request
 def servicio_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   servicioentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   servicioentity.delete()#BORRA
   message = CodeMessage(code=0, message='Se ha eliminado el proyecto')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, ServicioList, path='servicio/list', http_method='POST', name='servicio.list')
#siempre lleva cls y request
 def servicio_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = ServicioList(code=1) #CREA el mensaje de salida
   lstBd = Servicio.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
       
    lista.append(ServicioUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     titulo=i.titulo, 
     descripcion=i.descripcion, 
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = ServicioList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = ServicioList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(ServicioInput, CodeMessage, path='servicio/insert', http_method='POST', name='servicio.insert')
#siempre lleva cls y request
 def servicio_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   myservicio = Servicio()
   if myservicio.servicio_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Su servicio ha sido registrado exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(ServicioUpdate, CodeMessage, path='servicio/update', http_method='POST', name='servicio.update')
#siempre lleva cls y request
 def servicio_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   myservicio = Servicio()
   if myservicio.servicio_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message







# ***************
# *
# * Portafolio
# *
# ***************


@endpoints.api(name='portafolio_api', version='v1', description='portafolio REST API')
class PortafolioApi(remote.Service):

#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(PortafolioInput, CodeMessage, path='portafolio/insert', http_method='POST', name='portafolio.insert')
#siempre lleva cls y request
 def portafolio_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   myportafolio = Portafolio()
   if myportafolio.portafolio_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Su proyecto ha sido registrado exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message



# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, PortafolioList, path='portafolio/get', http_method='POST', name='portafolio.get')
#siempre lleva cls y request
 def portafolio_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   portaflioentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = PortafolioList(code=1, data=[PortafolioUpdate(token='Succesfully get',
    entityKey=portafolioentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(),  
    urlImage=servicioentity.get().urlImage)])
  except jwt.DecodeError:
   message = PortafolioList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = PortafolioList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='portafolio/delete', http_method='POST', name='portafolio.delete')
#siempre lleva cls y request
 def portafolio_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   portafolioentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   portafolioentity.delete()#BORRA
   message = CodeMessage(code=0, message='Se ha eliminado el proyecto')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, PortafolioList, path='portafolio/list', http_method='POST', name='portafolio.list')
#siempre lleva cls y request
 def portafolio_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = PortafolioList(code=1) #CREA el mensaje de salida
   lstBd = Portafolio.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
       
    lista.append(PortafolioUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     urlImage=i.urlImage))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = PortafolioList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = PortafolioList(code=-2, data=[])
  return message


# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(PortafolioUpdate, CodeMessage, path='portafolio/update', http_method='POST', name='portafolio.update')
#siempre lleva cls y request
 def portafolio_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   myportafolio = Portafolio()
   if myportafolio.portafolio_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# ***************
# *
# * Cliente
# *
# ***************


@endpoints.api(name='cliente_api', version='v1', description='cliente REST API')
class ClienteApi(remote.Service):
# get one
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, ClienteList, path='cliente/get', http_method='POST', name='cliente.get')
#siempre lleva cls y request
 def cliente_get(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
      #Obtiene el elemento dado el entityKey
   clienteentity = ndb.Key(urlsafe=request.entityKey)
      #CREA LA SALIDA de tipo JosueInput y le asigna los valores, es a como se declaro en el messages.py
      #josuentity.get().empresa_key.urlsafe() para poder optener el EntityKey
   message = ClienteList(code=1, data=[ClienteUpdate(token='Succesfully get',
    entityKey=clienteentity.get().entityKey,
    #empresa_key=teamentity.get().empresa_key.urlsafe(), 
    nombre=clienteentity.get().nombre, 
    imagen=clienteentity.get().imagen)])
  except jwt.DecodeError:
   message = ClienteList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = ClienteList(code=-2, data=[])
  return message


# delete
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(TokenKey, CodeMessage, path='cliente/delete', http_method='POST', name='cliente.delete')
#siempre lleva cls y request
 def cliente_remove(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   clienteentity = ndb.Key(urlsafe=request.entityKey)#Obtiene el elemento dado el EntitKey
   clienteentity.delete()#BORRA
   message = CodeMessage(code=0, message='Se ha eliminado el proyecto')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# list
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(Token, ClienteList, path='cliente/list', http_method='POST', name='cliente.list')
#siempre lleva cls y request
 def cliente_list(cls, request):
  try:
   token = jwt.decode(request.tokenint, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene usuario dado el token
   lista = [] #crea lista para guardar contenido de la BD
   lstMessage = ClienteList(code=1) #CREA el mensaje de salida
   lstBd = Cliente.query().fetch() #obtiene de la base de datos
   for i in lstBd: #recorre la base de datos
    #inserta a la lista creada con los elementos que se necesiten de la base de datos
    #i.empresa_key.urlsafe() obtiene el entityKey
       
    lista.append(ClienteUpdate(token='', 
     entityKey=i.entityKey, 
     #empresa_key=i.empresa_key.urlsafe(),
     nombre=i.nombre, 
     imagen=i.imagen))
   lstMessage.data = lista #ASIGNA a la salida la lista
   message = lstMessage
  except jwt.DecodeError:
   message = ClienteList(code=-1, data=[])
  except jwt.ExpiredSignatureError:
   message = ClienteList(code=-2, data=[])
  return message

# insert
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(ClienteInput, CodeMessage, path='cliente/insert', http_method='POST', name='cliente.insert')
#siempre lleva cls y request
 def cliente_add(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id']) #obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de
   mycliente = Cliente()
   if mycliente.cliente_m(request, user.empresa_key)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
          #la funcion josue_m puede actualizar e insertar
          #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=codigo, message='Su proyecto ha sido registrado exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message

# update
#                   ENTRADA    SALIDA        RUTA              siempre es POST     NOMBRE
 @endpoints.method(ClienteUpdate, CodeMessage, path='cliente/update', http_method='POST', name='cliente.update')
#siempre lleva cls y request
 def cliente_update(cls, request):
  try:
   token = jwt.decode(request.token, 'secret')#CHECA EL TOKEN
   user = Usuarios.get_by_id(token['user_id'])#obtiene el usuario para poder acceder a los metodos declarados en models.py en la seccion de USUARIOS
   empresakey = ndb.Key(urlsafe=user.empresa_key.urlsafe())#convierte el string dado a entityKey
   mycliente = Cliente()
   if mycliente.portafolio_m(request, empresakey)==0:#llama a la funcion declarada en models.py en la seccion de USUARIOS
    codigo=1
   else:
    codigo=-3
      #la funcion josue_m puede actualizar e insertar
      #depende de la ENTRADA de este endpoint method
   message = CodeMessage(code=1, message='Sus cambios han sido guardados exitosamente')
  except jwt.DecodeError:
   message = CodeMessage(code=-2, message='Invalid token')
  except jwt.ExpiredSignatureError:
   message = CodeMessage(code=-1, message='Token expired')
  return message














application = endpoints.api_server([UsuariosApi, EmpresasApi, ProyectoApi, ServicioApi, PortafolioApi], restricted=False)

