from .import db
from .Producto import Producto

class Inventarios(db.Model):
    __tablename__ = 'inventarios'
    id_inventarios = db.Column(db.Integer,  primary_key=True, autoincrement=True, nullable=False)
    entrada = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_inventario = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    salida = db.Column(db.Numeric(10, 2), nullable=False)
    
     # Clave foránea que referencia a Producto
    id_producto_inventarios = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)
    producto = db.relationship('Producto', back_populates='inventario_produto')
    
    @staticmethod
    def get_inventarios(id_inventarios):
        return Inventarios.query.filter_by(id_inventarios=id_inventarios).first()
    
       
    @classmethod
    def new(cls, kwargs):
        return Inventarios(**kwargs)
    
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
        return self.id_inventarios
    
    @staticmethod
    def get_inventarios_with_product():
        query = db.session.query(
            Inventarios,
            Producto
        ).join(
            Producto, Inventarios.id_producto_inventarios == Producto.id_producto
        ).all()
        return query
    
    @staticmethod
    def search_product_in_inventarios(product_name):
        query = db.session.query(
            Inventarios,
            Producto
        ).join(
            Producto, Inventarios.id_producto_inventarios == Producto.id_producto
        ).filter(
            Producto.nombre_producto.ilike(f"%{product_name}%")
        ).all()
        return query
    
    