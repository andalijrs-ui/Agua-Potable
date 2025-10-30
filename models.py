from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(20))
    fecha_alta = db.Column(db.DateTime, default=datetime.utcnow)
    nombre = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200), nullable=False)
    colonia = db.Column(db.String(100))
    manzana = db.Column(db.String(50))
    predio = db.Column(db.String(50))
    agua_potable = db.Column(db.Boolean, default=False)
    drenaje = db.Column(db.Boolean, default=False)
    medidor = db.Column(db.Boolean, default=False)
    tipo_uso = db.Column(db.String(50))
    observaciones = db.Column(db.Text)

# Ubicación
    razonsocial = db.Column(db.String(100))
    cia = db.Column(db.String(50))
    ciudad = db.Column(db.String(100))
    codigopostal = db.Column(db.String(10))
    nombrecompañia = db.Column(db.String(100))
    habitantes = db.Column(db.Integer)
    fechainstalacion = db.Column(db.Date)

# Servicios
    abastecimiento = db.Column(db.String(100))
    numtomas = db.Column(db.Integer)
    lecturainicial = db.Column(db.Float)
    numeromedidor = db.Column(db.String(50))

# Datos Técnicos
    materialbanqueta = db.Column(db.String(50))
    materialcalle = db.Column(db.String(50))
    capacidadcisternam2 = db.Column(db.Float)
    capacidadtinacolts = db.Column(db.Float)
    nummuebles = db.Column(db.Integer)
    aream2 = db.Column(db.Float)
    diametrodrenaje = db.Column(db.String(20))
    marcamedidor = db.Column(db.String(50))
    diametromedidor = db.Column(db.String(20))
    tipo = db.Column(db.String(50))
    anomalias = db.Column(db.Text)
    subsidio = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(50))

class Compania(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)

class Colonia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(100), nullable=True)
    codigo_postal = db.Column(db.String(10), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

class Consumo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo_uso = db.Column(db.String(15), nullable=False)  # D, C, I
    cuota_fija = db.Column(db.Float, nullable=False)
    consumo_basico = db.Column(db.Float)
    consumo_medio = db.Column(db.Float)
    consumo_alto = db.Column(db.Float)
    consumo_maximo = db.Column(db.Float)
    consumo_excesivo = db.Column(db.Float)
    consumo_aaa = db.Column(db.Float)
    precio_basico = db.Column(db.Float)
    precio_medio = db.Column(db.Float)
    precio_alto = db.Column(db.Float)
    precio_maximo = db.Column(db.Float)
    precio_excesivo = db.Column(db.Float)
    precio_aaa = db.Column(db.Float)
    ptje_int_moratorio = db.Column(db.Float)
    dias_tolerancia = db.Column(db.Integer)
    dia_limite_pago = db.Column(db.Integer)

class Concepto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    activo = db.Column(db.Boolean, default=True)

class Solicitante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_solicitante = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)

class Familia(db.Model):


    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)

class Grupos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    familia = db.Column(db.String(10), nullable=False)  # clave de la familia

class Material(db.Model):
    __tablename__ = 'materiales'

    id = db.Column(db.Integer, primary_key=True)
    clasificacion = db.Column(db.String(50), nullable=False)
    grupo = db.Column(db.String(50), nullable=False)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    um_compra = db.Column(db.String(20), nullable=False)
    um_salida = db.Column(db.String(20), nullable=False)
    factor = db.Column(db.Float, default=1.0)
    precio_compra = db.Column(db.Float, nullable=False)
    precio_salida = db.Column(db.Float, nullable=False)
    precio_publico = db.Column(db.Float, nullable=False)
    cantidad_unidad = db.Column(db.Float, default=1.0)
    existencias = db.Column(db.Integer, default=0)
    inventariado = db.Column(db.Boolean, default=True)
    fam = db.Column(db.String(3))
    gpo = db.Column(db.String(3))
    mat = db.Column(db.String(10))  

    def __repr__(self):
        return f"<Material {self.codigo}>"
    
class Tabulador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_grado = db.Column(db.String(10), unique=True, nullable=False)
    grado = db.Column(db.String(50), nullable=False)
    costo_hora = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Tabulador {self.numero_grado} - {self.grado}>'
