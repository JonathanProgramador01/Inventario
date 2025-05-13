from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User, Almacen, Producto, Producto, Entrada, Salida, Existencia

app = Flask(__name__)
app.secret_key = 'Caca'  # Cambia esto por una clave secreta real en producción

# Configuración de la base de datos (ajusta según tu DB)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Ejemplo para SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base de datos
db.init_app(app)
with app.app_context():
    db.create_all()  # Crea las tablas en la base de datos si no existen


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        contraseña = request.form['password']

        # Buscar usuario en la base de datos
        user = User.query.filter_by(usuario=usuario).first()

        if user and user.contraseña == contraseña:  # En producción, usa hash para contraseñas!
            # Guardar toda la información necesaria en la sesión
            session['user_id'] = user.id
            session['usuario'] = user.usuario
            session['rol'] = user.rol

            flash('Login exitoso!', 'success')
            return redirect(url_for('dashboard'))  # Redirección correcta
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')


# 343


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    # Obtener datos estadísticos reales
    almacenes_count = Almacen.query.count()
    productos_count = Producto.query.count()
    movimientos_count = Entrada.query.count() + Salida.query.count()

    # Obtener alertas (ejemplo: productos con stock bajo)
    alertas_stock = Existencia.query.filter(Existencia.cantidad_actual < 5).all()

    # Obtener actividad reciente (combinando entradas y salidas)
    entradas_recientes = Entrada.query.order_by(Entrada.fecha.desc()).limit(3).all()
    salidas_recientes = Salida.query.order_by(Salida.fecha.desc()).limit(3).all()
    actividad_reciente = sorted(
        [('Entrada', e) for e in entradas_recientes] + [('Salida', s) for s in salidas_recientes],
        key=lambda x: x[1].fecha,
        reverse=True
    )[:5]

    # Obtener resumen de inventario por almacén
    almacenes = Almacen.query.all()
    inventario_por_almacen = []
    for almacen in almacenes:
        count = Existencia.query.filter_by(almacen_id=almacen.id).count()
        inventario_por_almacen.append({
            'nombre': almacen.nombre,
            'productos': count,
            'valor': 0  # Puedes calcular esto si tienes precios
        })

    if user.rol == 'admin':
        return render_template(
            'admin_dashboard.html',
            user=user,
            almacenes_count=almacenes_count,
            productos_count=productos_count,
            movimientos_count=movimientos_count,
            alertas=alertas_stock,
            actividad_reciente=actividad_reciente,
            inventario_por_almacen=inventario_por_almacen
        )
    elif user.rol == 'veterano':
        return render_template('veterano_dashboard.html', user=user)
    else:
        return render_template('miembro_dashboard.html', user=user)











@app.route('/logout')
def logout():
    session.clear()  # Limpia toda la sesión
    return redirect(url_for('login'))  # Redirige al login








if __name__ == '__main__':
    app.run(debug=True)