from flask import Blueprint, request
from ..models import Producto
from ..responses import response, notFound, badRequest, badEquals, delete, successfully, update
from ..schemas import api_Producto, api_Productos

producto_routes = Blueprint('producto_routes', __name__)

def set_producto_by_codigo(function):
    def wrap(*args, **kwargs):
        json = request.get_json(force=True)
        codigo_producto = json.get('codigo_producto', None)
        producto = Producto.get_producto_by_codigo(codigo_producto)
        if producto is None:
            return notFound()
        return function(producto)
    wrap.__name__ = function.__name__
    return wrap

@producto_routes.route('/producto', methods=['POST'])
def post_producto():
    json = request.get_json(force=True)
    
    # Verificar si el código de producto ya existe
    codigo_producto = json.get('codigo_producto')
    if Producto.get_producto_by_codigo(codigo_producto):
        return badEquals()
    
    producto = Producto.new(json)
    if producto.save():
        return response(api_Producto.dump(producto))
    
    return badRequest()

@producto_routes.route('/producto/', methods=['GET'])
@set_producto_by_codigo
def get_client(producto):
    return successfully(api_Producto.dump(producto))

@producto_routes.route('/productos', methods=['GET'])
def get_clients():
    producto = Producto.query.all()
    return successfully(api_Productos.dump(producto))


@producto_routes.route('/producto', methods=['PUT'])
@set_producto_by_codigo
def update_producto(producto):
    json = request.get_json(force=True)
    for key, value in json.items():
        setattr(producto, key, value)
    if producto.save():
        return update(api_Producto.dump(producto))
    return badRequest()

@producto_routes.route('/producto', methods=['DELETE'])
@set_producto_by_codigo
def delete_producto(producto):
    if producto.delete():
        return delete()
    return badRequest()
