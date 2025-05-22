from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from models import db, User, Almacen, Producto, Entrada, Salida, Existencia
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps



app = Flask(__name__)
app.secret_key = 'Caca'  # Cambia esto por una clave secreta real en producción

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos
db.init_app(app)
with app.app_context():
    db.create_all()



def requiere_rol(rol):
    def decorator(f):
        @wraps(f)  # This ensures the original function's name and metadata are preserved
        def wrapped(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            user = User.query.get(session['user_id'])
            if user.rol != rol and user.rol != 'admin':  # Admin can access everything
                flash('No tienes permisos para acceder a esta sección', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return wrapped
    return decorator
# Ruta de login
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        contraseña = request.form['password']
        user = User.query.filter_by(usuario=usuario).first()

        # Cambio importante: comparación directa sin hash
        if user and user.contraseña == contraseña:  # Comparación en texto plano
            session['user_id'] = user.id
            session['usuario'] = user.usuario
            session['rol'] = user.rol
            return redirect(url_for('dashboard'))
        else:
            pass

    return render_template('auth/login.html')


# Ruta de logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# Dashboard principal
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    # Datos comunes para todos los dashboards
    alertas_stock = Existencia.query.filter(Existencia.cantidad_actual < 5).all()
    entradas_recientes = Entrada.query.order_by(Entrada.fecha.desc()).limit(3).all()
    salidas_recientes = Salida.query.order_by(Salida.fecha.desc()).limit(3).all()
    actividad_reciente = sorted(
        [('Entrada', e) for e in entradas_recientes] + [('Salida', s) for s in salidas_recientes],
        key=lambda x: x[1].fecha,
        reverse=True
    )[:5]

    if user.rol == 'admin':
        # Datos adicionales para admin
        almacenes_count = Almacen.query.count()
        productos_count = Producto.query.count()
        movimientos_count = Entrada.query.count() + Salida.query.count()

        almacenes = Almacen.query.all()
        inventario_por_almacen = []
        for almacen in almacenes:
            count = Existencia.query.filter_by(almacen_id=almacen.id).count()
            inventario_por_almacen.append({
                'nombre': almacen.nombre,
                'productos': count,
                'valor': 0
            })

        return render_template('admin/dashboard.html',
                               user=user,
                               almacenes_count=almacenes_count,
                               productos_count=productos_count,
                               movimientos_count=movimientos_count,
                               alertas=alertas_stock,
                               actividad_reciente=actividad_reciente,
                               inventario_por_almacen=inventario_por_almacen
                               )
    elif user.rol == 'veterano':
        return render_template('veterano/dashboard.html',
                               user=user,
                               alertas=alertas_stock,
                               actividad_reciente=actividad_reciente
                               )
    else:
        return render_template('miembro/dashboard.html',
                               user=user,
                               actividad_reciente=actividad_reciente
                               )






# ==============================================
# RUTAS DE ADMINISTRADOR
# ==============================================




@app.route('/admin/reportes')
@requiere_rol('admin')
def reportes():
    # Obtener datos para los reportes
    entradas_mes = Entrada.query.filter(
        Entrada.fecha >= datetime.now().replace(day=1)
    ).all()

    salidas_mes = Salida.query.filter(
        Salida.fecha >= datetime.now().replace(day=1)
    ).all()

    # Agrupar existencias por almacén
    existencias_por_almacen = {}
    for almacen in Almacen.query.all():
        existencias_por_almacen[almacen.nombre] = Existencia.query.filter_by(
            almacen_id=almacen.id
        ).all()

    return render_template('admin/reportes.html',
                           entradas_mes=entradas_mes,
                           salidas_mes=salidas_mes,
                           existencias_por_almacen=existencias_por_almacen)

@app.route('/admin/almacenes')
@requiere_rol('admin')
def gestion_almacenes():
    almacenes = Almacen.query.all()
    total_productos = Producto.query.count()
    # Obtener lista de ciudades únicas
    ciudades = list(set([a.ciudad for a in almacenes]))

    return render_template('admin/almacenes.html',
                           almacenes=almacenes,
                           total_productos=total_productos,
                           ciudades=ciudades)

@app.route('/admin/almacenes/editar/<int:id>', methods=['POST'])
@requiere_rol('admin')
def editar_almacen(id):
    almacen = Almacen.query.get_or_404(id)
    almacen.nombre = request.form['nombre']
    almacen.ciudad = request.form['ciudad']
    almacen.direccion = request.form['direccion']
    db.session.commit()
    flash('Almacén actualizado correctamente', 'success')
    return redirect(url_for('gestion_almacenes'))

@app.route('/admin/almacenes/eliminar/<int:id>')
@requiere_rol('admin')
def eliminar_almacen(id):
    almacen = Almacen.query.get_or_404(id)
    db.session.delete(almacen)
    db.session.commit()
    flash('Almacén eliminado correctamente', 'success')
    return redirect(url_for('gestion_almacenes'))



@app.route('/admin/almacenes/agregar', methods=['POST'])
@requiere_rol('admin')
def agregar_almacen():
    nombre = request.form['nombre']
    ciudad = request.form['ciudad']
    direccion = request.form['direccion']

    nuevo_almacen = Almacen(nombre=nombre, ciudad=ciudad, direccion=direccion)
    db.session.add(nuevo_almacen)
    db.session.commit()

    flash('Almacén agregado correctamente', 'success')
    return redirect(url_for('gestion_almacenes'))





@app.route('/admin/productos')
@requiere_rol('admin')
def gestion_productos():
    productos = Producto.query.all()
    return render_template('admin/productos.html', productos=productos)


@app.route('/admin/productos/agregar', methods=['POST'])
@requiere_rol('admin')
def agregar_producto():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    unidad = request.form['unidad']

    nuevo_producto = Producto(
        nombre=nombre,
        descripcion=descripcion,
        unidad=unidad
    )

    db.session.add(nuevo_producto)
    db.session.commit()

    flash('Producto agregado correctamente', 'success')
    return redirect(url_for('gestion_productos'))


@app.route('/admin/productos/editar/<int:id>', methods=['POST'])
@requiere_rol('admin')
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    producto.nombre = request.form['nombre']
    producto.descripcion = request.form['descripcion']
    producto.unidad = request.form['unidad']

    db.session.commit()
    flash('Producto actualizado correctamente', 'success')
    return redirect(url_for('gestion_productos'))


@app.route('/admin/productos/eliminar/<int:id>')
@requiere_rol('admin')
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()

    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('gestion_productos'))


@app.route('/admin/entradas')
@requiere_rol('admin')
def gestion_entradas():
    entradas = Entrada.query.order_by(Entrada.fecha.desc()).all()
    productos = Producto.query.all()
    almacenes = Almacen.query.all()
    return render_template('admin/entradas.html',
                           entradas=entradas,
                           productos=productos,
                           almacenes=almacenes,datetime=datetime)


@app.route('/admin/entradas/agregar', methods=['POST'])
@requiere_rol('admin')
def agregar_entrada():
    producto_id = request.form['producto_id']
    almacen_id = request.form['almacen_id']
    cantidad = float(request.form['cantidad'])
    fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')

    nueva_entrada = Entrada(
        producto_id=producto_id,
        almacen_id=almacen_id,
        cantidad=cantidad,
        fecha=fecha
    )

    db.session.add(nueva_entrada)
    db.session.commit()

    flash('Entrada registrada correctamente', 'success')
    return redirect(url_for('gestion_entradas'))


@app.route('/admin/entradas/eliminar/<int:id>')
@requiere_rol('admin')
def eliminar_entrada(id):
    entrada = Entrada.query.get_or_404(id)
    db.session.delete(entrada)
    db.session.commit()

    flash('Entrada eliminada correctamente', 'success')
    return redirect(url_for('gestion_entradas'))


@app.route('/admin/salidas')
@requiere_rol('admin')
def gestion_salidas():
    salidas = Salida.query.order_by(Salida.fecha.desc()).all()
    productos = Producto.query.all()
    almacenes = Almacen.query.all()
    return render_template('admin/salidas.html',
                           salidas=salidas,
                           productos=productos,
                           almacenes=almacenes,datetime=datetime)


@app.route('/admin/salidas/agregar', methods=['POST'])
@requiere_rol('admin')
def agregar_salida():
    producto_id = request.form['producto_id']
    almacen_id = request.form['almacen_id']
    cantidad = float(request.form['cantidad'])
    fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')

    # Verificar existencia suficiente
    existencia = Existencia.query.filter_by(
        producto_id=producto_id,
        almacen_id=almacen_id
    ).first()

    if not existencia or existencia.cantidad_actual < cantidad:
        flash('No hay suficiente stock para esta salida', 'danger')
        return redirect(url_for('gestion_salidas'))

    nueva_salida = Salida(
        producto_id=producto_id,
        almacen_id=almacen_id,
        cantidad=cantidad,
        fecha=fecha
    )

    # Actualizar existencia
    existencia.cantidad_actual -= cantidad

    db.session.add(nueva_salida)
    db.session.commit()

    flash('Salida registrada correctamente', 'success')
    return redirect(url_for('gestion_salidas'))


@app.route('/admin/salidas/eliminar/<int:id>')
@requiere_rol('admin')
def eliminar_salida(id):
    salida = Salida.query.get_or_404(id)

    # Revertir la salida en el inventario
    existencia = Existencia.query.filter_by(
        producto_id=salida.producto_id,
        almacen_id=salida.almacen_id
    ).first()

    if existencia:
        existencia.cantidad_actual += salida.cantidad

    db.session.delete(salida)
    db.session.commit()

    flash('Salida eliminada y stock revertido', 'success')
    return redirect(url_for('gestion_salidas'))


@app.route('/admin/existencias')
@requiere_rol('admin')
def gestion_existencias():
    # Obtener todos los registros de existencia con información relacionada
    existencias = db.session.query(
        Existencia,
        Producto,
        Almacen
    ).join(
        Producto, Existencia.producto_id == Producto.id
    ).join(
        Almacen, Existencia.almacen_id == Almacen.id
    ).order_by(
        Almacen.nombre, Producto.nombre
    ).all()

    productos = Producto.query.order_by(Producto.nombre).all()
    almacenes = Almacen.query.order_by(Almacen.nombre).all()

    return render_template('admin/existencias.html',
                           existencias=existencias,
                           productos=productos,
                           almacenes=almacenes)


@app.route('/admin/existencias/actualizar', methods=['POST'])
@requiere_rol('admin')
def actualizar_existencia():
    existencia_id = request.form.get('existencia_id')
    nueva_cantidad = float(request.form.get('cantidad'))

    existencia = Existencia.query.get_or_404(existencia_id)
    existencia.cantidad_actual = nueva_cantidad
    db.session.commit()

    return jsonify({
        'success': True,
        'nueva_cantidad': existencia.cantidad_actual
    })


@app.route('/admin/existencias/transferir', methods=['POST'])
@requiere_rol('admin')
def transferir_inventario():
    producto_id = request.form.get('producto_id')
    origen_id = request.form.get('origen_id')
    destino_id = request.form.get('destino_id')
    cantidad = float(request.form.get('cantidad'))

    # Verificar existencia en origen
    existencia_origen = Existencia.query.filter_by(
        producto_id=producto_id,
        almacen_id=origen_id
    ).first()

    if not existencia_origen or existencia_origen.cantidad_actual < cantidad:
        return jsonify({
            'success': False,
            'message': 'No hay suficiente stock en el almacén de origen'
        }), 400

    # Actualizar origen
    existencia_origen.cantidad_actual -= cantidad

    # Crear o actualizar destino
    existencia_destino = Existencia.query.filter_by(
        producto_id=producto_id,
        almacen_id=destino_id
    ).first()

    if existencia_destino:
        existencia_destino.cantidad_actual += cantidad
    else:
        existencia_destino = Existencia(
            producto_id=producto_id,
            almacen_id=destino_id,
            cantidad_actual=cantidad
        )
        db.session.add(existencia_destino)

    db.session.commit()

    return jsonify({
        'success': True,
        'origen': {
            'nueva_cantidad': existencia_origen.cantidad_actual
        },
        'destino': {
            'nueva_cantidad': existencia_destino.cantidad_actual
        }
    })





@app.route('/admin/usuarios')
@requiere_rol('admin')
def gestion_usuarios():
    usuarios = User.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios, datetime=datetime)

