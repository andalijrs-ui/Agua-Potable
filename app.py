from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Usuario
from datetime import datetime
from flask import jsonify
from flask_migrate import Migrate
from models import Compania, Colonia, Concepto,Consumo, Solicitante, Familia, Grupos, Material, Tabulador


import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Para sistemas Linux/macOS
app = Flask(__name__)
print(app.url_map)
app.config['SECRET_KEY'] = 'clave'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema_agua.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)

with app.app_context():
    db.create_all()
import sqlite3
import sqlite3

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rutas')
def mostrar_rutas():
    return '<br>'.join(str(rule) for rule in app.url_map.iter_rules())

#METODO CATALOGO GENERAL
@app.route('/catalogo')
def catalogo():
    tipo = request.args.get('catalogo')

    if tipo == 'companias':
        return redirect(url_for('agregar_compania'))
    elif tipo == 'colonias':
        return redirect(url_for('listar_colonias'))
    elif tipo == 'usuarios':
        return redirect(url_for('listar_usuarios'))
    elif tipo == 'consumos':
        return redirect(url_for('nuevo_consumo')) 
    elif tipo == 'conceptos':
        return redirect(url_for('nuevo_concepto'))
    elif tipo == 'solicitante':
        return redirect(url_for('form_solicitante'))
    elif tipo == 'familias':
        return redirect(url_for('form_familia'))
    elif tipo == 'grupos':
        return redirect(url_for('form_grupo'))
    elif tipo == 'materiales':
        return redirect(url_for('form_material'))
    elif tipo == 'tabuladores':
        return redirect(url_for('catalogo_tabulador'))
    elif tipo == 'unidad_medida':
        return redirect(url_for('mostrar_catalogo'))

    return render_template('catalogo_general.html')

