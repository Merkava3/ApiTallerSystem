from flask import Blueprint, request
from ..models import Reparaciones
from ..responses import response, notFound, badRequest, delete, successfully, update
from ..schemas import api_reparacion, api_reparaciones

reparaciones_routes = Blueprint('reparaciones_routes', __name__)

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

@reparaciones_routes.route('/reparacion', methods=['POST'])
def post_reparacion():
    json = request.get_json(force=True)        
    reparacion = Reparaciones.new(json)
    if reparacion.save():
        return response(api_reparacion.dump(reparacion))    
    return badRequest()


@reparaciones_routes.route('/reparaciones', methods=['GET'])
def get_reparaciones():
    devices = Reparaciones.query.all()
    return successfully(api_reparaciones.dump(devices))

@reparaciones_routes.route('/reparacion', methods=['GET'])
def get_reparacion():
    data = request.get_json(force=True)
    id_reparaciones = data.get('id_reparaciones') if data else None
    
    if not id_reparaciones:
        return badRequest("El campo 'id_reparaciones' es obligatorio.")
    
    reparacion = Reparaciones.get_reparaciones_with_details(id_reparaciones)
    
    if not reparacion:
        return notFound()
    
    return successfully(api_reparaciones.dump(reparacion))

@reparaciones_routes.route('/reparacion/', methods=['PUT'])
@set_reparacion
def update_reparacion(reparacion):
    json = request.get_json(force=True)
    for key, value in json.items():
        setattr(reparacion, key, value)
    if reparacion.save():
        return update(api_reparacion.dump(reparacion))
    return badRequest()

@reparaciones_routes.route('/reparacion/', methods=['DELETE'])
@set_reparacion
def delete_reparacion(reparacion):
    if reparacion.delete():
        return delete()
    return badRequest()
