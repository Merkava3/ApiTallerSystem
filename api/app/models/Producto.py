from . import db

class Producto(db.Model):
    __tablename__ = 'producto'
    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nombre_producto = db.Column(db.String(45), nullable=False)
    codigo_producto = db.Column(db.String(45), unique=True,  nullable=False)
    precio_compra_producto = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    precio_venta_producto = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    cantidad_producto = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    detalle_producto = db.Column(db.String(45), nullable=False)
    categoria = db.Column(db.String(45), nullable=False)
    
    producto_detalles_ventas = db.relationship('Detalles_ventas', back_populates='producto')
    inventario_produto = db.relationship('Inventarios', back_populates='producto', cascade="all, delete-orphan")
    producto_detalles_compras = db.relationship('Detalles_compra', back_populates='producto', cascade="all, delete-orphan")

    
    
    @staticmethod
    def get_producto_by_codigo(codigo_producto):
        return Producto.query.filter_by(codigo_producto=codigo_producto).first()
       
    @classmethod
    def new(cls, kwargs):
        return Producto(**kwargs)
    
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
        return self.codigo_producto

    

    
    
    