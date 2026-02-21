from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_reclutamiento_2024'

# ==========================================
# DATOS SIMULADOS (BASE DE DATOS EN MEMORIA)
# ==========================================

# Tabla: candidatos
candidatos_db = [
    {
        'cedula': '1801234567',
        'nombres': 'María Fernanda López',
        'correo': 'maria.lopez@email.com',
        'telefono': '0991234567',
        'direccion': 'Av. Principal 123, Quito'
    },
    {
        'cedula': '1709876543',
        'nombres': 'Carlos Andrés Ruiz',
        'correo': 'carlos.ruiz@email.com',
        'telefono': '0987654321',
        'direccion': 'Calle Secundaria 456, Guayaquil'
    },
    {
        'cedula': '1804567890',
        'nombres': 'Ana Patricia Vargas',
        'correo': 'ana.vargas@email.com',
        'telefono': '0976543210',
        'direccion': 'Av. Amazonas 789, Quito'
    }
]

# Tabla: cargos
cargos_db = [
    {'id_cargo': 1, 'nombre': 'Desarrollador Backend', 'descripcion': 'Desarrollo de APIs y servicios'},
    {'id_cargo': 2, 'nombre': 'Analista de RRHH', 'descripcion': 'Gestión de talento humano'},
    {'id_cargo': 3, 'nombre': 'Diseñador UX/UI', 'descripcion': 'Diseño de interfaces de usuario'},
    {'id_cargo': 4, 'nombre': 'Gerente de Ventas', 'descripcion': 'Liderazgo comercial'},
    {'id_cargo': 5, 'nombre': 'Contador Senior', 'descripcion': 'Gestión financiera y tributaria'}
]

# Tabla: postulacion
postulaciones_db = [
    {
        'id_postulacion': 101,
        'create_at': '2024-01-15',
        'estado': 'En revisión',
        'id_cargo': 1,
        'cargo_nombre': 'Desarrollador Backend'
    },
    {
        'id_postulacion': 102,
        'create_at': '2024-01-16',
        'estado': 'Entrevista técnica',
        'id_cargo': 2,
        'cargo_nombre': 'Analista de RRHH'
    },
    {
        'id_postulacion': 103,
        'create_at': '2024-01-17',
        'estado': 'Oferta enviada',
        'id_cargo': 3,
        'cargo_nombre': 'Diseñador UX/UI'
    }
]

# Tabla: postulacioncandidato
postulacion_candidato_db = [
    {'cedula': '1801234567', 'id_postulacion': 101, 'fechareg': '2024-01-15', 'descripcion': 'Postulación inicial'},
    {'cedula': '1709876543', 'id_postulacion': 102, 'fechareg': '2024-01-16', 'descripcion': 'Referido interno'},
    {'cedula': '1804567890', 'id_postulacion': 103, 'fechareg': '2024-01-17', 'descripcion': 'Portal web'}
]

# Tabla: estudios
estudios_db = [
    {'id_estudio': 1, 'nivel': 'Superior', 'titulos': 'Ingeniería en Sistemas', 'instituciones': 'EPN', 'cedula': '1801234567'},
    {'id_estudio': 2, 'nivel': 'Superior', 'titulos': 'Licenciatura en Psicología', 'instituciones': 'UCE', 'cedula': '1709876543'},
    {'id_estudio': 3, 'nivel': 'Superior', 'titulos': 'Diseño Gráfico', 'instituciones': 'UDLA', 'cedula': '1804567890'}
]

# Tabla: experiencialaboral
experiencia_db = [
    {'id_experiencia': 1, 'empresa': 'TechCorp', 'cargo': 'Junior Developer', 'descripcion': '2 años desarrollo web', 'cedula': '1801234567'},
    {'id_experiencia': 2, 'empresa': 'HR Solutions', 'cargo': 'Asistente RRHH', 'descripcion': '3 años gestión de personal', 'cedula': '1709876543'}
]

# Tabla: referenciaspersonales
referencias_db = [
    {'id_referencias': 1, 'nombres': 'Juan Pérez', 'relacion': 'Ex-jefe', 'telefono': '0991112222', 'descripcion': 'Referencia laboral', 'cedula': '1801234567'}
]

# Tabla: licencias
licencias_db = [
    {'id_licencia': 1, 'tipo': 'Conducir', 'fecha_caducidad': '2026-05-20', 'cedula': '1801234567'},
    {'id_licencia': 2, 'tipo': 'Certificación Scrum', 'fecha_caducidad': '2025-12-31', 'cedula': '1801234567'}
]

