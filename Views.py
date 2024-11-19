from  flask import Blueprint
from .models import Cliente, Dispositivo, Usuario, Reparaciones
from flask import request
from marshmallow import pprint
from .responses import response, notFound, badRequest, badEquals, delete, successfully, update
from .schemas import api_cliente, api_clientes, api_dispositivos, api_dispositivo, api_Usuario, api_Usuarios, api_reparacion, api_reparaciones





api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')

# --------------------- Cliente --------------------------------------- 

# Decorador para obtener el cliente
def set_client(function):
    def wrap(*args, **kwargs):
        json = request.get_json(force=True)
        cedula_cliente = json.get('cedula_cliente', None)
        usuario = Cliente.query.filter_by(cedula_cliente=cedula_cliente).first()
        if usuario is None:
            return notFound()
        return function(usuario)
    wrap.__name__ = function.__name__
    return wrap

@api_v1.route('/clientes', methods=['GET'])
def get_clients():
    users = Cliente.query.all()
    return successfully(api_clientes.dump(users))

# Ruta para obtener un cliente
@api_v1.route('/cliente/', methods=['GET'])
@set_client
def get_client(usuario):
    return successfully(api_cliente.dump(usuario))

@api_v1.route('/cliente', methods=['POST'])
def create_user():    
    json = request.get_json(force=True)     
    user_exists = Cliente.get_cliente(json["cedula_cliente"])    
    if user_exists:
        return badEquals() 
    else:
        user = Cliente.new(json)
        if user.save():
            return response(api_cliente.dump(user))   
    return badRequest()

@api_v1.route('/cliente/', methods=['PUT'])
@set_client
def update_client(usuario):
    json = request.get_json(force=True)
    for key, value in json.items():
        setattr(usuario, key, value)
    if usuario.save():
        return update(api_cliente.dump(usuario))
    return badRequest()

@api_v1.route('/cliente/', methods=['DELETE'])
@set_client
def delete_client(usuario):
    if usuario.delete():
        return delete()
    return badRequest()


#---------------------------------------- dispositivo---------------------------------------------------------------------

def set_dispositivo(function):
    def wrap(*args, **kwargs):
        json = request.get_json(force=True)
        serial_dispositivo = json.get('serial_dispositivo', None)
        device = Dispositivo.query.filter_by(serial_dispositivo=serial_dispositivo).first()
        if device is None:
            return notFound()
        return function(device)
    wrap.__name__ = function.__name__
    return wrap

@api_v1.route('/dispositivos', methods=['GET'])
def get_dispositivos():
    devices = Dispositivo.query.all()
    return successfully(api_dispositivos.dump(devices))

@api_v1.route('/dispositivo', methods=['POST'])
def post_dispositivo():
    json = request.get_json(force=True)
    dispositivo_exist = Dispositivo.getDispositivo(json['serial_dispositivo'])
    if dispositivo_exist:
        return badEquals()
    else:
        device = Dispositivo.new(json)
        if device.save():
            return response(api_dispositivo.dump(device))
    return badRequest()

@api_v1.route('/dispositivo/', methods=['GET'])
@set_dispositivo
def get_dispositivo(device):
    return successfully(api_dispositivo.dump(device))

@api_v1.route('/dispositivo/', methods=['PUT'])
@set_dispositivo
def update_dispositivo(device):
    json = request.get_json(force=True)
    for key, value in json.items():
        setattr(device, key, value)
    if device.save():
        return update(api_dispositivo.dump(device))
    return badRequest()

@api_v1.route('/dispositivo/', methods=['DELETE'])
@set_dispositivo
def delete_dispositivo(device):
    if device.delete():
        return delete()
    return badRequest()


#---------------------------------------- usuario ---------------------------------------------------------------------

def set_usuario(function):
    def wrap(*args, **kwargs):
        json = request.get_json(force=True)
        correo_usuario = json.get('correo_usuario', None)
        usuario = Usuario.query.filter_by(correo_usuario=correo_usuario).first()
        if usuario is None:
            return notFound()
        return function(usuario)
    wrap.__name__ = function.__name__
    return wrap

@api_v1.route('/usuarios', methods=['GET'])
def get_usuarios():
    devices = Usuario.query.all()
    return successfully(api_Usuarios.dump(devices))

@api_v1.route('/usuario', methods=['POST'])
def post_usuario():
    json = request.get_json(force=True)
    dispositivo_exist = Usuario.getUsuario(json['correo_usuario'])
    if dispositivo_exist:
        return badEquals()
    else:
        device = Usuario.new(json)
        if device.save():
            return response(api_Usuario.dump(device))
    return badRequest()

@api_v1.route('/usuario/', methods=['GET'])
@set_usuario
def get_usuario(usuario):
    return successfully(api_Usuario.dump(usuario))

@api_v1.route('/usuario/', methods=['PUT'])
@set_usuario
def update_usuario(usuario):
    json = request.get_json(force=True)
    for key, value in json.items():
        setattr(usuario, key, value)
    if usuario.save():
        return update(api_Usuario.dump(usuario))
    return badRequest()


@api_v1.route('/usuario/', methods=['DELETE'])
@set_usuario
def delete_usuario(usuario):
    if usuario.delete():
        return delete()
    return badRequest()


#---------------------------------------- reparaciones ---------------------------------------------------------------------
def set_reparacion(function):
    def wrap(*args, **kwargs):
        json = request.get_json(force=True)
        id_reparaciones = json.get('id_reparaciones', None)
        reparacion = Reparaciones.get_reparaciones(id_reparaciones)
        if reparacion is None:
            return notFound()
        return function(reparacion)
    wrap.__name__ = function.__name__
    return wrap

@api_v1.route('/reparacion', methods=['POST'])
def post_reparacion():
    json = request.get_json(force=True)        
    device = Reparaciones.new(json)
    if device.save():
        return response(api_reparacion.dump(device))    
    return badRequest()

@api_v1.route('/reparacion', methods=['GET'])
def get_reparacion():
    data = request.get_json(force=True)  # Intenta obtener el JSON enviado en la solicitud
    id_reparaciones = data.get('id_reparaciones') if data else None
    
    if not id_reparaciones:
        return badRequest("El campo 'id_reparaciones' es obligatorio.")
    
    device = Reparaciones.get_reparaciones_with_details(id_reparaciones)
    
    if not device:
        return notFound()
    
    return successfully(api_reparaciones.dump(device))

@api_v1.route('/reparacion/', methods=['PUT'])
@set_reparacion
def update_reparacion(reparacion):
    json = request.get_json(force=True)
    for key, value in json.items():
        setattr(reparacion, key, value)
    if reparacion.save():
        return update(api_reparacion.dump(reparacion))
    return badRequest()




