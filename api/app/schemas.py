from marshmallow import Schema, post_dump
from marshmallow import fields as serializacion
from .helper import remove_empty 


class ClienteSchemas(Schema):
    class Meta:
        fields = ('id_cliente', 'cedula_cliente', 'nombre_cliente', 'apellido_cliente', 'direccion_cliente', 'telefono_cliente', 'telefono2_cliente', 'correo_cliente')

      
class DispositivoSchemas(Schema):    
    class Meta:
        #ordered = True      
        fields = ('id_dispositivo', 'serial_dispositivo', 'marca', 'tipo', 'serial_cargador', "modelo") 
    

# aqui debe a ver una un nested entre dispositivo y cargador para tomar las propiedades de cargador y cargarlas en dispositivos para
# es decir hacer esto https://marshmallow.readthedocs.io/en/stable/nesting.html
# hice el cargue de migrations
# aca se realiza el cambio
""" ya lo intente de todas maneras no lo cargaba siempre me retorna el json pero solo con los datos del dispositivo
cuando revizo el objeto estan los datos """
     

class ProductoSchemas(Schema):    
    class Meta:        
        fields = ('id_producto','nombre_producto','codigo_producto', 'precio_compra_producto', 'precio_venta_producto', 'cantidad_producto', 'stock', 'detalle_producto', 'categoria')
       


class UsuarioSchemas(Schema):    
    class Meta:        
        fields = ('id_usuario', 'nombre_usuario', 'apellido_usuario', 'correo_usuario', 
                  'telefono_usuario', 'telefono2_usuario', 'direccion', 'token', 'perfil')
       
class ReparacionesSchemas(Schema):
    cliente = serializacion.Nested(ClienteSchemas)
    dispositivo = serializacion.Nested(DispositivoSchemas)
    usuario = serializacion.Nested(UsuarioSchemas)

    class Meta:
        fields = ('id_reparaciones','fecha', 'comentario','procedimientos', 'precio_reparacion', 'id_usuario_reparaciones', 'id_cliente_reparaciones', 'id_dispositivo_reparaciones')
        
    @post_dump(pass_many=True)
    def remove_empty(self, data, many, **kwargs):
        return remove_empty(data, many)  # Usa la función importada
       

class VentasSchema(Schema):
    # Relación anidada con el esquema de cliente
    cliente = serializacion.Nested(ClienteSchemas)    
    # Relación anidada con el esquema de usuario
    usuario = serializacion.Nested(UsuarioSchemas)
    
    class Meta:
        # Campos que se desean serializar
        fields = (
            'id_venta',
            'cliente',
            'usuario',
            'total_venta',
            'estado_venta',
            'fecha_venta'
        )

    @post_dump(pass_many=True)
    def remove_empty(self, data, many, **kwargs):
        return remove_empty(data, many)  # Usa la función importada 

class PermisoSchema(Schema):
    usuario = serializacion.Nested(UsuarioSchemas)   
    class Meta:
        fields = ('id_permiso', 'permiso', 'usuario_permiso','usuario')
    
    @post_dump(pass_many=True)
    def remove_empty(self, data, many, **kwargs):
        return remove_empty(data, many)  # Usa la función importada 

class DetallesVentasClienteProductoSchema(Schema):
    id_detalles_ventas = serializacion.Number()
    cedula_cliente = serializacion.String()
    nombre_cliente = serializacion.String()
    apellido_cliente = serializacion.String()
    direccion_cliente = serializacion.String()
    correo_cliente = serializacion.String()
    fecha_detalles_ventas = serializacion.DateTime()
    cantidad_detalles_ventas = serializacion.Number()
    precio_detalles_ventas = serializacion.Number()
    nombre_producto = serializacion.String()
        
    class Meta:
        fields = (
            'id_detalles_ventas',
            'cedula_cliente',
            'nombre_cliente',
            'apellido_cliente',
            'direccion_cliente',
            'correo_cliente',
            'fecha_detalles_ventas',
            'cantidad_detalles_ventas',
             'precio_detalles_ventas',        
            'nombre_producto'
        )

    

class Inventariochema(Schema):
    producto = serializacion.Nested(ProductoSchemas)   
    class Meta:
        fields = ('id_inventarios', 'entrada', 'fecha_inventario','salida','producto')
    
    @post_dump(pass_many=True)
    def remove_empty(self, data, many, **kwargs):
        return remove_empty(data, many)  # Usa la función importada 

    
   
