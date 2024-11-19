from . import db
from .Proveedores import Proveedores
from .Usuario import Usuario


class Compras(db.Model):
    __tablename__ = 'compras'
    id_compras = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    total_compra = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_compra = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    metodo_pago = db.Column(db.String(45),  nullable=False) 
       
    usuario_compras =  db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    usuario = db.relationship('Usuario', back_populates='compras_usuario')
    
    compras_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id_proveedores'))
    proveedores = db.relationship('Proveedores', back_populates='compras_proveedores')
    
    compras_detalles_compras = db.relationship('Detalles_compra', back_populates='compras')

    
    @staticmethod
    def get_compras(id_compras):
        return Compras.query.filter_by(id_compras=id_compras).first()
    
    @classmethod
    def count_compras(cls):
        return db.session.query(db.func.count(cls.id_compras)).scalar()  
       
    @classmethod
    def new(cls, kwargs):
        return  Compras(**kwargs)
    
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
        return self.id_compras
    
    @staticmethod
    def get_compras_with_proveedor(id_compras, nit_proveedor):
        query = db.session.query(
            Compras,
            Proveedores
        ).join(
            Proveedores, Compras.compras_proveedor == Proveedores.id_proveedores
        ).filter(
            Compras.id_compras == id_compras,
            Proveedores.nit == nit_proveedor
        ).first()
        return query

    @staticmethod
    def get_compras_with_usuario(id_compras, correo_usuario=None, id_usuario=None):
        query = db.session.query(
            Compras,
            Usuario
        ).join(
            Usuario, Compras.usuario_compras == Usuario.id_usuario
        ).filter(
            Compras.id_compras == id_compras
        )
        
        if correo_usuario:
            query = query.filter(Usuario.correo_usuario == correo_usuario)
        if id_usuario:
            query = query.filter(Usuario.id_usuario == id_usuario)
        
        result = query.first()
        return result

    @staticmethod
    def get_compras_with_proveedor_and_usuario(id_compras, nit_proveedor, correo_usuario=None, id_usuario=None):
        # Get the purchase with the provider
        compra_proveedor = Compras.get_compras_with_proveedor(id_compras, nit_proveedor)
        
        if not compra_proveedor:
            return None
        
        # Get the purchase with the user
        compra_usuario = Compras.get_compras_with_usuario(id_compras, correo_usuario, id_usuario)
        
        if not compra_usuario:
            return None
        
        return compra_proveedor, compra_usuario

    



    
    
    
    
    
    