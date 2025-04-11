import json
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from app import db
from app.models import Property  # Importamos el modelo de la propiedad


import os
from types import SimpleNamespace
import requests
from app import db
from flask import Blueprint, render_template, session, redirect, url_for, flash
from app import db  # Importa db aquí, después de que la app se haya inicializado
from app.models import Property, Photo
from functools import wraps
from types import SimpleNamespace
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, session, make_response
)
import base64
from PIL import Image
from io import BytesIO
import time

# Se define el blueprint para agrupar las rutas
main = Blueprint('main', __name__)

# URL base de la API (reemplaza por la URL correcta)
API_BASE_URL = "https://rent4all-geb3etamc4dub9eu.canadacentral-01.azurewebsites.net/api"



# Decorador opcional para evitar cache (puedes aplicarlo a rutas donde no quieras cache)
def nocache(view):
    @wraps(view)
    def no_cache_view(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return no_cache_view

# Página de inicio: redirige a login
@main.route('/')
def home():
    return redirect(url_for('main.login'))

# -------------------------------------------------------------------
# RUTA DE LOGIN
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        payload = {"username": username, "password": password}
        try:
            response = requests.post(f"{API_BASE_URL}/Auth/login", json=payload)
            print("DEBUG: Status Code:", response.status_code)
            print("DEBUG: Response Text:", response.text)
            print("DEBUG: Status Code:", response.status_code)
            if response.status_code == 200:
                data = response.json()
                print("DEBUG: Data recibida:", data)

                token = data.get("token")
                user_info = data.get("user")

                if not user_info:
                    flash("No se encontró información del usuario en la respuesta.", "error")
                    return redirect(url_for('main.login'))

                # Extrae y ajusta el rol (podés modificar según el formato real de la API)
                role = user_info.get("role", "").strip().capitalize()
                user_name = user_info.get("username")
                user_id = user_info.get("id")  # Verificá que 'id' exista

                # Log para confirmar datos en sesión
                print(f"DEBUG: role: {role}, user_name: {user_name}, user_id: {user_id}")

                session['token'] = token
                session['role'] = role
                session['user_name'] = user_name
                session['user_id'] = user_id

                if role == 'Owner':
                    return redirect(url_for('main.owner_dashboard'))
                elif role == 'Tenant':
                    return redirect(url_for('main.tenant_dashboard'))
                else:
                    flash("Rol no válido", "error")
                    return redirect(url_for('main.login'))
            else:
                flash("Credenciales incorrectas", "error")
        except Exception as e:
            flash(f"Error de conexión: {str(e)}", "error")
    return render_template('login.html')




# -------------------------------------------------------------------
# RUTAS PARA EL DASHBOARD DEL PROPIETARIO



# Ruta del dashboard del propietario
@main.route('/dashboard/owner')
def owner_dashboard():
    # Verifica si el usuario tiene sesión activa y es propietario
    if 'token' not in session or session.get('role') != 'Owner':
        return redirect(url_for('main.login'))  # Redirige a login si no está autenticado o no es propietario

    user_name = session.get('user_name')  # Nombre del usuario desde la sesión
    user_id = session.get('user_id')      # ID del propietario

    try:
        # Obtener todas las propiedades del propietario desde la base de datos
        propiedades = Property.query.filter_by(ownerId=user_id).all()

        if not propiedades:
            flash("No tienes propiedades registradas aún.", "info")
    except Exception as e:
        flash(f"Error al recuperar las propiedades: {str(e)}", "error")
        propiedades = []

    return render_template('owner_dashboard.html',
                           user_name=user_name,  # Nombre del usuario
                           role_display="Propietario",  # O cualquier otra variable que quieras mostrar
                           propiedades=propiedades)  # Pasa las propiedades a la plantilla






# -------------------------------------------------------------------
# RUTA GET: Mostrar formulario para crear propiedad (sólo para Owner)
@main.route('/create-property', methods=['GET'])
def show_create_property_form():
    if 'token' not in session or session.get('role') != 'Owner':
        flash("Acceso denegado. Solo los propietarios pueden agregar propiedades.", "error")
        return redirect(url_for('main.login'))
    return render_template('owner_create_property.html')

# Ruta para procesar el formulario y agregar la propiedad
@main.route('/create-property', methods=['POST'])
def owner_create_property():
    if 'token' not in session or session.get('role') != 'Owner':
        flash("Acceso denegado.", "error")
        return redirect(url_for('main.login'))

    # Recibir los datos del formulario
    property_type = request.form['type']
    price = float(request.form['price'])
    city = request.form['city']
    address = request.form['address']
    description = request.form['description']
    photosBase64 = request.form['photosBase64']

    # Convertir las fotos Base64 a imágenes (si se proporcionaron)
    photos = []
    if photosBase64:
        photos_data = base64.b64decode(photosBase64)
        for photo_data in photos_data:
            try:
                image = Image.open(BytesIO(photo_data))
                image_filename = f"photo_{int(time.time())}.jpg"
                image.save(f"app/static/img/{image_filename}")
                photos.append(Photo(url=f"/static/img/{image_filename}"))
            except Exception as e:
                flash(f"Error al guardar la foto: {e}", "error")

    # Crear un nuevo objeto Property
    new_property = Property(
        type=property_type,
        price=price,
        city=city,
        address=address,
        description=description,
        ownerId=session['user_id']
    )

    try:
        # Guardar en la base de datos
        db.session.add(new_property)
        db.session.commit()

        # Guardar las fotos relacionadas con la propiedad
        for photo in photos:
            photo.property_id = new_property.id
            db.session.add(photo)

        db.session.commit()
        flash("Propiedad agregada exitosamente", "success")

        return redirect(url_for('main.owner_dashboard'))
    
    except Exception as e:
        db.session.rollback()
        flash(f"Hubo un error al guardar la propiedad: {e}", "error")
        return redirect(url_for('main.owner_dashboard'))



# -------------------------------------------------------------------
# RUTA PARA EL DASHBOARD DEL INQUILINO

@main.route('/dashboard/tenant')
def tenant_dashboard():
    if 'token' not in session or session.get('role') != 'Tenant':
        flash("Acceso denegado. Debes ser un inquilino.", "error")
        return redirect(url_for('main.login'))
    # En este ejemplo se usa 'user_name' para inquilinos
    return render_template('tenant_dashboard.html', user_name=session.get('user_name'))

# -------------------------------------------------------------------


# -------------------------------------------------------------------
# RUTA DE REGISTRO DE USUARIO

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phoneNumber']
        password = request.form['password']
        role = request.form['role']

        # Validación del rol
        if role not in ["Owner", "Tenant"]:
            flash("Rol inválido. Debe ser 'Owner' o 'Tenant'", "error")
            return redirect(url_for('main.register'))

        payload = {
            "username": username,
            "email": email,
            "phoneNumber": phone,
            "password": password,
            "role": role
        }

        try:
            response = requests.post(f"{API_BASE_URL}/api/Auth/register", json=payload)
            if response.status_code in (200, 201):
                flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
                return redirect(url_for('main.login'))
            else:
                flash("Error en el registro. Revisa los datos e intenta de nuevo.", "error")
        except Exception as e:
            flash(f"Error de conexión: {str(e)}", "error")

    return render_template('register.html')



@main.route('/property/<int:property_id>')
def property_detail(property_id):
    # Verificar que el usuario esté autenticado (opcional, según tus requerimientos)
    if 'token' not in session:
        flash("Debes iniciar sesión para ver los detalles de la propiedad.", "error")
        return redirect(url_for('main.login'))
    
    # Construir la URL de la API para obtener la propiedad por ID
    url = f"{API_BASE_URL}/api/Property/{property_id}"
    
    try:
        # Puedes enviar además headers con el token si la API lo requiere:
        headers = {"Authorization": f"Bearer {session.get('token')}"}
        api_response = requests.get(url, headers=headers)
        
        if api_response.status_code == 200:
            property_data = api_response.json()
            # Renderizar la plantilla de detalle y pasar la data obtenida
            return render_template('property_detail.html', property=property_data)
        else:
            flash("No se pudo obtener la información de la propiedad.", "error")
            return redirect(url_for('main.owner_dashboard'))
    except Exception as e:
        flash(f"Error de conexión: {str(e)}", "error")
        return redirect(url_for('main.owner_dashboard'))



# -------------------------------------------------------------------
# RUTA DE LOGOUT




# Ruta para editar la propiedad
@main.route('/edit-property/<int:property_id>', methods=['GET', 'POST'])
def edit_property(property_id):
    if 'token' not in session or session.get('role') != 'Owner':
        return redirect(url_for('main.login'))  # Verificamos que el usuario esté autenticado y sea propietario

    # Buscar la propiedad por su ID
    property = Property.query.get(property_id)

    if not property:
        flash("La propiedad no existe.", "error")
        return redirect(url_for('main.owner_dashboard'))  # Si no existe la propiedad, volvemos al dashboard

    if request.method == 'POST':
        # Actualizar los campos de la propiedad con los nuevos datos del formulario
        property.type = request.form['type']
        property.price = float(request.form['price'])
        property.city = request.form['city']
        property.address = request.form['address']
        property.description = request.form['description']

        # Guardar los cambios en la base de datos
        try:
            db.session.commit()  # Guardar los cambios en la base de datos
            flash("Propiedad actualizada correctamente.", "success")
            return redirect(url_for('main.owner_dashboard'))  # Redirigir al dashboard
        except Exception as e:
            db.session.rollback()  # En caso de error, revertir los cambios
            flash(f"Error al actualizar la propiedad: {str(e)}", "error")

    return render_template('edit_property.html', property=property)  # Mostrar el formulario de edición








@main.route('/logout', methods=['POST'])
def logout():
    session.pop('token', None)
    session.pop('user_name', None)
    session.pop('role', None)
    session.pop('ultima_propiedad', None)
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('main.login'))
