from . import db
from .Compras import Compras
from .Producto import Producto
from .Proveedores import Proveedores
from .Usuario import Usuario

class Detalles_compra(db.Model):
    __tablename__ = 'Detalles_compra'
    id_Detalles_compra = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)   
    Cantidad_Detalles_compra = db.Column(db.Integer, nullable=False)
    Precio_Detalles_compra =  db.Column(db.Numeric(10, 2), nullable=False)
    
    id_compras_Detalles = db.Column(db.Integer, db.ForeignKey('compras.id_compras'))
    compras = db.relationship('Compras', back_populates='compras_detalles_compras', overlaps="compras_detalles_compras")
    
    # Clave foránea correcta apuntando a producto
    id_producto_compras = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    producto = db.relationship('Producto', back_populates='producto_detalles_compras')
    
    @staticmethod
    def get_Detalles_compra(id_Detalles_compra):
        return Detalles_compra.query.filter_by(id_Detalles_compra=id_Detalles_compra).first()

    @classmethod
    def new(cls, kwargs):
        return Detalles_compra(**kwargs)

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
        return self.id_Detalles_compra 
        

    @staticmethod
    def get_detalles_por_producto(id_producto):
        query = db.session.query(
            Detalles_compra,
            Producto
        ).join(
            Producto, Detalles_compra.id_producto_compras == Producto.id_producto
        ).filter(
            Producto.id_producto == id_producto
        ).all()
        return query

    @staticmethod
    def get_detalles_por_compras(id_compras):
        query = db.session.query(
            Detalles_compra,
            Compras
        ).join(
            Compras, Detalles_compra.id_compras_Detalles == Compras.id_compras
        ).filter(
            Compras.id_compras == id_compras
        ).all()
        return query

    @staticmethod
    def get_detalles_compras_producto(id_producto, id_compras):
        # Get details by product ID
        detalles_producto = Detalles_compra.get_detalles_por_producto(id_producto)
        
        if not detalles_producto:
            return None
        
        # Get details by purchase ID
        detalles_compras = Detalles_compra.get_detalles_por_compras(id_compras)
        
        if not detalles_compras:
            return None
        
        return detalles_producto, detalles_compras
    
    @staticmethod
    def get_compras_with_details():
        query = db.session.query(
            Compras,
            Detalles_compra,
            Producto,
            Usuario,
            Proveedores
        ).join(
            Detalles_compra, Compras.id_compras == Detalles_compra.id_compras_Detalles
        ).join(
            Producto, Detalles_compra.id_producto_compras == Producto.id_producto
        ).join(
            Usuario, Compras.usuario_compras == Usuario.id_usuario
        ).join(
            Proveedores, Compras.compras_proveedor == Proveedores.id_proveedores
        ).all()      
        return query