# METODOS CATALOGO USUARIO
@app.route('/usuarios/nuevo', methods=['GET', 'POST'])
def agregar_usuario():
    mensaje = None
    print("Ruta /usuarios/nuevo activada")

    if request.method == 'POST':
        # Captura de datos del formulario
        nombre = request.form['nombre']
        apellido_paterno = request.form['apellido_paterno']
        apellido_materno = request.form['apellido_materno']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        colonia = request.form['colonia']
        manzana = request.form['manzana']
        predio = request.form['predio']
        agua_potable = 'agua_potable' in request.form
        drenaje = 'drenaje' in request.form
        medidor = 'medidor' in request.form
        tipo_uso = request.form['tipo_uso']
        observaciones = request.form['observaciones']
        razonsocial = request.form.get('razonsocial', '')
        cia = request.form['cia']
        ciudad = request.form['ciudad']
        codigopostal = request.form['codigopostal']
        nombrecompañia = request.form['nombrecompañia']
        fechainstalacion = request.form['fechainstalacion']
        lecturainicial_raw = request.form.get('lecturainicial', '')
        abastecimiento = request.form['abastecimiento']
        numeromedidor = request.form.get('numeromedidor', '')
        materialbanqueta = request.form.get('materialbanqueta', '')
        materialcalle = request.form.get('materialcalle', '')
        capacidadcisternam2_raw = request.form.get('capacidadcisternam2', '')
        capacidadtinacolts_raw = request.form.get('capacidadtinacolts', '')
        aream2_raw = request.form.get('aream2', '')
        habitantes_raw = request.form.get('habitantes', '')
        numtomas_raw = request.form.get('numtomas', '')
        nummuebles_raw = request.form.get('nummuebles', '')
        diametrodrenaje = request.form['diametrodrenaje']
        marcamedidor = request.form['marcamedidor']
        diametromedidor = request.form['diametromedidor']
        tipo = request.form['tipo']
        anomalias = request.form['anomalias']
        subsidio = 'subsidio' in request.form
        status = request.form['status']

        def safe_float(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0.0

        def safe_int(value):
            try:
                return int(value)
            except (ValueError, TypeError):
                return 0

        lecturainicial = safe_float(lecturainicial_raw)
        capacidadcisternam2 = safe_float(capacidadcisternam2_raw)
        capacidadtinacolts = safe_float(capacidadtinacolts_raw)
        aream2 = safe_float(aream2_raw)
        habitantes = safe_int(habitantes_raw)
        numtomas = safe_int(numtomas_raw)
        nummuebles = safe_int(nummuebles_raw)

        # Verificar si el usuario ya existe
        existente = Usuario.query.filter_by(
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno
        ).first()


        if existente:
            folio = existente.folio
        else:
            fecha_actual = datetime.utcnow().strftime('%Y%m%d')
            folios_existentes = db.session.query(Usuario.folio).distinct().count()
            folio = f'USU-{fecha_actual}-{folios_existentes + 1:03d}'


        nuevo_usuario = Usuario(
            folio=folio,
            fecha_alta=datetime.utcnow(),
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            telefono=telefono,
            direccion=direccion,
            colonia=colonia,
            manzana=manzana,
            predio=predio,
            agua_potable=agua_potable,
            drenaje=drenaje,
            medidor=medidor,
            tipo_uso=tipo_uso,
            observaciones=observaciones,
            razonsocial=razonsocial,
            cia=cia,
            codigopostal=codigopostal,
            ciudad=ciudad,
            nombrecompañia=nombrecompañia,
            habitantes=habitantes,
            fechainstalacion=datetime.utcnow(),
            abastecimiento=abastecimiento,
            numtomas=numtomas,
            lecturainicial=lecturainicial,
            numeromedidor=numeromedidor,
            materialbanqueta=materialbanqueta,
            materialcalle=materialcalle,
            capacidadcisternam2=capacidadcisternam2,
            capacidadtinacolts=capacidadtinacolts,
            nummuebles=nummuebles,
            aream2=aream2,
            diametrodrenaje=diametrodrenaje,
            marcamedidor=marcamedidor,
            diametromedidor=diametromedidor,
            tipo=tipo,
            anomalias=anomalias,
            subsidio=subsidio,
            status=status
            )

        db.session.add(nuevo_usuario)
        db.session.commit()
        return redirect('/usuarios?guardado=ok')

    return render_template('usuario/form_usuario.html', mensaje=mensaje)
@app.route('/usuarios')
def listar_usuarios():
    colonia = request.args.get('colonia')
    tipo_uso = request.args.get('tipo_uso')
    fecha_alta = request.args.get('fecha_alta')

    query = Usuario.query

    if colonia:
        query = query.filter(Usuario.colonia.ilike(f"%{colonia}%"))
    if tipo_uso:
        query = query.filter_by(tipo_uso=tipo_uso)
    if fecha_alta:
        try:
            fecha_obj = datetime.strptime(fecha_alta, '%Y-%m-%d')
            query = query.filter(db.func.date(Usuario.fecha_alta) == fecha_obj.date())
        except ValueError:
            pass  # Ignora si la fecha no es válida

    usuarios = Usuario.query.all()

    return render_template('usuario/lista_usuarios.html', usuarios=usuarios)
@app.route('/usuarios/buscar')
def buscar_usuarios():
    folio = request.args.get('folio')
    nombre = request.args.get('nombre')
    apellido_paterno = request.args.get('apellido_paterno')
    apellido_materno = request.args.get('apellido_materno')
    colonia = request.args.get('colonia')
    fecha_alta = request.args.get('fecha_alta')

    query = Usuario.query

    if folio:
        query = query.filter(Usuario.folio.ilike(f"%{folio}%"))
    if nombre:
        query = query.filter(Usuario.nombre.ilike(f"%{nombre}%"))
    if apellido_paterno:
        query = query.filter(Usuario.apellido_paterno.ilike(f"%{apellido_paterno}%"))
    if apellido_materno:
        query = query.filter(Usuario.apellido_materno.ilike(f"%{apellido_materno}%"))
    if colonia:
        query = query.filter(Usuario.colonia.ilike(f"%{colonia}%"))
    if fecha_alta:
        try:
            fecha_obj = datetime.strptime(fecha_alta, '%Y-%m-%d')
            query = query.filter(db.func.date(Usuario.fecha_alta) == fecha_obj.date())
        except ValueError:
            pass

    usuarios = query.all()

    resultados = []
    for u in usuarios:
        resultados.append({
            'id': u.id,
        'folio': u.folio,
        'nombre': u.nombre,
        'apellido_paterno': u.apellido_paterno,
        'apellido_materno': u.apellido_materno,
        'telefono': u.telefono,
        'direccion': u.direccion,
        'colonia': u.colonia,
        'manzana': u.manzana,
        'predio': u.predio,
        'agua_potable': u.agua_potable,
        'drenaje': u.drenaje,
        'medidor': u.medidor,
        'tipo_uso': u.tipo_uso,
        'observaciones': u.observaciones,
        'razonsocial': u.razonsocial,
        'cia': u.cia,
        'ciudad': u.ciudad,
        'codigopostal': u.codigopostal,
        'nombrecompañia': u.nombrecompañia,
        'habitantes': u.habitantes,
        'fechainstalacion': u.fechainstalacion.strftime('%d/%m/%Y') if u.fechainstalacion else '',
        'abastecimiento': u.abastecimiento,
        'numtomas': u.numtomas,
        'lecturainicial': u.lecturainicial,
        'numeromedidor': u.numeromedidor,
        'materialbanqueta': u.materialbanqueta,
        'materialcalle': u.materialcalle,
        'capacidadcisternam2': u.capacidadcisternam2,
        'capacidadtinacolts': u.capacidadtinacolts,
        'nummuebles': u.nummuebles,
        'aream2': u.aream2,
        'diametrodrenaje': u.diametrodrenaje,
        'marcamedidor': u.marcamedidor,
        'diametromedidor': u.diametromedidor,
        'tipo': u.tipo,
        'anomalias': u.anomalias,
        'subsidio': u.subsidio,
        'status': u.status,
        'fecha_alta': u.fecha_alta.strftime('%d/%m/%Y') if u.fecha_alta else ''
        })

    return jsonify(resultados)    
@app.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    mensaje = None

    if request.method == 'POST':
        usuario.folio = request.form['folio']
        usuario.nombre = request.form['nombre']
        usuario.apellido_paterno = request.form['apellido_paterno']
        usuario.colonia = request.form['colonia']
        usuario.tipo_uso = request.form['tipo_uso']
        usuario.fecha_alta = datetime.strptime(request.form['fecha_alta'], '%Y-%m-%d')

        db.session.commit()
        return redirect('/usuarios?modificado=ok')

    return render_template('usuario/editar_usuario.html', usuario=usuario, mensaje=mensaje)
@app.route('/usuarios/<int:id>/eliminar')
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect('/usuarios?eliminado=ok')



#METODOS CATALOGO COMPAÑIAS
@app.route('/agregarcompania', methods=['GET', 'POST'])
def agregar_compania():
    mensaje = None

    if request.method == 'POST':
        numero = request.form['numero']
        nombre = request.form['nombre']

        if not numero or not nombre:
            mensaje = "Todos los campos son obligatorios."
        else:
            existente = Compania.query.filter_by(numero=numero).first()
            if existente:
                mensaje = "Ya existe una compañía con ese número."
            else:
                nueva = Compania(numero=numero, nombre=nombre)
                db.session.add(nueva)
                db.session.commit()
                return redirect('/agregarcompania?guardado=ok')

    if request.args.get('guardado') == 'ok':
        mensaje = "✅ Compañía guardada con éxito."

    companias = Compania.query.order_by(Compania.numero).all()
    return render_template('compañia/agregarcompania.html', companias=companias, mensaje=mensaje)
@app.route('/compania/editar/<int:id>', methods=['GET', 'POST'])
def editar_compania(id):
    compania = Compania.query.get_or_404(id)
    mensaje = None

    if request.method == 'POST':
        nuevo_numero = request.form['numero']
        nuevo_nombre = request.form['nombre']

        if not nuevo_numero or not nuevo_nombre:
            mensaje = "Todos los campos son obligatorios."
        else:
            # Verifica si el número ya existe en otra compañía
            existente = Compania.query.filter(Compania.numero == nuevo_numero, Compania.id != id).first()
            if existente:
                mensaje = "Ya existe otra compañía con ese número."
            else:
                compania.numero = nuevo_numero
                compania.nombre = nuevo_nombre
                db.session.commit()
                return redirect('/agregarcompania?modificado=ok')

    return render_template('compañia/editarcompania.html', compania=compania, mensaje=mensaje)
@app.route('/compania/eliminar/<int:id>')
def eliminar_compania(id):
    compania = Compania.query.get_or_404(id)
    db.session.delete(compania)
    db.session.commit()
    return redirect('/agregarcompania?eliminado=ok')



#METODOS CATALOGO COLONIAS
@app.route('/colonias')
def listar_colonias():
    colonias = Colonia.query.order_by(Colonia.fecha_registro.desc()).all()
    return render_template('colonia/lista_colonias.html', colonias=colonias)
@app.route('/colonias/nueva', methods=['GET', 'POST'])
def agregar_colonia():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ciudad = request.form.get('ciudad', '')
        codigo_postal = request.form.get('codigo_postal', '')

        nueva = Colonia(nombre=nombre, ciudad=ciudad, codigo_postal=codigo_postal)
        db.session.add(nueva)
        db.session.commit()
        return redirect(url_for('listar_colonias', guardado='ok'))

    return render_template('colonia/agregar_colonia.html')
@app.route('/colonias/editar/<int:id>', methods=['GET', 'POST'])
def editar_colonia(id):
    colonia = Colonia.query.get_or_404(id)

    if request.method == 'POST':
        colonia.nombre = request.form['nombre']
        colonia.ciudad = request.form['ciudad']
        colonia.codigo_postal = request.form['codigo_postal']
        db.session.commit()
        return redirect(url_for('listar_colonias'))

    return render_template('colonia/editar_colonia.html', colonia=colonia)
@app.route('/colonias/eliminar/<int:id>')
def eliminar_colonia(id):
    colonia = Colonia.query.get_or_404(id)
    db.session.delete(colonia)
    db.session.commit()
    return redirect(url_for('listar_colonias', eliminado='ok'))



#METODOS CATALOGO CONSUMOS
def parse_float(value):
    return float(value) if value.strip() != '' else 0.0
@app.route('/consumos/nuevo', methods=['GET', 'POST'])
def nuevo_consumo():
    if request.method == 'POST':
        nuevo = Consumo(
            tipo_uso=request.form['tipo_uso'],
            cuota_fija=parse_float(request.form['cuota_fija']),
            consumo_basico=parse_float(request.form['consumo_basico']),
            consumo_medio=parse_float(request.form['consumo_medio']),
            consumo_alto=parse_float(request.form['consumo_alto']),
            consumo_maximo=parse_float(request.form['consumo_maximo']),
            consumo_excesivo=parse_float(request.form['consumo_excesivo']),
            consumo_aaa=parse_float(request.form['consumo_aaa']),
            precio_basico=parse_float(request.form['precio_basico']),
            precio_medio=parse_float(request.form['precio_medio']),
            precio_alto=parse_float(request.form['precio_alto']),
            precio_maximo=parse_float(request.form['precio_maximo']),
            precio_excesivo=parse_float(request.form['precio_excesivo']),
            precio_aaa=parse_float(request.form['precio_aaa']),
            ptje_int_moratorio=parse_float(request.form['ptje_int_moratorio']) / 100,
            dias_tolerancia=int(request.form['dias_tolerancia'] or 0),
            dia_limite_pago=int(request.form['dia_limite_pago'] or 0)
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('✅ Consumo registrado con éxito.', 'success')
        return redirect(url_for('nuevo_consumo'))  # ← redirige después de guardar

    consumos = Consumo.query.order_by(Consumo.id.desc()).all()
    return render_template('consumos/form_consumo.html', consumos=consumos)
@app.route('/consumos/editar/<int:id>', methods=['GET', 'POST'])
def editar_consumo(id):
    consumo = Consumo.query.get_or_404(id)

    if request.method == 'POST':
        consumo.tipo_uso = request.form['tipo_uso']
        consumo.cuota_fija = parse_float(request.form['cuota_fija'])
        consumo.consumo_medio = parse_float(request.form['consumo_medio'])
        consumo.precio_medio = parse_float(request.form['precio_medio'])
        consumo.consumo_alto = parse_float(request.form['consumo_alto'])
        consumo.precio_alto = parse_float(request.form['precio_alto'])
        consumo.consumo_maximo = parse_float(request.form['consumo_maximo'])
        consumo.precio_maximo = parse_float(request.form['precio_maximo'])
        consumo.consumo_excesivo = parse_float(request.form['consumo_excesivo'])
        consumo.precio_excesivo = parse_float(request.form['precio_excesivo'])
        consumo.consumo_aaa = parse_float(request.form['consumo_aaa'])
        consumo.precio_aaa = parse_float(request.form['precio_aaa'])
        consumo.ptje_int_moratorio = parse_float(request.form['ptje_int_moratorio']) / 100
        consumo.dias_tolerancia = int(request.form['dias_tolerancia'] or 0)
        consumo.dia_limite_pago = int(request.form['dia_limite_pago'] or 0)

        db.session.commit()
        flash('✏️ Consumo actualizado correctamente.', 'success')
        return redirect(url_for('nuevo_consumo'))

    return render_template('consumos/editar_consumo.html', consumo=consumo, consumos=Consumo.query.order_by(Consumo.id.desc()).all())
@app.route('/consumos/eliminar/<int:id>')
def eliminar_consumo(id):
    consumo = Consumo.query.get_or_404(id)
    db.session.delete(consumo)
    db.session.commit()
    flash('🗑️ Consumo eliminado correctamente.', 'success')
    return redirect(url_for('nuevo_consumo'))



#MODELO CATALOGO CONCEPTO
@app.route('/conceptos/nuevo', methods=['GET', 'POST'])
def nuevo_concepto():
    if request.method == 'POST':
        concepto = Concepto(
            clave=request.form['clave'],
            nombre=request.form['nombre'],
            tipo=request.form['tipo']
        )
        db.session.add(concepto)
        db.session.commit()
        flash('✅ Concepto registrado con éxito.', 'success')
        return redirect(url_for('nuevo_concepto'))  # ← POST-Redirect-GET

    conceptos = Concepto.query.order_by(Concepto.id.desc()).all()
    return render_template('conceptos/form_concepto.html', concepto=None, conceptos=conceptos)
@app.route('/conceptos/editar/<int:id>', methods=['GET', 'POST'])
def editar_concepto(id):
    concepto = Concepto.query.get_or_404(id)

    if request.method == 'POST':
        concepto.clave = request.form['clave']
        concepto.nombre = request.form['nombre']
        concepto.tipo = request.form['tipo']
        db.session.commit()
        flash('✏️ Concepto actualizado.', 'success')
        return redirect(url_for('nuevo_concepto'))

    conceptos = Concepto.query.order_by(Concepto.id.desc()).all()
    return render_template('conceptos/form_concepto.html', concepto=concepto, conceptos=conceptos)
@app.route('/conceptos/eliminar/<int:id>')
def eliminar_concepto(id):
    concepto = Concepto.query.get_or_404(id)
    db.session.delete(concepto)
    db.session.commit()
    flash('🗑️ Concepto eliminado.', 'success')
    return redirect(url_for('nuevo_concepto'))



#MODELO DE CATALOGO SOLICITANTE 
@app.route('/solicitantes', methods=['GET', 'POST'])
def form_solicitante():
    if request.method == 'POST':
        nuevo = Solicitante(
            id_solicitante=request.form['id_solicitante'],
            nombre=request.form['nombre']
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('✅ Solicitante agregado con éxito.', 'success')
        return redirect(url_for('form_solicitante'))

    solicitantes = Solicitante.query.order_by(Solicitante.id.asc()).all()
    return render_template('form_solicitante.html', solicitante=None, solicitantes=solicitantes)
@app.route('/solicitantes/editar/<int:id>', methods=['GET', 'POST'])
def editar_solicitante(id):
    solicitante = Solicitante.query.get_or_404(id)

    if request.method == 'POST':
        solicitante.id_solicitante = request.form['id_solicitante']
        solicitante.nombre = request.form['nombre']
        db.session.commit()
        flash('✏️ Solicitante actualizado.', 'success')
        return redirect(url_for('form_solicitante'))

    solicitantes = Solicitante.query.order_by(Solicitante.id.asc()).all()
    return render_template('form_solicitante.html', solicitante=solicitante, solicitantes=solicitantes)
@app.route('/solicitantes/eliminar/<int:id>')
def eliminar_solicitante(id):
    solicitante = Solicitante.query.get_or_404(id)
    db.session.delete(solicitante)
    db.session.commit()
    flash('🗑️ Solicitante eliminado.', 'success')
    return redirect(url_for('form_solicitante'))



#MODELO DE CATALOGO FAMILIAS
@app.route('/familias', methods=['GET', 'POST'])
def form_familia():
    if request.method == 'POST':
        nueva = Familia(
            clave=request.form['clave'],
            nombre=request.form['nombre']
        )
        db.session.add(nueva)
        db.session.commit()
        flash('✅ Familia agregada con éxito.', 'success')
        return redirect(url_for('form_familia'))

    familias = Familia.query.order_by(Familia.clave.asc()).all()
    return render_template('form_familia.html', familia=None, familias=familias)
@app.route('/familias/editar/<int:id>', methods=['GET', 'POST'])
def editar_familia(id):
    familia = Familia.query.get_or_404(id)

    if request.method == 'POST':
        familia.clave = request.form['clave']
        familia.nombre = request.form['nombre']
        db.session.commit()
        flash('✏️ Familia actualizada.', 'success')
        return redirect(url_for('form_familia'))

    familias = Familia.query.order_by(Familia.clave.asc()).all()
    return render_template('form_familia.html', familia=familia, familias=familias)
@app.route('/familias/eliminar/<int:id>')
def eliminar_familia(id):
    familia = Familia.query.get_or_404(id)
    db.session.delete(familia)
    db.session.commit()
    flash('🗑️ Familia eliminada.', 'success')
    return redirect(url_for('form_familia'))



#MODELO DE CATALOGO GRUPOS
@app.route('/grupos', methods=['GET', 'POST'])
def form_grupo():
    familias = Familia.query.order_by(Familia.clave).all()

    if request.method == 'POST':
        nuevo = Grupos(
            codigo=request.form['codigo'],
            nombre=request.form['nombre'],
            familia=request.form['familia']
        )
        db.session.add(nuevo)
        db.session.commit()
        flash('✅ Grupo agregado con éxito.', 'success')
        return redirect(url_for('form_grupo'))

    grupos = Grupos.query.order_by(Grupos.codigo).all()
    return render_template('form_grupo.html', grupo=None, grupos=grupos, familias=familias)
@app.route('/grupos/editar/<int:id>', methods=['GET', 'POST'])
def editar_grupo(id):
    grupo = Grupos.query.get_or_404(id)
    familias = Familia.query.order_by(Familia.clave).all()

    if request.method == 'POST':
        grupo.codigo = request.form['codigo']
        grupo.nombre = request.form['nombre']
        grupo.familia = request.form['familia']
        db.session.commit()
        flash('✏️ Grupo actualizado.', 'success')
        return redirect(url_for('form_grupo'))

    grupos = Grupos.query.order_by(Grupos.codigo).all()
    return render_template('form_grupo.html', grupo=grupo, grupos=grupos, familias=familias)
@app.route('/grupos/eliminar/<int:id>')
def eliminar_grupo(id):
    grupo = Grupos.query.get_or_404(id)
    db.session.delete(grupo)
    db.session.commit()
    flash('🗑️ Grupo eliminado.', 'success')
    return redirect(url_for('form_grupo'))



#MODELO DE CATALOGO DE MATERIALES
@app.route('/form-material')
def form_material():
    materiales = Material.query.all()
    return render_template('form_material.html', materiales=materiales)
@app.route('/guardar-material', methods=['POST'])
def guardar_material():
    nuevo = Material(
        clasificacion = request.form.get('clasificacion', ''),
        fam = request.form.get('fam'),
        gpo = request.form.get('gpo'),
        mat = request.form.get('codigoMat'),
        grupo=request.form['grupo'],
        codigo = request.form.get('codigoMat', ''),
        nombre=request.form['material'],
        um_compra=request.form['umCompra'],
        um_salida=request.form['umSalida'],
        precio_compra=float(request.form['precioCompra']),
        precio_salida=float(request.form['precioSalida']),
        precio_publico=float(request.form['precioPublico']),
        cantidad_unidad = float(request.form.get('cantidadUnidad', 1.0)),
        existencias = int(request.form.get('existencias', 0)),
        inventariado = 'inventariado' in request.form
    )
    db.session.add(nuevo)
    db.session.commit()
    flash('Material guardado correctamente')
    return redirect(url_for('form_material'))
@app.route('/editar-material/<int:id>', methods=['GET', 'POST'])
def editar_material(id):
    material = Material.query.get_or_404(id)
    if request.method == 'POST':
        material.nombre = request.form['material']
        material.um_compra = request.form['umCompra']
        material.um_salida = request.form['umSalida']
        material.precio_compra = float(request.form['precioCompra'])
        material.precio_salida = float(request.form['precioSalida'])
        material.precio_publico = float(request.form['precioPublico'])
        material.cantidad_unidad = float(request.form.get('cantidadUnidad', 1.0))
        material.existencias = int(request.form.get('existencias', 0))
        material.inventariado = 'inventariado' in request.form
        db.session.commit()
        flash('Material actualizado correctamente')
        return redirect(url_for('form_material'))
    return render_template('editar_material.html', material=material)
@app.route('/eliminar-material/<int:id>')
def eliminar_material(id):
    material = Material.query.get_or_404(id)
    db.session.delete(material)
    db.session.commit()
    flash('Material eliminado correctamente')
    return redirect(url_for('form_material'))

#MODELO DE CATALAGO DE PROVEEDORES





# Mostrar catálogo
@app.route('/tabulador')
def catalogo_tabulador():
    tabuladores = Tabulador.query.order_by(Tabulador.numero_grado).all()
    return render_template('tabulador/catalogo_tabulador.html', tabuladores=tabuladores)

# Agregar registro
@app.route('/tabulador/agregar', methods=['POST'])
def agregar_tabulador():
    nuevo = Tabulador(
        numero_grado=request.form['numero_grado'],
        grado=request.form['grado'],
        costo_hora=float(request.form['costo_hora'])
    )
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('catalogo_tabulador'))

@app.route('/tabulador/editar/<int:id>')
def editar_tabulador(id):
    editar = Tabulador.query.get_or_404(id)
    tabuladores = Tabulador.query.order_by(Tabulador.numero_grado).all()
    return render_template('tabulador/catalogo_tabulador.html',
                           tabuladores=tabuladores,
                           editar=editar)

@app.route('/tabulador/actualizar', methods=['POST'])
def actualizar_tabulador():
    id = int(request.form['id'])
    tab = Tabulador.query.get_or_404(id)
    tab.numero_grado = request.form['numero_grado']
    tab.grado = request.form['grado']
    tab.costo_hora = float(request.form['costo_hora'])
    db.session.commit()
    return redirect(url_for('catalogo_tabulador'))

# Eliminar registro
@app.route('/tabulador/eliminar/<int:id>', methods=['POST'])
def eliminar_tabulador(id):
    tab = Tabulador.query.get_or_404(id)
    db.session.delete(tab)
    db.session.commit()
    return redirect(url_for('catalogo_tabulador'))

@app.route('/cobro')
def redirigir_cobro():
    accion = request.args.get('accion')

    if accion == 'servicio_agua':
        return "<h2>Vista: Cobro de servicio de agua (en construcción)</h2>"
    elif accion == 'usuarios_atrasados':
        return "<h2>Vista: Cobro a usuarios atrasados (en construcción)</h2>"
    elif accion == 'impresion_recibo':
        return "<h2>Vista: Impresión de recibo (en construcción)</h2>"
    elif accion == 'pagos_adelantados':
        return "<h2>Vista: Pagos adelantados (en construcción)</h2>"
    
    return "<h2>Acción no reconocida.</h2>"

@app.route('/instituciones')
def redirigir_instituciones():
    accion = request.args.get('accion')

    if accion == 'agregar':
        return "<h2>Vista: Agregar institución (en construcción)</h2>"
    elif accion == 'capturar_lectura':
        return "<h2>Vista: Capturar lectura (en construcción)</h2>"
    elif accion == 'consulta_lectura':
        return "<h2>Vista: Consulta lectura (en construcción)</h2>"
    elif accion == 'impresion_formato':
        return "<h2>Vista: Impresión de formato de lecturas institucionales (en construcción)</h2>"
    elif accion == 'consulta_individual':
        return "<h2>Vista: Consulta de lecturas individual (en construcción)</h2>"
    
    return "<h2>Acción no reconocida.</h2>"

@app.route('/lecturas')
def redirigir_lecturas():
    accion = request.args.get('accion')

    if accion == 'impresion_formato':
        return "<h2>Vista: Impresión de formato de lecturas (en construcción)</h2>"
    elif accion == 'captura_lecturas':
        return "<h2>Vista: Captura de lecturas (en construcción)</h2>"
    elif accion == 'deudores_materiales':
        return "<h2>Vista: Capturar deudores de materiales (en construcción)</h2>"
    elif accion == 'captura_promedio':
        return "<h2>Vista: Capturar promedio de lectura (en construcción)</h2>"
    elif accion == 'promediar_lectura':
        return "<h2>Vista: Promediar una lectura (en construcción)</h2>"
    elif accion == 'lecturas_anteriores':
        return "<h2>Vista: Captura de lecturas anterior (en construcción)</h2>"
    elif accion == 'correccion_lectura':
        return "<h2>Vista: Corrección de toma de lecturas (en construcción)</h2>"
    elif accion == 'verificacion_lectura':
        return "<h2>Vista: Verificación de toma de lecturas (en construcción)</h2>"
    
    return "<h2>Acción no reconocida.</h2>"

@app.route('/consultas')
def redirigir_consultas():
    accion = request.args.get('accion')

    if accion == 'usuarios_lecturas':
        return "<h2>Vista: Consultas de Usuarios y estados de lecturas (en construcción)</h2>"
    elif accion == 'consulta_general':
        return "<h2>Vista: Consulta general de usuarios (en construcción)</h2>"
    elif accion == 'cobros_fecha':
        return "<h2>Vista: Cobros por fecha (en construcción)</h2>"
    elif accion == 'colonias':
        return "<h2>Vista: Colonias (en construcción)</h2>"
    elif accion == 'concentrado_individual':
        return "<h2>Vista: Concentrado individual de cobros (en construcción)</h2>"
    elif accion == 'suspension_historia':
        return "<h2>Vista: Historia de suspensión de usuario (en construcción)</h2>"
    elif accion == 'adeudos':
        return "<h2>Vista: Adeudos de consumo y materiales (en construcción)</h2>"
    elif accion == 'reconexiones':
        return "<h2>Vista: Cobro de reconexiones realizadas (en construcción)</h2>"
    elif accion == 'ordenes_trabajo':
        return "<h2>Vista: Consulta de órdenes de trabajo (en construcción)</h2>"
    elif accion == 'historial_consumos':
        return "<h2>Vista: Historial de consumos y pagos (en construcción)</h2>"
    elif accion == 'total_pagar':
        return "<h2>Vista: Total a pagar (en construcción)</h2>"
    elif accion == 'sumatoria_empresas':
        return "<h2>Vista: Sumatoria de empresas (en construcción)</h2>"
    elif accion == 'contratos_cancelados':
        return "<h2>Vista: Relación de contratos cancelados (en construcción)</h2>"
    
    return "<h2>Acción no reconocida.</h2>"

@app.route('/almacen')
def redirigir_almacen():
    accion = request.args.get('accion')

    if accion == 'inventario_inicial':
        return "<h2>Vista: Inventario inicial (en construcción)</h2>"
    elif accion == 'requisicion_compras':
        return "<h2>Vista: Requisición de compras (en construcción)</h2>"
    elif accion == 'captura_compras':
        return "<h2>Vista: Captura de compras (en construcción)</h2>"
    elif accion == 'vale_salida':
        return "<h2>Vista: Captura de vale de salida (en construcción)</h2>"
    elif accion == 'kardex':
        return "<h2>Vista: Kardex de materiales (en construcción)</h2>"
    elif accion == 'hoja_inventario':
        return "<h2>Vista: Hoja de inventario (en construcción)</h2>"
    elif accion == 'precio_materiales':
        return "<h2>Vista: Precio de materiales (en construcción)</h2>"
    elif accion == 'costo_ordenes':
        return "<h2>Vista: Costo de órdenes de trabajo (en construcción)</h2>"
    
    return "<h2>Acción no reconocida.</h2>"

@app.route('/reportes')
def redirigir_reportes():
    accion = request.args.get('accion')

    if accion == 'adeudo_materiales':
        return "<h2>Vista: Usuarios que adeudan materiales (en construcción)</h2>"
    elif accion == 'usuarios_suspendidos':
        return "<h2>Vista: Usuarios suspendidos actualmente (en construcción)</h2>"
    elif accion == 'catalogo_materiales':
        return "<h2>Vista: Catálogo de materiales (en construcción)</h2>"
    elif accion == 'contrato_servicio':
        return "<h2>Vista: Contrato de servicio (en construcción)</h2>"
    elif accion == 'ingresos_fechas':
        return "<h2>Vista: Reporte de ingresos entre fechas (general) (en construcción)</h2>"
    elif accion == 'ingresos_diarios':
        return "<h2>Vista: Reporte de ingresos diarios (en construcción)</h2>"
    
    return "<h2>Acción no reconocida.</h2>"

@app.route('/vencimientos')
def redirigir_vencimientos():
    accion = request.args.get('accion')

    if accion == 'registro_fechas':
        return "<h2>Vista: Registro de fechas (en construcción)</h2>"
    elif accion == 'tiempo_aviso':
        return "<h2>Vista: Tiempo de aviso (en construcción)</h2>"
    elif accion == 'usuarios_morosos':
        return "<h2>Vista: Usuarios que no se han presentado a pagar a tiempo (en construcción)</h2>"
    
    return "<h2>Acción no reconocida.</h2>"

@app.route('/egresos')
def redirigir_egresos():
    accion = request.args.get('accion')

    if accion == 'capturar_egreso':
        return "<h2>Vista: Capturar egreso (en construcción)</h2>"
    elif accion == 'capturar_egreso_anterior':
        return "<h2>Vista: Capturar egreso anterior (en construcción)</h2>"
    elif accion == 'alta_concepto_egreso':
        return "<h2>Vista: Alta concepto de egreso (en construcción)</h2>"
    elif accion == 'alta_concepto_deposito':
        return "<h2>Vista: Alta concepto de depósito (en construcción)</h2>"
    elif accion == 'alta_concepto_retiro':
        return "<h2>Vista: Alta concepto de retiro (en construcción)</h2>"
    elif accion == 'consulta_ingresos_mes':
        return "<h2>Vista: Consulta de ingresos por mes (en construcción)</h2>"
    elif accion == 'consulta_egresos_mes':
        return "<h2>Vista: Consulta de egresos por mes (en construcción)</h2>"
    elif accion == 'gastos_diarios':
        return "<h2>Vista: Gastos diarios (en construcción)</h2>"
    elif accion == 'depositos_municipio':
        return "<h2>Vista: Depósitos a la cuenta del municipio (en construcción)</h2>"
    elif accion == 'egresos_municipio':
        return "<h2>Vista: Egresos cuenta municipio (en construcción)</h2>"
    
    return "<h2>Acción no reconocida.</h2>"

@app.route('/ordenes')
def redirigir_ordenes():
    accion = request.args.get('accion')

    if accion == 'consulta_anteriores':
        return "<h2>Vista: Consulta de órdenes de trabajo anterior (en construcción)</h2>"
    elif accion == 'reinstalacion_servicio':
        return "<h2>Vista: Orden de reinstalación de servicio (en construcción)</h2>"
    elif accion == 'elaboracion_medidores':
        return "<h2>Vista: Elaboración de orden de trabajo - Medidores (en construcción)</h2>"
    elif accion == 'elaboracion_interno':
        return "<h2>Vista: Elaboración de orden de trabajo - Interno (en construcción)</h2>"
    elif accion == 'elaboracion_externo':
        return "<h2>Vista: Elaboración de orden de trabajo - Externo (en construcción)</h2>"
    elif accion == 'asignacion_materiales':
        return "<h2>Vista: Asignación de materiales a órdenes de trabajo (en construcción)</h2>"
    elif accion == 'formato_arqueo':
        return "<h2>Vista: Elaboracion de formato arqueo (en construccion)</h2>"

    return "<h2>Acción no reconocida.</h2>"

@app.route('/opciones')
def redirigir_opciones():
    accion = request.args.get('accion')

    if accion == 'registrar_usuario':
         return redirect('/usuarios/nuevo')
    elif accion == 'cambiar_contrasena':
        return "<h2>Vista: Cambiar mi contraseña (en construcción)</h2>"
    elif accion == 'cerrar_sesion':
        return "<h2>Sesión cerrada correctamente (simulado)</h2>"
    elif accion == 'salir_sistema':
        return "<h2>Gracias por usar el sistema. Puede cerrar la ventana.</h2>"
    
    return "<h2>Acción no reconocida.</h2>"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)