# Tabla: documentos
documentos_db = [
    {'id_documentos': 1, 'nombrearchivo': 'cv_maria_lopez.pdf', 'tipo': 'PDF', 'id_postulacion': 101},
    {'id_documentos': 2, 'nombrearchivo': 'certificado_titulo.pdf', 'tipo': 'PDF', 'id_postulacion': 101}
]

# Tabla: historial
historial_db = [
    {'id_historial': 1, 'estado': 'Postulado', 'descripcion': 'Registro inicial', 'id_postulacion': 101},
    {'id_historial': 2, 'estado': 'En revisión', 'descripcion': 'CV revisado', 'id_postulacion': 101},
    {'id_historial': 3, 'estado': 'Entrevista', 'descripcion': 'Entrevista programada', 'id_postulacion': 102}
]

# ==========================================
# RUTAS PRINCIPALES
# ==========================================

@app.route('/')
def index():
    """Dashboard principal con estadísticas"""
    stats = {
        'total_candidatos': len(candidatos_db),
        'total_postulaciones': len(postulaciones_db),
        'total_cargos': len(cargos_db),
        'postulaciones_activas': len([p for p in postulaciones_db if p['estado'] != 'Cerrado'])
    }
    
    ultimas_postulaciones = sorted(postulaciones_db, key=lambda x: x['create_at'], reverse=True)[:5]
    
    return render_template('index.html', 
                         stats=stats, 
                         ultimas_postulaciones=ultimas_postulaciones,
                         cargos=cargos_db)

@app.route('/about')
def about():
    """Página Acerca de"""
    return render_template('about.html')

# ==========================================
# RUTAS: CANDIDATOS
# ==========================================

@app.route('/candidatos')
def lista_candidatos():
    """Lista todos los candidatos"""
    return render_template('candidatos/lista.html', candidatos=candidatos_db)

@app.route('/candidato/<cedula>')
def detalle_candidato(cedula):
    """Detalle completo de un candidato con relaciones"""
    candidato = next((c for c in candidatos_db if c['cedula'] == cedula), None)
    
    if not candidato:
        flash('Candidato no encontrado', 'danger')
        return redirect(url_for('lista_candidatos'))
    
    # Obtener datos relacionados
    estudios = [e for e in estudios_db if e['cedula'] == cedula]
    experiencias = [e for e in experiencia_db if e['cedula'] == cedula]
    referencias = [r for r in referencias_db if r['cedula'] == cedula]
    licencias = [l for l in licencias_db if l['cedula'] == cedula]
    
    # Obtener postulaciones del candidato
    postulaciones_ids = [pc['id_postulacion'] for pc in postulacion_candidato_db if pc['cedula'] == cedula]
    postulaciones = [p for p in postulaciones_db if p['id_postulacion'] in postulaciones_ids]
    
    return render_template('candidatos/detalle.html',
                         candidato=candidato,
                         estudios=estudios,
                         experiencias=experiencias,
                         referencias=referencias,
                         licencias=licencias,
                         postulaciones=postulaciones)

@app.route('/candidato/nuevo', methods=['GET', 'POST'])
def nuevo_candidato():
    """Formulario para nuevo candidato"""
    if request.method == 'POST':
        nuevo = {
            'cedula': request.form['cedula'],
            'nombres': request.form['nombres'],
            'correo': request.form['correo'],
            'telefono': request.form['telefono'],
            'direccion': request.form['direccion']
        }
        candidatos_db.append(nuevo)
        flash('Candidato registrado exitosamente', 'success')
        return redirect(url_for('lista_candidatos'))
    
    return render_template('candidatos/formulario.html')

# ==========================================
# RUTAS: POSTULACIONES
# ==========================================

@app.route('/postulaciones')
def lista_postulaciones():
    """Lista todas las postulaciones"""
    return render_template('postulaciones/lista.html', 
                         postulaciones=postulaciones_db,
                         candidatos=candidatos_db,
                         postulacion_candidato=postulacion_candidato_db)

