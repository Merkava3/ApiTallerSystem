from flask import Blueprint
from .Routes.cliente_routes import cliente_routes
from .Routes.dispositivos_routes import dispositivo_routes
from .Routes.reparaciones_routes import reparaciones_routes
from .Routes.usuarios_routes import usuarios_routes
from .Routes.ventas_routes import ventas_routes
from .Routes.producto_routes import producto_routes
from .Routes.permisos_routes import permisos_routes
from .Routes.inventarios_routes import inventario_routes
from .Routes.proveedores_routes import proveedores_routes
from .Routes.compras_routes import compras_routes
from .Routes.detalles_compra_routes import detalles_compra_routes
from .Routes.detalles_venta_routes import detalles_venta_routes

api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')

# ------------------------ Ruta Cliente --------------------------------------
api_v1.register_blueprint(cliente_routes)

#------------------------ Ruta Usuario ---------------------------------------
api_v1.register_blueprint(usuarios_routes)

#------------------------ Ruta Dispositivo -----------------------------------
api_v1.register_blueprint(dispositivo_routes)

# ----------------------- Ruta Reparacion ------------------------------------
api_v1.register_blueprint(reparaciones_routes)

# ------------------------- Ruta ventas --------------------------------------
api_v1.register_blueprint(ventas_routes)

# ------------------------- Ruta Productos -----------------------------------
api_v1.register_blueprint(producto_routes)

# ------------------------- Ruta Permisos -------------------------------------
api_v1.register_blueprint(permisos_routes)

# ------------------------- Ruta Inventarios -----------------------------------
api_v1.register_blueprint(inventario_routes)

# ------------------------ Ruta Proveedores -----------------------------------
api_v1.register_blueprint(proveedores_routes)

# ------------------------ Ruta Compras ---------------------------------------
api_v1.register_blueprint(compras_routes)

# ------------------------ Ruta detalles_compra -------------------------------
api_v1.register_blueprint(detalles_compra_routes)


# ------------------------ Ruta detalles_venta -------------------------------
api_v1.register_blueprint(detalles_venta_routes)


