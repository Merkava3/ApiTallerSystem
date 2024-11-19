from flask import Blueprint, request
from ..models import Compras
from ..responses import response, notFound, badRequest, badEquals, delete, successfully, update
from ..schemas import api_compra, api_compras, api_compra_details

compras_routes = Blueprint('compras_routes', __name__)

def set_compra(function):
    def wrap(*args, **kwargs):
        json = request.get_json(force=True)
        id_compras = json.get('id_compras', None)
        compra = Compras.get_compras(id_compras)
        if compra is None:
            return notFound()
        return function(compra)
    wrap.__name__ = function.__name__
    return wrap


@compras_routes.route('/compra', methods=['POST'])
def post_compras():
    json = request.get_json(force=True)    
    # Verificar si el código de producto ya existe
    codigo_producto = json.get('id_compras')
    if Compras.get_compras(codigo_producto):
        return badEquals()    
    compra = Compras.new(json)
    if compra.save():
        return response(api_compra.dump(compra))
    
@compras_routes.route('/compra/', methods=['GET'])
@set_compra
def get_compra(compra):
    return successfully(api_compra.dump(compra))

@compras_routes.route('/compras/count', methods=['GET'])
def count_ventas():
    count = Compras.count_compras()
    return successfully({"total_compras": count})

@compras_routes.route('/compras', methods=['GET'])
def get_compras():
    compra = Compras.query.all()
    return successfully(api_compras.dump(compra))

@compras_routes.route('/compra', methods=['PUT'])
@set_compra
def update_producto(compra):
    json = request.get_json(force=True)
    for key, value in json.items():
        setattr(compra, key, value)
    if compra.save():
        return update(api_compra.dump(compra))
    return badRequest()

@compras_routes.route('/compra', methods=['DELETE'])
@set_compra
def delete_producto(compra):
    if compra.delete():
        return delete()
    return badRequest()