@app.route('/postulacion/<int:id_postulacion>')
def detalle_postulacion(id_postulacion):
    """Detalle de postulación con historial y documentos"""
    postulacion = next((p for p in postulaciones_db if p['id_postulacion'] == id_postulacion), None)
    
    if not postulacion:
        flash('Postulación no encontrada', 'danger')
        return redirect(url_for('lista_postulaciones'))
    
    # Obtener candidatos asociados
    cedulas = [pc['cedula'] for pc in postulacion_candidato_db if pc['id_postulacion'] == id_postulacion]
    candidatos_postulacion = [c for c in candidatos_db if c['cedula'] in cedulas]
    
    # Obtener historial y documentos
    historial = [h for h in historial_db if h['id_postulacion'] == id_postulacion]
    documentos = [d for d in documentos_db if d['id_postulacion'] == id_postulacion]
    
    return render_template('postulaciones/detalle.html',
                         postulacion=postulacion,
                         candidatos=candidatos_postulacion,
                         historial=historial,
                         documentos=documentos)

# ==========================================
# RUTAS: CARGOS
# ==========================================

@app.route('/cargos')
def lista_cargos():
    """Lista de cargos disponibles"""
    return render_template('cargos/lista.html', cargos=cargos_db)

@app.route('/cargo/nuevo', methods=['GET', 'POST'])
def nuevo_cargo():
    """Crear nuevo cargo"""
    if request.method == 'POST':
        nuevo = {
            'id_cargo': len(cargos_db) + 1,
            'nombre': request.form['nombre'],
            'descripcion': request.form['descripcion']
        }
        cargos_db.append(nuevo)
        flash('Cargo creado exitosamente', 'success')
        return redirect(url_for('lista_cargos'))
    
    return render_template('cargos/formulario.html')

# ==========================================
# RUTAS DINÁMICAS (API JSON)
# ==========================================

@app.route('/api/candidato/<cedula>')
def api_candidato(cedula):
    """API JSON para datos de candidato"""
    candidato = next((c for c in candidatos_db if c['cedula'] == cedula), None)
    
    if candidato:
        return jsonify({
            'mensaje': f'Candidato encontrado: {candidato["nombres"]}',
            'datos': candidato,
            'consulta': datetime.now().isoformat()
        })
    return jsonify({'error': 'Candidato no encontrado'}), 404

@app.route('/api/postulacion/<int:id_postulacion>')
def api_postulacion(id_postulacion):
    """API JSON para estado de postulación"""
    postulacion = next((p for p in postulaciones_db if p['id_postulacion'] == id_postulacion), None)
    
    if postulacion:
        return jsonify({
            'mensaje': f'Postulación #{id_postulacion} - {postulacion["estado"]}',
            'datos': postulacion,
            'consulta': datetime.now().isoformat()
        })
    return jsonify({'error': 'Postulación no encontrada'}), 404

@app.route('/api/cargo/<int:id_cargo>')
def api_cargo(id_cargo):
    """API JSON para información de cargo"""
    cargo = next((c for c in cargos_db if c['id_cargo'] == id_cargo), None)
    
    if cargo:
        # Contar postulaciones para este cargo
        count = len([p for p in postulaciones_db if p['id_cargo'] == id_cargo])
        return jsonify({
            'mensaje': f'Cargo: {cargo["nombre"]} - Consulta exitosa',
            'datos': cargo,
            'postulaciones_activas': count,
            'consulta': datetime.now().isoformat()
        })
    return jsonify({'error': 'Cargo no encontrado'}), 404

# ==========================================
# MANEJO DE ERRORES
# ==========================================

@app.errorhandler(404)
def not_found(error):
    return render_template('base.html', 
                         error='Página no encontrada',
                         mensaje='La ruta solicitada no existe'), 404

if __name__ == '__main__':
    print("=" * 60)
    print("🎯 SISTEMA DE RECLUTAMIENTO - Flask + Jinja2")
    print("=" * 60)
    print("Rutas disponibles:")
    print("  • /                          → Dashboard")
    print("  • /about                     → Acerca de")
    print("  • /candidatos                → Lista candidatos")
    print("  • /candidato/<cedula>        → Detalle candidato")
    print("  • /candidato/nuevo           → Nuevo candidato")
    print("  • /postulaciones             → Lista postulaciones")
    print("  • /postulacion/<id>          → Detalle postulación")
    print("  • /cargos                    → Lista cargos")
    print("  • /cargo/nuevo               → Nuevo cargo")
    print("  • /api/...                   → Endpoints JSON")
    print("=" * 60)
    app.run(debug=True, port=5000)