from flask import Blueprint, request
from ..models import Permiso
from ..responses import response, notFound, badRequest, successfully
from ..schemas import api_permiso, api_permisos

permisos_routes = Blueprint('permisos_routes', __name__)


def set_persimo_by_usuario(function):
    def wrap(*args, **kwargs):
        json = request.get_json(force=True)
        usuario_permiso = json.get('usuario_permiso', None)
        permiso = Permiso.get_permiso(usuario_permiso)
        if  permiso is None:
            return notFound()
        return function(permiso)
    wrap.__name__ = function.__name__
    return wrap

@permisos_routes.route('/permiso', methods=['POST'])
def post_permiso():
    json = request.get_json(force=True)        
    permiso = Permiso.new(json)
   
    if permiso.save():
        return response(api_permiso.dump(permiso))    
    return badRequest()

@permisos_routes.route('/permiso/', methods=['GET'])
@set_persimo_by_usuario
def get_client(permiso):
    return successfully(api_permiso.dump(permiso))

@permisos_routes.route('/permisos', methods=['GET'])
def set_persimo_by_usuario():
    permiso = Permiso.query.all()
    return successfully(api_permisos.dump(permiso))


