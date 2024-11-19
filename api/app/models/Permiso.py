from . import db
from .Usuario import Usuario

class Permiso(db.Model):
    __tablename__ = 'permiso'
    id_permiso =  db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)   
    permiso = db.Column(db.String(45), nullable=False)
    
    usuario_permiso = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    usuario = db.relationship('Usuario', back_populates='permiso_usuario')
    
    @staticmethod
    def get_permiso(usuario_permiso):
        return Permiso.query.filter_by(usuario_permiso=usuario_permiso).first()
    
       
    @classmethod
    def new(cls, kwargs):
        return  Permiso(**kwargs)
    
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
        return self.id_permiso
    
    @staticmethod
    def get_permisos_by_user_email(correo_usuario):
        query = db.session.query(
            Permiso,
            Usuario
        ).join(
            Usuario, Permiso.usuario_permiso == Usuario.id_usuario
        ).filter(
            Usuario.correo_usuario == correo_usuario
        ).all()
        return query
    