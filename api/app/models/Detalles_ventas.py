from . import db
from .Ventas import Ventas
from .Producto import Producto
from .Cliente import Cliente 
from .Ventas import Ventas

class Detalles_ventas(db.Model):
    __tablename__ = 'detalles_ventas'
    id_detalles_ventas = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    cantidad_detalles_ventas = db.Column(db.Numeric(10,2),  nullable=False)
    precio_detalles_ventas = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_detalles_ventas = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)    
    
    venta_detalles_ventas  = db.Column(db.Integer, db.ForeignKey('ventas.id_venta'), nullable=False)
    venta = db.relationship('Ventas', back_populates='detalles_ventas', overlaps="detalles_ventas")
    
    producto_detalles_ventas = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    producto = db.relationship('Producto', back_populates='producto_detalles_ventas', overlaps='producto_detalles_ventas')   
    
    @staticmethod
    def get_detalles_venta(id_detalles_ventas):
        return Detalles_ventas.query.filter_by(id_detalles_ventas=id_detalles_ventas).first()   
       
    @classmethod
    def new(cls, **kwargs):  # Cambio en la definición para aceptar **kwargs
        return Detalles_ventas(**kwargs)
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
       
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False
    
    def __str__(self):
        return self.id_detalles_ventas
    
    @staticmethod
    def get_ventas_with_details(id_venta):
        query = db.session.query(
            Detalles_ventas,
            Ventas,
            Producto
        ).join(
            Detalles_ventas, Ventas.id_venta == Detalles_ventas.venta_detalles_ventas
        ).join(
            Producto,  Producto.id_producto == Detalles_ventas.producto_detalles_ventas
        ).filter(
            Ventas.id_venta == id_venta
        ).first()
        return query
    
    @staticmethod
    def get_detailed_sales():
        query = db.session.query(
        Detalles_ventas.id_detalles_ventas,  # Asegúrate de incluir id_venta
        Ventas.id_cliente_venta,  # Asegúrate de incluir el id del cliente
        Cliente.cedula_cliente,
        Cliente.nombre_cliente,
        Cliente.apellido_cliente,
        Cliente.direccion_cliente,
        Cliente.correo_cliente,
        Detalles_ventas.fecha_detalles_ventas,
        Detalles_ventas.cantidad_detalles_ventas,
        Detalles_ventas.precio_detalles_ventas,        
        Producto.nombre_producto
    ).join(
        Ventas, Detalles_ventas.venta_detalles_ventas == Ventas.id_venta
    ).join(
        Cliente, Ventas.id_cliente_venta == Cliente.id_cliente
    ).join(
        Producto, Detalles_ventas.producto_detalles_ventas == Producto.id_producto
    ).all()
        return query
    
    def __str__(self):
        return self.id_detalles_ventas