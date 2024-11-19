from flask import Blueprint, request
from ..models import Cliente
from ..responses import response, notFound, badRequest, badEquals, delete, successfully, update
from ..schemas import api_cliente, api_clientes

cliente_routes = Blueprint('cliente_routes', __name__)

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

@cliente_routes.route('/clientes/count', methods=['GET'])
def count_clients():
    count = Cliente.count_clients()
    return successfully({"total_clients": count})

@cliente_routes.route('/clientes/ultimos', methods=['GET'])
def three_clients():
   theree= Cliente.get_last_three_clients()
   return successfully(api_clientes.dump(theree))


@cliente_routes.route('/clientes', methods=['GET'])
def get_clients():
    users = Cliente.query.all()
    return successfully(api_clientes.dump(users))

@cliente_routes .route('/clienteSearch/', methods=['POST'])
@set_client
def get_client(usuario):
    return successfully(api_cliente.dump(usuario))

@cliente_routes.route('/clienteRegister', methods=['POST'])
def create_user():    
    json = request.get_json(force=True)     
    user_exists = Cliente.get_cliente(json["cedula_cliente"])    
    if user_exists:
        return badEquals() 
    else:
        user = Cliente.new(json)
        print("\n")
        print("\n")
        print(user) 
        print("\n")
        print("\n")     
        if user.save():
            return response(api_cliente.dump(user))   
    return badRequest()

@cliente_routes.route('/cliente/', methods=['PUT'])
@set_client
def update_client(usuario):
    json = request.get_json(force=True)
    for key, value in json.items():
        setattr(usuario, key, value)
    if usuario.save():
        return update(api_cliente.dump(usuario))
    return badRequest()

@cliente_routes.route('/cliente/', methods=['DELETE'])
@set_client
def delete_client(usuario):
    if usuario.delete():
        return delete()
    return badRequest()
