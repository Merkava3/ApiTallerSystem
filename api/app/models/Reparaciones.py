from . import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from .Cliente import Cliente
from .Dispositivo import Dispositivo
from .Usuario import Usuario

class Reparaciones(db.Model):
    __tablename__ = 'reparaciones'
    id_reparaciones = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    comentario = db.Column(db.String(500), nullable=False)
    procedimientos = db.Column(db.String(500), nullable=False)
    precio_reparacion = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)

    id_usuario_reparaciones = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    usuario = db.relationship('Usuario', back_populates='reparaciones_usuario')

    id_cliente_reparaciones = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), nullable=False)
    cliente = db.relationship('Cliente', back_populates='reparaciones_cliente')
 
    id_dispositivo_reparaciones = db.Column(db.Integer, db.ForeignKey('dispositivo.id_dispositivo'), nullable=False)
    dispositivo = db.relationship('Dispositivo', back_populates='reparaciones_dispositivo')

    @staticmethod
    def get_reparaciones(id_reparaciones):
        return Reparaciones.query.filter_by(id_reparaciones=id_reparaciones).first()
    
    @staticmethod
    def get_all():
        """Obtiene todos los Reparaciones almacenados en la base de datos."""
        return Reparaciones.query.all()


    @classmethod
    def new(cls, kwargs):
        return Reparaciones(**kwargs)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error en save: {e}")
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error en delete: {e}")
            return False
        
    @staticmethod
    def get_reparaciones_with_details(id_reparaciones):
        query = db.session.query(
            Reparaciones,
            Cliente,
            Dispositivo,
            Usuario
        ).join(
            Cliente, Reparaciones.id_cliente_reparaciones == Cliente.id_cliente
        ).join(
            Dispositivo, Reparaciones.id_dispositivo_reparaciones == Dispositivo.id_dispositivo
        ).join(
            Usuario, Reparaciones.id_usuario_reparaciones == Usuario.id_usuario
        ).filter(
            Reparaciones.id_reparaciones == id_reparaciones
        ).first()

        return query
