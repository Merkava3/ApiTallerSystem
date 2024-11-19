from . import db
from datetime import datetime


class cliente(db.Model):
    __tablename__ = 'cliente'
    # id
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cedula_cliente = db.Column(db.String(16), unique=True, nullable=False)
    nombre_cliente = db.Column(db.String(20), nullable=False)
    apellido_cliente = db.Column(db.String(20), nullable=False)
    direccion_cliente = db.Column(db.String(50), nullable=False)
    telefono_cliente = db.Column(db.String(15), nullable=False)    
    telefono2_cliente = db.Column(db.String(15), nullable=False)
    correo_cliente = db.Column(db.String(40), nullable=False)
    #def __str__(self):
        #return self.nombre    
    
    @staticmethod
    def get_cliente(id_cliente): # un objeto Cliente sdi existe, y si no Noe
        return cliente.query.filter_by(id_cliente=id_cliente).first()
    @classmethod
    def new(cls, kwargs):  # json to Task object
        #print(kwargs)  # dictionary
        return cliente(**kwargs)
    
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
        
        
class dispositivo(db.Model):
    __tablename__ = 'dispositivo'  
    id_dispositivo = db.Column(db.Integer, primary_key=True, autoincrement=True)     
    serial_dispositivo = db.Column(db.String(50), primary_key=True)
    marca = db.Column(db.String(30), nullable=False)    
    tipo = db.Column(db.String(30), nullable=False)
   
    @staticmethod
    def getDispositivo(serial_dispositivo): # un objeto Cliente sdi existe, y si no Noe
        return dispositivo.query.filter_by(serial_dispositivo=serial_dispositivo).first()
    
    @staticmethod
    def GetdispotivoCargador(serial_dispositivo):
        return db.session.query(dispositivo,reparaciones).join(dispositivo, dispositivo.serial_dispositivo == serial_dispositivo).first() 

    @classmethod
    def new(cls, kwargs):  # json to Task object
        #print(kwargs)  # dictionary
        return dispositivo(**kwargs)
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
        return self.serial_dispositivo
 
class usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario  =db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_usuario = db.Column(db.String(20), nullable=False)
    apellido_usuario = db.Column(db.String(20), nullable=False)
    correo_usuario = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(8), nullable=False)
    telefono_cliente = db.Column(db.String(15), nullable=False)
    telefono2_cliente = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.String(80), nullable=False)
    token = db.Column(db.String(700), nullable=False)
    perfil = db.Column(db.String(50), nullable=False)    
    
    
    @staticmethod
    def getReparacion(id_usuario):
        return usuario.query.filter_by(id_usuario=id_usuario).first()
    
    @staticmethod
    def Get(id_usuario):
        return db.session.query(usuario, dispositivo).join(usuario, usuario.id_usuario == id_usuario).first() 
    
    @classmethod
    def new(cls, kwargs):
        return usuario(**kwargs)
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
    
    def __str__(self):
        return self.id_usuario
        

class Permiso(db.Model):
    __tablename__ = 'permiso'
    id_permiso = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    permiso = db.Column(db.String(50), nullable=False)
    
    permiso_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))  # Foreign key should match the type and length of the referenced column
    usuario = db.relationship("usuario", backref=db.backref('permisos', lazy=True))  # Relationship with the Usuario model
    
   
    @staticmethod
    def getReparacion(id_permiso):
        return usuario.query.filter_by(id_permiso=id_permiso).first()
    
    @staticmethod
    def Get(id_usuario):
        return db.session.query(usuario, dispositivo).join(usuario, usuario.id_usuario == id_usuario).first() 
    
    @classmethod
    def new(cls, kwargs):
        return usuario(**kwargs)
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
    
    def __str__(self):
        return self.id_usuario
    
    
    
