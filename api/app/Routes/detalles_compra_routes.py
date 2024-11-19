from flask import Blueprint, request
from ..models import Detalles_compra
from flask import jsonify
from ..responses import response, notFound, badRequest, badEquals, delete, successfully, update
from ..schemas import api_detalles_compra, api_detalles_compras, api_compra_details 


detalles_compra_routes = Blueprint('detalles_compra_routes', __name__)


def set_detalles_compra(function):
    def wrap(*args, **kwargs):
        json = request.get_json(force=True)
        id_Detalles_compra = json.get('id_Detalles_compra', None)
        producto = Detalles_compra.get_Detalles_compra(id_Detalles_compra)
        if producto is None:
            return notFound()
        return function(producto)
    wrap.__name__ = function.__name__
    return wrap

@detalles_compra_routes.route('/detalles_compra', methods=['POST'])
def post_detalles_compra():
    json = request.get_json(force=True)    
    # Verificar si el código de producto ya existe
    id_Detalles_compra = json.get('id_Detalles_compra')
    if Detalles_compra.get_Detalles_compra(id_Detalles_compra):
        return badEquals()
    
    detalles_compra = Detalles_compra.new(json)
    if detalles_compra.save():
        return response(api_detalles_compra.dump(detalles_compra))
    
    return badRequest()

@detalles_compra_routes.route('/detalles_compra', methods=['GET'])
@set_detalles_compra
def get_detalles_compra(detalles_compra):
    return successfully(api_detalles_compra.dump(detalles_compra))

@detalles_compra_routes.route('/detalles_compras', methods=['GET'])
def get_detalles_compras():
    detalles_compra = Detalles_compra.query.all()
    return successfully(api_detalles_compras.dump(detalles_compra))


@detalles_compra_routes.route('/detalle_compra', methods=['PUT'])
@set_detalles_compra
def update_producto(detalles_compra):
    json = request.get_json(force=True)
    for key, value in json.items():
        setattr(detalles_compra, key, value)
    if detalles_compra.save():
        return update(api_detalles_compra.dump(detalles_compra))
    return badRequest()

@detalles_compra_routes.route('/detalle_compra', methods=['DELETE'])
@set_detalles_compra
def delete_producto(detalles_compra):
    if detalles_compra.delete():
        return delete()
    return badRequest()


@detalles_compra_routes.route('/compra_detalles/details', methods=['GET'])
def get_compras_with_details():
    result = Detalles_compra.get_compras_with_details()
    print(result)

    if not result:
        return notFound()  # Si no hay resultados, retorna un error 404

    serialized_result = []

    for item in result:
        compras = item[0]  # Primer objeto en la tupla (Compras)
        detalles_compra = item[1]  # Segundo objeto en la tupla (Detalles_compra)
        producto = item[2]  # Tercer objeto en la tupla (Producto)
        usuario = item[3]  # Cuarto objeto en la tupla (Usuario)
        proveedores = item[4]  # Quinto objeto en la tupla (Proveedores)

        serialized_result.append({
            "id_compras": compras.id_compras,  # 'id_compras' está en el modelo Compras
            "fecha_compra": compras.fecha_compra,  # 'fecha_compra' en Compras
            "categoria": producto.categoria,  # 'categoria' en Producto
            "cantidad": detalles_compra.Cantidad_Detalles_compra,  # 'cantidad' en Detalles_compra
            "correo_usuario": usuario.correo_usuario,
            "nombre_producto": producto.nombre_producto,
            "detalle_producto": producto.detalle_producto,
            "nit": proveedores.nit,
            "telefono": proveedores.telefono
                       
        })

    return jsonify({
        "status": "success",
        "data": serialized_result
    })




