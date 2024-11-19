from flask import Blueprint, request
from ..models import Usuario
from ..responses import response, notFound, badRequest, badEquals, delete, successfully, update
from ..schemas import api_Usuario, api_Usuarios

usuarios_routes = Blueprint('usuarios_routes', __name__)

def set_user(function):
    def wrap(*args, **kwargs):
        json = request.get_json(force=True)
        correo_usuario = json.get('correo_usuario', None)
        usuario = Usuario.query.filter_by(correo_usuario=correo_usuario).first()
        if usuario is None:
            return notFound()
        return function(usuario)
    wrap.__name__ = function.__name__
    return wrap


@usuarios_routes.route('/usuarios', methods=['GET'])
def get_clients():
    users = Usuario.query.all()
    return successfully(api_Usuarios.dump(users))

@usuarios_routes.route('/usuario/', methods=['GET'])
@set_user
def get_usuario(usuario):
    return successfully(api_Usuario.dump(usuario))



@usuarios_routes.route('/usuario', methods=['POST'])
def create_user():    
    json = request.get_json(force=True)     
    user_exists = Usuario.get_user(json["correo_usuario"])    
    if user_exists:
        return badEquals() 
    else:
        user = Usuario.new(**json)
        print("\n")
        print("\n")
        print(user) 
        print("\n")
        print(user.save())
        print("\n")             
        if user.save():
            return response(api_Usuario.dump(user))   
    return badRequest()

    
    
@usuarios_routes.route('/usuario/', methods=['PUT'])
@set_user
def update_producto(usuario):
    json = request.get_json(force=True)
    for key, value in json.items():
        setattr(usuario, key, value)
    if usuario.save():
        return update(api_Usuario.dump(usuario))
    return badRequest()
    

@usuarios_routes.route('/usuario', methods=['DELETE'])
@set_user
def delete_user(usuario):
    if usuario.delete():
        return delete()
    return badRequest()