class productos(db.Model):
         _tablename__ = "productos"
         id_producto =  db.Column(db.Integer, primary_key=True, autoincrement=True)
         nombre_producto = db.Column(db.String(45), nullable=False)
         codigo_producto = db.Column(db.String(255), nullable=False)
         precio_compra_producto = db.Column(db.DECIMAL(10, 2), nullable=False)
         precio_venta_producto = db.Column(db.DECIMAL(10, 2), nullable=False)
         cantidad = db.Column(db.Integer, nullable=False)
         stock = db.Column(db.Integer, nullable=False)
         detalle = db.Column(db.String(45), nullable=False)
         categoria = db.Column(db.String(45), nullable=False)
         
         @staticmethod
         def get_compras(id_detalles_compra): # un objeto Cliente sdi existe, y si no Noe
            return compras.query.filter_by( id_detalles_compra= id_detalles_compra).first()
        
         @classmethod
         def new(cls, kwargs):  # json to Task object
            #print(kwargs)  # dictionary
            return compras(**kwargs)
        
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
                    
class reparaciones(db.Model):
    __tablename__ = 'reparaciones'
    id_reparaciones = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    comentario = db.Column(db.String(500), nullable=False)
    procedimientos = db.Column(db.String(500), nullable=False)
    precio_reparacion = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)

    # Foreign key to usuario
    id_usuario_reparaciones = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    usuario = db.relationship("Usuario", backref=db.backref('reparaciones', lazy=True))

    # Foreign key to cliente
    id_cliente_reparaciones = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), nullable=False)
    cliente = db.relationship("Cliente", backref=db.backref('reparaciones', lazy=True))

    # Foreign key to dispositivo
    id_dispositivo_reparaciones = db.Column(db.Integer, db.ForeignKey('dispositivo.id_dispositivo'), nullable=False)
    dispositivo = db.relationship("Dispositivo", backref=db.backref('reparaciones', lazy=True))

    @staticmethod
    def get_reparaciones(id_reparaciones):
        return  reparaciones.query.filter_by(id_reparaciones=id_reparaciones).first()

    @classmethod
    def new(cls, kwargs):
        return  reparaciones(**kwargs)

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

    
    
    
    
class proveedores(db.Model):
    _tablename__ = "proveedores"
    id_proveedores = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nit = db.Column(db.String(45), unique=True,nullable=False)
    telefono_proovedor = db.Column(db.String(15), nullable=False)
    direccion_proovedor = db.Column(db.String(80), nullable=False)
    estado = db.Column(db.Integer, nullable=False)
    
    @staticmethod
    def get_compras(id_proveedores ): # un objeto Cliente sdi existe, y si no Noe
        return compras.query.filter_by(id_proveedores=id_proveedores ).first()
    
    
    @classmethod
    def new(cls, kwargs):  # json to Task object
        #print(kwargs)  # dictionary
        return  proveedores(**kwargs)
    
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
    
