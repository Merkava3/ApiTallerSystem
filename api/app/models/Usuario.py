from . import db
from sqlalchemy.exc import IntegrityError

class Usuario(db.Model):    
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_usuario = db.Column(db.String(20), nullable=False)
    apellido_usuario = db.Column(db.String(20), nullable=False)
    correo_usuario = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(8), nullable=False)
    telefono_usuario = db.Column(db.String(15), nullable=False)
    telefono2_usuario = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.String(80), nullable=False)
    token = db.Column(db.String(700), unique=True, nullable=False)
    perfil = db.Column(db.String(50), nullable=False)

    ventas = db.relationship('Ventas', back_populates='usuario')
    reparaciones_usuario = db.relationship('Reparaciones', back_populates='usuario')
    permiso_usuario = db.relationship('Permiso', back_populates='usuario')
    compras_usuario = db.relationship('Compras', back_populates='usuario')
    

    @staticmethod
    def get_user(correo_usuario):
        return Usuario.query.filter_by(correo_usuario=correo_usuario).first()

    @classmethod
    def new(cls, **kwargs):
        return Usuario(**kwargs)

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

    def __str__(self):
        return f"Usuario: {self.nombre_usuario} {self.apellido_usuario} - {self.correo_usuario}"
