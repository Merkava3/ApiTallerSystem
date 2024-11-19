from flask import Blueprint, request
from ..models import Detalles_ventas
from ..responses import response, notFound, badRequest, badEquals, delete, successfully, update
from ..schemas import api_detalles_ventas, api_detalles_venta, api_detalles_ventas_cliente_producto

detalles_venta_routes = Blueprint('detalles_venta_routes', __name__)

# Decorador para verificar la existencia de detalles de venta
def set_detalles_venta(function):
    def wrap(*args, **kwargs):
        json = request.get_json(force=True)
        id_detalles_ventas = json.get('id_detalles_ventas', None)  # Eliminado espacio adicional
        detalles_ventas = Detalles_ventas.get_detalles_venta(id_detalles_ventas)
        if detalles_ventas is None:
            return notFound()
        return function(detalles_ventas)
    wrap.__name__ = function.__name__
    return wrap

@detalles_venta_routes.route('/detalles_venta', methods=['POST'])
def post_detalles_ventas():
    json = request.get_json(force=True)
    
    # Convertir JSON si es una lista, dejando solo el primer elemento si es un diccionario
    if isinstance(json, list):
        if len(json) > 0 and isinstance(json[0], dict):
            json = json[0]  # Tomar el primer elemento si es un diccionario
        else:
            return badRequest("Invalid JSON format. Expected an object but received a list.")
    
    # Proceder con el flujo original si json es un diccionario
    if not isinstance(json, dict):
        return badRequest("Invalid JSON format. Expected an object.")
    
    id_detalles_ventas = json.get('id_detalles_ventas')
    if id_detalles_ventas and Detalles_ventas.get_detalles_venta(id_detalles_ventas):
        return badEquals()
    
    detalles_ventas = Detalles_ventas.new(**json)
    if detalles_ventas.save():
        return response(api_detalles_venta.dump(detalles_ventas))
    return badRequest()


# Ruta para obtener un reporte detallado de ventas
@detalles_venta_routes.route('/detalles_ventas/detallado', methods=['GET'])
def get_detailed_sales():
    detalles = Detalles_ventas.get_detailed_sales()
    return successfully(api_detalles_ventas_cliente_producto.dump(detalles))

# Ruta para obtener un detalle de venta específico
@detalles_venta_routes.route('/detalles_venta', methods=['GET'])
@set_detalles_venta
def get_client(detalles_ventas):
    return successfully(api_detalles_venta.dump(detalles_ventas))

# Ruta para obtener todos los detalles de ventas
@detalles_venta_routes.route('/detalles_ventas', methods=['GET'])
def get_detalles_venta():
    detalles_ventas = Detalles_ventas.query.all()
    return successfully(api_detalles_ventas.dump(detalles_ventas))

# Ruta para actualizar un detalle de venta
@detalles_venta_routes.route('/detalles_venta', methods=['PUT'])
@set_detalles_venta
def update_detalles_venta(detalles_venta):
    json = request.get_json(force=True)
    for key, value in json.items():
        setattr(detalles_venta, key, value)
    if detalles_venta.save():
        return update(api_detalles_venta.dump(detalles_venta))
    return badRequest()

# Ruta para eliminar un detalle de venta
@detalles_venta_routes.route('/detalles_venta', methods=['DELETE'])
@set_detalles_venta
def delete_producto(detalles_venta):
    if detalles_venta.delete():
        return delete()
    return badRequest()





