from . import db


class Cliente(db.Model):
    __tablename__ = 'cliente'
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cedula_cliente = db.Column(db.String(16), unique=True, nullable=False)
    nombre_cliente = db.Column(db.String(20), nullable=False)
    apellido_cliente = db.Column(db.String(20), nullable=False)
    direccion_cliente = db.Column(db.String(50), nullable=False)
    telefono_cliente = db.Column(db.String(15), nullable=False)    
    telefono2_cliente = db.Column(db.String(15), nullable=False)
    correo_cliente = db.Column(db.String(40),nullable=False)
    
    reparaciones_cliente = db.relationship('Reparaciones', back_populates='cliente')
    ventas_cliente = db.relationship('Ventas', back_populates='cliente')

    @staticmethod
    def get_cliente(id_cliente):
        return Cliente.query.filter_by(id_cliente=id_cliente).first()
    
    @classmethod
    def count_clients(cls):
        return db.session.query(db.func.count(cls.id_cliente)).scalar()
    
    @classmethod
    def get_last_three_clients(cls):      
        return cls.query.order_by(cls.id_cliente.desc()).limit(3).all()

    @classmethod
    def new(cls, kwargs):
        return Cliente(**kwargs)

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
