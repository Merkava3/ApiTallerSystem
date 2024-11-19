from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .Cliente import Cliente
from .Dispositivo import Dispositivo
from .Usuario import Usuario
from .Permiso import Permiso
from .Producto import Producto
from .Reparaciones import  Reparaciones
from .Proveedores import Proveedores
from .Compras import Compras
from .Ventas import Ventas
from .Detalles_ventas import Detalles_ventas
from .Detalles_compra import Detalles_compra
from .Inventarios import Inventarios