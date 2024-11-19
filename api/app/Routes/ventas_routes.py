from flask import Blueprint, request
from ..models import Ventas, Detalles_ventas, db
from ..responses import response, notFound, badRequest, badEquals, delete, successfully, update
from ..schemas import api_ventas, api_venta, api_detalles_venta

ventas_routes = Blueprint('ventas_routes', __name__)

def set_venta(function):
    def wrap(*args, **kwargs):
        json = request.get_json(force=True)
        id_venta = json.get('id_venta', None)
        venta = Ventas.query.filter_by(id_venta=id_venta).first()
        if venta is None:
            return notFound()
        return function(venta)
    wrap.__name__ = function.__name__
    return wrap

@ventas_routes.route('/ventas', methods=['GET'])
def get_ventas():
    ventas = Ventas.query.all()
    return successfully(api_ventas.dump(ventas))

@ventas_routes.route('/venta', methods=['GET'])
@set_venta
def get_venta(venta):
    return successfully(api_venta.dump(venta))


@ventas_routes.route('/ventas/count', methods=['GET'])
def count_ventas():
    count = Ventas.count_ventas()
    return successfully({"total_ventas": count})


@ventas_routes.route('/venta', methods=['PUT'])
@set_venta
def update_venta(venta):
    json = request.get_json(force=True)
    for key, value in json.items():
        setattr(venta, key, value)
    if venta.save():
        return update(api_venta.dump(venta))
    return badRequest()

@ventas_routes.route('/venta', methods=['POST'])
def create_venta():
    json = request.get_json(force=True)
    
    # Datos para la tabla Ventas
    venta_data = {
        "usuario_venta": json.get("usuario_venta"),
        "id_cliente_venta": json.get("id_cliente_venta"),
        "total_venta": json.get("total_venta"),
        "estado_venta": json.get("estado_venta")
    }  
   
    
    # Crear objeto de venta
    venta = Ventas.new(venta_data)

    # Datos para la tabla Detalles_ventas (lista de detalles)
    detalles_data = json.get("detalles_ventas", [])
    detalles = [Detalles_ventas.new({
        "cantidad_detalles_ventas": d["cantidad_detalles_ventas"],
        "precio_detalles_ventas": d["precio_detalles_ventas"],
        "venta_detalles_ventas": venta.id_venta,  # ID de la venta relacionada
        "producto_detalles_ventas": d["producto_detalles_ventas"]
    }) for d in detalles_data]

    # Transacción para guardar la venta y sus detalles
    try:
        db.session.add(venta)
        db.session.flush()  # Refleja el ID de la venta en la sesión antes de los detalles

        # Agregar detalles a la sesión con el ID de venta actual
        for detalle in detalles:
            detalle.venta_detalles_ventas = venta.id_venta  # asigna el ID de la venta
            db.session.add(detalle)

        db.session.commit()  # Confirma ambas operaciones si no hay errores

        return response({
            "venta": api_venta.dump(venta),
            "detalles": [api_detalles_venta.dump(d) for d in detalles]
        })
    except Exception as e:
        db.session.rollback()  # Revierte la transacción si ocurre un error
        print(f"Error: {e}")
        return badRequest()

@ventas_routes.route('/venta', methods=['DELETE'])
@set_venta
def delete_venta(venta):
    if venta.delete():
        return delete()
    return badRequest()