class ProveedoresSchemas(Schema):
    class Meta:
        fields = ('id_proveedores', 'nit', 'telefono', 'direccion', 'estado')

class ComprasSchemas(Schema):
    usuario = serializacion.Nested(UsuarioSchemas)
    provedores = serializacion.Nested(ProveedoresSchemas)
    class Meta:
        fields = (
            'id_compras',           
            'total_compra',
            'fecha_compra',
            'metodo_pago',
            'usuario',
            'provedores'
        )
    @post_dump(pass_many=True)
    def remove_empty(self, data, many, **kwargs):
        return remove_empty(data, many) # Usa la función importada
    
class DetallesComprasSchemas(Schema):
    compras = serializacion.Nested(ComprasSchemas)
    producto = serializacion.Nested(ProductoSchemas)
    class Meta:
         fields = (
            'id_Detalles_compra',           
            'Cantidad_Detalles_compra',
            'Precio_Detalles_compra',          
            'compras',
            'producto'
        )
    @post_dump(pass_many=True)
    def remove_empty(self, data, many, **kwargs):
        return remove_empty(data, many) # Usa la función importada

class DetallesVentasSchemas(Schema):
    venta =  producto = serializacion.Nested(VentasSchema)
    producto = serializacion.Nested(ProductoSchemas)
    class Meta:
         fields = (
            'id_detalles_ventas',           
            'cantidad_detalles_ventas',
            'precio_detalles_ventas', 
            'fecha_detalles_ventas',         
            'venta',
            'producto'
        )
    @post_dump(pass_many=True)
    def remove_empty(self, data, many, **kwargs):
        return remove_empty(data, many) # Usa la función importada


class DetallesComprasWithDetailsSchemas(Schema):
    id_compras = serializacion.Number()
    fecha_compra = serializacion.DateTime()
    Cantidad_Detalles_compra = serializacion.Number()
    correo_usuario = serializacion.String()
    nombre_producto = serializacion.String()
    detalle_producto = serializacion.String()
    categoria = serializacion.String()
    nit = serializacion.String()
    telefono = serializacion.String()    
    class Meta:
        fields = (
            'id_compras',
            'fecha_compra',
            'Cantidad_Detalles_compra',
            'correo_usuario',
            'nombre_producto',
            'detalle_producto',
            'categoria',
            'nit',
            'telefono'
        )
    #@post_dump(pass_many=True)
    #def remove_empty(self, data, many, **kwargs):
        #return remove_empty(data, many) 
    
    
# --- serialization client ----- 
api_cliente  = ClienteSchemas()
api_clientes = ClienteSchemas(many=True)

# serialization usuario -------
api_Usuario = UsuarioSchemas()
api_Usuarios = UsuarioSchemas(many=True)

# serialization dispositivo -------
api_dispositivo = DispositivoSchemas()
api_dispositivos = DispositivoSchemas(many=True)

# serialization reparacion --------
api_reparacion = ReparacionesSchemas()
api_reparaciones = ReparacionesSchemas(many=True)

# serialization ventas --------
api_venta = VentasSchema()
api_ventas = VentasSchema(many=True)

# serialization producto --------
api_Producto = ProductoSchemas()
api_Productos = ProductoSchemas(many=True)

# serialization permiso --------
api_permiso = PermisoSchema()
api_permisos = PermisoSchema(many=True)

# serialization inventario --------
api_inventario  = Inventariochema()
api_inventarios = Inventariochema(many=True)

# serialization proveedores --------
api_proveedor  = ProveedoresSchemas()
api_proveedores = ProveedoresSchemas(many=True)

# serialization Compras ------------
api_compra  = ComprasSchemas()
api_compras = ComprasSchemas(many=True)


# serialization Detalles Compras ------------
api_detalles_compra  = DetallesComprasSchemas()
api_detalles_compras = DetallesComprasSchemas(many=True)
api_compra_details = DetallesComprasWithDetailsSchemas(many=True)


# serialization Detalles Ventas ------------
api_detalles_venta  = DetallesVentasSchemas()
api_detalles_ventas = DetallesVentasSchemas(many=True)


# Crear las instancias de serialización para API
api_detalles_ventas_cliente_producto = DetallesVentasClienteProductoSchema(many=True)



