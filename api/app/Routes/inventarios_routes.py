from flask import Blueprint, request
from ..models import Inventarios
from ..responses import response, notFound, badRequest, badEquals, delete, successfully, update
from ..schemas import api_inventario, api_inventarios


inventario_routes = Blueprint('inventario_routes', __name__)


def set_inventario(function):
    def wrap(*args, **kwargs):
        json = request.get_json(force=True)
        id_inventarios = json.get('id_inventarios', None)
        inventario = Inventarios.get_inventarios(id_inventarios)
        if inventario is None:
            return notFound()
        return function(inventario)
    wrap.__name__ = function.__name__
    return wrap



@inventario_routes.route('/inventario', methods=['POST'])
def post_producto():
    json = request.get_json(force=True)    
    # Verificar si el código de producto ya existe
    id_inventarios = json.get('id_inventarios')
    if Inventarios.get_inventarios(id_inventarios):
        return badEquals()
    
    producto = Inventarios.new(json)
    if producto.save():
        return response(api_inventario.dump(producto))    
    return badRequest()

@inventario_routes.route('/inventarios', methods=['GET'])
def get_clients():
    Inventario = Inventarios.query.all()
    return successfully(api_inventarios.dump(Inventario))


@inventario_routes.route('/inventario', methods=['GET'])
@set_inventario
def get_client(inventario):
    return successfully(api_inventario.dump(inventario))


@inventario_routes.route('/inventario', methods=['PUT'])
@set_inventario
def update_producto(inventario):
    json = request.get_json(force=True)
    for key, value in json.items():
        setattr(inventario, key, value)
    if inventario.save():
        return update(api_inventario.dump(inventario))
    return badRequest()



@inventario_routes.route('/inventario', methods=['DELETE'])
@set_inventario
def delete_producto(inventario):
    if inventario.delete():
        return delete()
    return badRequest()






