from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from . import db

class Dispositivo(db.Model):
    __tablename__ = 'dispositivo'  
    id_dispositivo = db.Column(db.Integer, primary_key=True, autoincrement=True)   
    serial_dispositivo = db.Column(db.String(50), unique=True, nullable=False)
    marca = db.Column(db.String(30), nullable=False)    
    tipo = db.Column(db.String(30), nullable=False)  # Ej. portatil
    cargador = db.Column(db.Enum('Si', 'No', name='cargador_enum'), nullable=False)
    serial_cargador = db.Column(db.String(50), nullable=False)    
    modelo = db.Column(db.String(50), nullable=False)  # Ej. portatil alinwerae
    
    reparaciones_dispositivo = db.relationship('Reparaciones', back_populates='dispositivo')
   
    @staticmethod
    def get_dispositivo(serial_dispositivo):  # Método estático para obtener un dispositivo por su serial
        return Dispositivo.query.filter_by(serial_dispositivo=serial_dispositivo).first()    

    @classmethod
    def new(cls, kwargs):  # Convierte un diccionario en un objeto Dispositivo
        return Dispositivo(**kwargs)
    
    @staticmethod
    def get_all():
        """Obtiene todos los dispositivos almacenados en la base de datos."""
        return Dispositivo.query.all()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()  # Deshace la transacción en caso de error
            print(f"Error en save: {e}")  # Imprime el error para depuración
            return False

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()  # Deshace la transacción en caso de error
            print(f"Error en delete: {e}")  # Imprime el error para depuración
            return False
    
    def __str__(self):
        return self.serial_dispositivo
