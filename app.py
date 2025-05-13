from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, User

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
            session['usuario'] = usuario
            flash('Login exitoso!', 'success')
            return redirect(url_for('dashboard'))  # Asegúrate de crear esta ruta
        else:
            flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('login.html')





@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if user.rol == 'admin':
        return render_template('admin_dashboard.html', user=user)
    elif user.rol == 'veterano':
        return render_template('veterano_dashboard.html', user=user)
    else:
        return render_template('miembro_dashboard.html', user=user)









if __name__ == '__main__':
    app.run(debug=True)