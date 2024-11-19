from flask import Blueprint, request
from ..models import Proveedores
from ..responses import response, notFound, badRequest, badEquals, delete, successfully, update
from ..schemas import api_proveedor, api_proveedores


proveedores_routes = Blueprint('proveedores_routes', __name__)

def set_proveedor(function):
    def wrap(*args, **kwargs):
        json = request.get_json(force=True)
        nit = json.get('nit', None)
        proveedor = Proveedores.get_proveedores(nit)
        if proveedor is None:
            return notFound()
        return function(proveedor)
    wrap.__name__ = function.__name__
    return wrap

@proveedores_routes.route('/proveedor', methods=['POST'])
def post_proveedor():
    json = request.get_json(force=True)    
    # Verificar si el código de producto ya existe
    nit = json.get('nit')
    if Proveedores.get_proveedores(nit):
        return badEquals()
    
    proveedor= Proveedores.new(json)
    if  proveedor.save():
        return response(api_proveedor.dump(proveedor))
    
    return badRequest()

@proveedores_routes.route('/proveedor/', methods=['GET'])
@set_proveedor
def get_proveedor(proveedor):
    return successfully(api_proveedor.dump(proveedor))


@proveedores_routes.route('/proveedores', methods=['GET'])
def get_proveedores():
    producto = Proveedores.query.all()
    return successfully(api_proveedores.dump(producto))

@proveedores_routes.route('/proveedor', methods=['PUT'])
@set_proveedor
def update_producto(proveedor):
    json = request.get_json(force=True)
    for key, value in json.items():
        setattr(proveedor, key, value)
    if proveedor.save():
        return update(api_proveedor.dump(proveedor))
    return badRequest()

@proveedores_routes.route('/proveedor', methods=['DELETE'])
@set_proveedor
def delete_producto(proveedor):
    if proveedor.delete():
        return delete()
    return badRequest()

