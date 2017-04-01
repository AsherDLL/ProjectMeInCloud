from protorpc import messages
from protorpc import message_types

class MessageNone(messages.Message):
    inti = messages.StringField(1)
# Input messages
#Recibe el token para validar
class Token(messages.Message):
    tokenint = messages.StringField(1, required=True)
    #entityKey = messages.StringField(2, required=False)
    #fromurl = messages.StringField(3)

#Recibe el token y un entityKey de cualquier base de datos para validar
class TokenKey(messages.Message):
    tokenint = messages.StringField(1, required=True)
    entityKey = messages.StringField(2, required=True)
    #fromurl = messages.StringField(3)


#Recibe el email y contrasena para la creacion de token
class EmailPasswordMessage(messages.Message):
    email = messages.StringField(1, required=True)
    password = messages.StringField(2, required=True)


#USERS
class UserInput(messages.Message):
    token = messages.StringField(1) 
    empresa_key = messages.StringField(2)
    email = messages.StringField(3)
    password = messages.StringField(4)



class UserUpdate(messages.Message):
    token = messages.StringField(1)
    email = messages.StringField(2)
    password = messages.StringField(3)
    entityKey = messages.StringField(4, required=True)

class UserList(messages.Message):
    code = messages.IntegerField(1)
    data = messages.MessageField(UserUpdate, 2, repeated=True)


######Empresa########

#Mensaje de Entrada y Salida para la base de datos Empresa
class EmpresaInput(messages.Message):
    token = messages.StringField(1, required=True) 
    codigo_empresa = messages.StringField(2)
    nombre_empresa = messages.StringField(3)


class EmpresaUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    entityKey = messages.StringField(2, required=True)
    codigo_empresa = messages.StringField(3)
    nombre_empresa = messages.StringField(4)



#regresa una lista para la base de datos Empresa
class EmpresaList(messages.Message):
    code = messages.IntegerField(1)
#regresa mensaje de lo ocurrido
#mensaje de tipo MENSAJEFIELD que regresa una lista de tipo EmpresaUpdate
#es necesario el repeated para que sea lista
    data = messages.MessageField(EmpresaUpdate, 2, repeated=True)


######Team########

#Mensaje de Entrada y Salida para la base de datos Team
class TeamInput(messages.Message):
    token = messages.StringField(1, required=True) 
    nombre = messages.StringField(2)
    puesto = messages.StringField(3)
    urlImage = messages.StringField(5)

    
class TeamUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    #empresa_key = messages.StringField(2, required=True)
    entityKey = messages.StringField(2, required=True)
    nombre = messages.StringField(3)
    puesto = messages.StringField(4)
    urlImage = messages.StringField(5)

#regresa una lista para la base de datos Empresa
class TeamList(messages.Message):
    code = messages.IntegerField(1)
#regresa mensaje de lo ocurrido
#mensaje de tipo MENSAJEFIED que regresa una lista de tipo TeamUpdate
#es necesario el repeated para que sea lista
    data = messages.MessageField(TeamUpdate, 2, repeated=True)



#Messages para proyectos
class ProyectoInput(messages.Message):
    token = messages.StringField(1, required=True)
    titulo = messages.StringField(2)
    contenido = messages.StringField(3)
    urlImage = messages.StringField(5)


class ProyectoUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    entityKey = messages.StringField(2, required=True)
    titulo = messages.StringField(3)
    contenido = messages.StringField(4)
    urlImage = messages.StringField(5)

class ProyectoList(messages.Message):
    code = messages.IntegerField(1)
    data = messages.MessageField(ProyectoUpdate, 2, repeated=True)



#Messages para Servicios
class ServicioInput(messages.Message):
    token = messages.StringField(1, required=True)
    titulo = messages.StringField(2)
    descripcion = messages.StringField(3)
    urlImage = messages.StringField(5)


class ServicioUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    entityKey = messages.StringField(2, required=True)
    titulo = messages.StringField(3)
    descripcion = messages.StringField(4)
    urlImage = messages.StringField(5)

class ServicioList(messages.Message):
    code = messages.IntegerField(1)
    data = messages.MessageField(ServicioUpdate, 2, repeated=True)



#Messages para Portafolio
class PortafolioInput(messages.Message):
    token = messages.StringField(1, required=True)
    urlImage = messages.StringField(2)



class PortafolioUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    entityKey = messages.StringField(2, required=True)
    urlImage = messages.StringField(3)


class PortafolioList(messages.Message):
    code = messages.IntegerField(1)
    data = messages.MessageField(PortafolioUpdate, 2, repeated=True)



#Messages para Cliente
class ClienteInput(messages.Message):
    token = messages.StringField(1, required=True)
    nombre = messages.StringField(2)
    imagen = messages.StringField(3)
    


class ClienteUpdate(messages.Message):
    token = messages.StringField(1, required=True)
    entityKey = messages.StringField(2, required=True)
    nombre = messages.StringField(3)
    imagen = messages.StringField(4)
    

class ClienteList(messages.Message):
    code = messages.IntegerField(1)
    data = messages.MessageField(PortafolioUpdate, 2, repeated=True)








    
# Output messages
#regresa un token
class TokenMessage(messages.Message):
    code = messages.IntegerField(1)
    message = messages.StringField(2)
    token = messages.StringField(3)

#regresa mensajes de lo ocurrido
class CodeMessage(messages.Message):
    code = messages.IntegerField(1)
    message = messages.StringField(2)