class compras(db.Model):
    _tablename__ = "compras"
    id_compras = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    total_compra =  db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    feha_compra = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    metodo_pago =  db.Column(db.String(50), nullable=False)
    
    # compras - usuarios
    id_usuario_compras = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))  # serial_cargador
    usuario = db.relationship("usuario", backref=db.backref('usuario',lazy=True)) 
    
    # compras - proveedor
    id_proveedor_compras = db.Column(db.Integer, db.ForeignKey('proveedores.id_proveedores'))  # serial_cargador
    provedores = db.relationship("proveedores", backref=db.backref('proveedores',lazy=True)) 
    
    
    @staticmethod
    def get_compras(id_compras): # un objeto Cliente sdi existe, y si no Noe
        return compras.query.filter_by(id_compras=id_compras).first()
    
    @classmethod
    def new(cls, kwargs):  # json to Task object
        #print(kwargs)  # dictionary
        return compras(**kwargs)
    
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
        

        
    class detalles_compra(db.Model):
        _tablename__ = "detalles_compra"
        id_detalles_compra =  db.Column(db.Integer, primary_key=True, autoincrement=True)
        cantidad = db.Column(db.Integer,  nullable=False)
        precio = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
        # compras - detalles compra
        compras_detalles_compra = db.Column(db.Integer, db.ForeignKey('compras.id_compras'))  # serial_cargador
        compras = db.relationship("compras", backref=db.backref('compras',lazy=True))
        
        # detalles_compras - producto
        compras_detalles_productos = db.Column(db.Integer, db.ForeignKey('productos.id_producto'))  # serial_cargador
        productos = db.relationship("productos", backref=db.backref('productos',lazy=True))
        
        @staticmethod
        def get_compras( id_detalles_compra): # un objeto Cliente sdi existe, y si no Noe
            return compras.query.filter_by( id_detalles_compra= id_detalles_compra).first()
        
        @classmethod
        def new(cls, kwargs):  # json to Task object
            #print(kwargs)  # dictionary
            return compras(**kwargs)
        
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
 
         
         
    class venta(db.Model):
          __tablename__ = 'venta'
          id_venta = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
          id_usuario_venta = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))  # serial_cargador
          usuario = db.relationship("usuario", backref=db.backref('usuario',lazy=True))
          id_cliente_reparaciones = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), nullable=False) 
          reparacion = db.relationship("cliente",backref = db.backref('cliente',lazy=True))          
          total = db.Column(db.DECIMAL(10, 2), nullable=False)
          estado = db.Column(db.Integer, nullable=False)
          fecha_venta = db.Column(db.Date, default=datetime.utcnow)
          
          @staticmethod
          def get_compras(id_detalles_compra): # un objeto Cliente sdi existe, y si no Noe
            return compras.query.filter_by( id_detalles_compra= id_detalles_compra).first()
        
          @classmethod
          def new(cls, kwargs):  # json to Task object
            #print(kwargs)  # dictionary
            return compras(**kwargs)
        
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
            
    class detalles_venta(db.Model):
        __tablename__ = 'detalles_venta'
        id_detalles_venta = db.Column(db.Integer, primary_key=True, autoincrement=True)
        cantidad = db.Column(db.DECIMAL(10, 2), nullable=False)
        precio = db.Column(db.DECIMAL(10, 2), nullable=False)
        fecha_detalles_venta = db.Column(db.Date, default=datetime.utcnow)
        
        # detalles_venta - ventas
        venta_detalles_venta = db.Column(db.Integer, db.ForeignKey('venta.id_venta'))  # serial_cargador
        venta = db.relationship("venta", backref=db.backref('venta',lazy=True)) 
        
         # detalles_venta - productos
        producto_detalles_venta = db.Column(db.Integer, db.ForeignKey('productos.id_producto'))  # serial_cargador
        productos = db.relationship("productos", backref=db.backref('productos',lazy=True)) 
        
        
        @staticmethod
        def get_compras(id_detalles_venta): # un objeto Cliente sdi existe, y si no Noe
            return compras.query.filter_by( id_detalles_venta=id_detalles_venta).first()
        
        @classmethod
        def new(cls, kwargs):  # json to Task object
            #print(kwargs)  # dictionary
            return compras(**kwargs)
        
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
            
    class inventario :
        __tablename__ = 'inventario'
        id_inventario =  db.Column(db.Integer, primary_key=True, autoincrement=True)
        fecha =  db.Column(db.Date, default=datetime.utcnow, nullable=False)
        entrada = db.Column(db.DECIMAL(10, 2), nullable=False)
        salida = db.Column(db.Date, default=datetime.utcnow, nullable=False)
        
        producto_iventario = db.Column(db.Integer, db.ForeignKey('productos.id_productos'))  # serial_cargador
        productos = db.relationship("productos", backref=db.backref('productos',lazy=True)) 
        
        @staticmethod
        def get_compras(id_detalles_venta): # un objeto Cliente sdi existe, y si no Noe
            return compras.query.filter_by( id_detalles_venta=id_detalles_venta).first()
        
        @classmethod
        def new(cls, kwargs):  # json to Task object
            #print(kwargs)  # dictionary
            return compras(**kwargs)
        
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
        
         
           
           
        

    
     
    
    
    
    
    
    