from . import db
from sqlalchemy.exc import IntegrityError
from .Cliente import Cliente
from .Usuario import Usuario


class Ventas(db.Model):
    __tablename__ = 'ventas'
    id_venta = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    
    usuario_venta = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    usuario = db.relationship('Usuario', back_populates='ventas')
    
    id_cliente_venta = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), nullable=False)
    cliente = db.relationship('Cliente', back_populates='ventas_cliente')
    
    total_venta = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    estado_venta = db.Column(db.Integer, nullable=False)
    fecha_venta = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    
    detalles_ventas = db.relationship('Detalles_ventas', back_populates='venta')
    
    @staticmethod
    def get_ventas(id_venta):
        return Ventas.query.filter_by(id_venta=id_venta).first()
    
    @classmethod
    def count_ventas(cls):
        return db.session.query(db.func.count(cls.id_venta)).scalar()

    @classmethod
    def new(cls, kwargs):
        return Ventas(**kwargs)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except IntegrityError as e:
            db.session.rollback()
            print(f"IntegrityError: {e}")
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Exception: {e.__class__.__name__}: {e}")
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Exception: {e.__class__.__name__}: {e}")
            return False

    
    @staticmethod
    def get_ventas_with_details(id_venta):
        query = db.session.query(
            Ventas,
            Cliente,
            Usuario
        ).join(
            Cliente, Ventas.id_cliente_venta == Cliente.id_cliente
        ).join(
            Usuario, Ventas.usuario_venta == Usuario.id_usuario
        ).filter(
            Ventas.id_venta == id_venta
        ).first()
        return query