@app.route('/admin/usuarios/agregar', methods=['POST'])
@requiere_rol('admin')
def agregar_usuario():
    usuario = request.form['usuario']
    password = request.form['password']
    rol = request.form['rol']

    if User.query.filter_by(usuario=usuario).first():
        flash('El nombre de usuario ya existe', 'danger')
        return redirect(url_for('gestion_usuarios'))

    nuevo_usuario = User(
        usuario=usuario,
        contraseña=generate_password_hash(password),
        rol=rol
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    flash('Usuario creado correctamente', 'success')
    return redirect(url_for('gestion_usuarios'))


@app.route('/admin/usuarios/editar/<int:id>', methods=['POST'])
@requiere_rol('admin')
def editar_usuario(id):
    usuario = User.query.get_or_404(id)
    usuario.usuario = request.form['usuario']
    usuario.rol = request.form['rol']

    if request.form['password']:
        usuario.contraseña = generate_password_hash(request.form['password'])

    db.session.commit()

    flash('Usuario actualizado correctamente', 'success')
    return redirect(url_for('gestion_usuarios'))


@app.route('/admin/usuarios/eliminar/<int:id>')
@requiere_rol('admin')
def eliminar_usuario(id):
    usuario = User.query.get_or_404(id)

    # Prevenir auto-eliminación
    if usuario.id == session.get('user_id'):
        flash('No puedes eliminar tu propio usuario', 'danger')
        return redirect(url_for('gestion_usuarios'))

    db.session.delete(usuario)
    db.session.commit()

    flash('Usuario eliminado correctamente', 'success')
    return redirect(url_for('gestion_usuarios'))





# ==============================================
# RUTAS DE VETERANO
# ==============================================

@app.route('/veterano/dashboard')
@requiere_rol('veterano')
def veterano_dashboard():
    # Datos para las tarjetas resumen
    hoy = datetime.now().date()
    semana_pasada = hoy - timedelta(days=7)

    entradas_hoy = Entrada.query.filter(
        db.func.date(Entrada.fecha) == hoy
    ).count()

    salidas_hoy = Salida.query.filter(
        db.func.date(Salida.fecha) == hoy
    ).count()

    # Productos con bajo stock (menos de 10 unidades)
    bajo_stock = Existencia.query.filter(
        Existencia.cantidad_actual < 10
    ).count()

    # Últimas 5 entradas y salidas
    ultimas_entradas = Entrada.query.order_by(
        Entrada.fecha.desc()
    ).limit(5).all()

    ultimas_salidas = Salida.query.order_by(
        Salida.fecha.desc()
    ).limit(5).all()

    return render_template('veterano/dashboard.html',
                           entradas_hoy=entradas_hoy,
                           salidas_hoy=salidas_hoy,
                           bajo_stock=bajo_stock,
                           ultimas_entradas=ultimas_entradas,
                           ultimas_salidas=ultimas_salidas)


@app.route('/veterano/entradas')
@requiere_rol('veterano')
def veterano_entradas():
    entradas = Entrada.query.order_by(Entrada.fecha.desc()).all()
    return render_template('veterano/entradas.html', entradas=entradas)


@app.route('/veterano/salidas')
@requiere_rol('veterano')
def veterano_salidas():
    salidas = Salida.query.order_by(Salida.fecha.desc()).all()
    return render_template('veterano/salidas.html', salidas=salidas)






# ==============================================
# RUTAS DE MIEMBRO
# ==============================================











if __name__ == '__main__':
    app.run(debug=True)