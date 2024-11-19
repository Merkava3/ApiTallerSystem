from . import db

class Proveedores(db.Model):
    __tablename__ = 'proveedores'
    id_proveedores = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    nit = db.Column(db.String(45),  unique=True,nullable=False)
    telefono = db.Column(db.String(15),  unique=True, nullable=False)
    direccion = db.Column(db.String(80), nullable=False)
    estado = db.Column(db.Integer, nullable=False)    
    compras_proveedores = db.relationship('Compras', back_populates='proveedores') 
    
    @staticmethod
    def get_proveedores(nit):
        return Proveedores.query.filter_by(nit=nit).first()
       
    @classmethod
    def new(cls, kwargs):
        return Proveedores(**kwargs)
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()  # Deshacer cambios en caso de error
            print(f"Error en save: {e}")  # Imprimir detalles del error
            return False 
            
    def delete(self):
            try:
                db.session.delete(self)
                db.session.commit()
                return True
            except:
                return False
            
    def __str__(self):
        return self.nit