from flask import Blueprint, request
from ..models import Dispositivo
from ..responses import response, notFound, badRequest, badEquals, delete, successfully, update
from ..schemas import api_dispositivo, api_dispositivos

dispositivo_routes = Blueprint('dispositivo_routes', __name__)

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

@dispositivo_routes.route('/dispositivos', methods=['GET'])
def get_dispositivos():
    devices = Dispositivo.query.all()
    return successfully(api_dispositivos.dump(devices))

@dispositivo_routes.route('/dispositivo', methods=['POST'])
def post_dispositivo():
    json = request.get_json(force=True)
    dispositivo_exist = Dispositivo.get_dispositivo(json['serial_dispositivo'])
    if dispositivo_exist:
        return badEquals()
    else:
        device = Dispositivo.new(json)
        if device.save():
            return response(api_dispositivo.dump(device))
    return badRequest()

@dispositivo_routes.route('/dispositivo/', methods=['GET'])
@set_dispositivo
def get_dispositivo(device):
    return successfully(api_dispositivo.dump(device))

@dispositivo_routes.route('/dispositivo/', methods=['PUT'])
@set_dispositivo
def update_dispositivo(device):
    json = request.get_json(force=True)
    for key, value in json.items():
        setattr(device, key, value)
    if device.save():
        return update(api_dispositivo.dump(device))
    return badRequest()

@dispositivo_routes.route('/dispositivo/', methods=['DELETE'])
@set_dispositivo
def delete_dispositivo(device):
    if device.delete():
        return delete()
    return badRequest()
