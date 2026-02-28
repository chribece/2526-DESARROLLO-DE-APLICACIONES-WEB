from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from config import Config
from database import db
from models import Cargo, Candidato, Postulacion, EstadisticasRRHH
from forms import CargoForm, CandidatoForm, PostulacionForm, BusquedaCandidatoForm
from utils import formatear_fecha, calcular_match, EstadoPipeline
import os

app = Flask(__name__)
app.config.from_object(Config)

# Inicializar base de datos al inicio
@app.before_request
def init_db():
    if not hasattr(app, 'db_initialized'):
        db.init_database()
        app.db_initialized = True

# Context processors
@app.context_processor
def inject_globals():
    return {
        'colors': Config.COLORS,
        'formatear_fecha': formatear_fecha
    }

# Rutas principales
@app.route('/')
def index():
    stats = EstadisticasRRHH.get_dashboard_stats()
    return render_template('index.html', stats=stats)

@app.route('/about')
def about():
    return render_template('about.html')

# ============ RUTAS CARGOS ============
@app.route('/cargos')
def lista_cargos():
    estado = request.args.get('estado')
    cargos = Cargo.get_all(estado=estado)
    return render_template('cargos/lista.html', cargos=cargos, estado_filtro=estado)

@app.route('/cargos/nuevo', methods=['GET', 'POST'])
def nuevo_cargo():
    form = CargoForm()
    if form.validate_on_submit():
        cargo = Cargo(
            titulo=form.titulo.data,
            descripcion=form.descripcion.data,
            departamento=form.departamento.data,
            salario_minimo=form.salario_minimo.data,
            salario_maximo=form.salario_maximo.data,
            tipo_contrato=form.tipo_contrato.data,
            ubicacion=form.ubicacion.data,
            estado=form.estado.data,
            fecha_cierre=form.fecha_cierre.data
        )
        cargo.save()
        flash('✅ Cargo creado exitosamente', 'success')
        return redirect(url_for('lista_cargos'))
    return render_template('cargos/formulario.html', form=form, titulo='Nuevo Cargo')

@app.route('/cargos/<int:id>/editar', methods=['GET', 'POST'])
def editar_cargo(id):
    cargo = Cargo.get_by_id(id)
    if not cargo:
        flash('Cargo no encontrado', 'error')
        return redirect(url_for('lista_cargos'))
    
    form = CargoForm(obj=cargo)
    if form.validate_on_submit():
        cargo.titulo = form.titulo.data
        cargo.descripcion = form.descripcion.data
        cargo.departamento = form.departamento.data
        cargo.salario_minimo = form.salario_minimo.data
        cargo.salario_maximo = form.salario_maximo.data
        cargo.tipo_contrato = form.tipo_contrato.data
        cargo.ubicacion = form.ubicacion.data
        cargo.estado = form.estado.data
        cargo.fecha_cierre = form.fecha_cierre.data
        cargo.save()
        flash('✅ Cargo actualizado exitosamente', 'success')
        return redirect(url_for('lista_cargos'))
    
    return render_template('cargos/formulario.html', form=form, titulo='Editar Cargo', cargo=cargo)

@app.route('/cargos/<int:id>/eliminar', methods=['POST'])
def eliminar_cargo(id):
    cargo = Cargo.get_by_id(id)
    if cargo:
        cargo.delete()
        flash('🗑️ Cargo eliminado', 'info')
    return redirect(url_for('lista_cargos'))

# ============ RUTAS CANDIDATOS ============
@app.route('/candidatos')
def lista_candidatos():
    form_busqueda = BusquedaCandidatoForm(request.args)
    activo = request.args.get('activo', '1') == '1'
    
    candidatos = Candidato.get_all(activo=activo)
    
    # Filtrar por búsqueda si hay parámetros
    if request.args.get('habilidad'):
        candidatos = [c for c in candidatos 
                     if request.args.get('habilidad').lower() in 
                     ','.join(c.habilidades).lower()]
    
    return render_template('candidatos/lista.html', 
                         candidatos=candidatos, 
                         form_busqueda=form_busqueda,
                         activo=activo)

@app.route('/candidatos/<int:id>')
def detalle_candidato(id):
    candidato = Candidato.get_by_id(id)
    if not candidato:
        flash('Candidato no encontrado', 'error')
        return redirect(url_for('lista_candidatos'))
    
    postulaciones = Postulacion.get_por_candidato(id)
    return render_template('candidatos/detalle.html', 
                         candidato=candidato, 
                         postulaciones=postulaciones)

@app.route('/candidatos/nuevo', methods=['GET', 'POST'])
def nuevo_candidato():
    form = CandidatoForm()
    if form.validate_on_submit():
        habilidades = [h.strip() for h in form.habilidades.data.split(',')] if form.habilidades.data else []
        
        candidato = Candidato(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
            telefono=form.telefono.data,
            linkedin=form.linkedin.data,
            portfolio=form.portfolio.data,
            resumen=form.resumen.data,
            habilidades=habilidades,
            experiencia_anos=form.experiencia_anos.data or 0,
            nivel_educativo=form.nivel_educativo.data,
            ubicacion=form.ubicacion.data,
            disponibilidad=form.disponibilidad.data,
            salario_esperado=form.salario_esperado.data or 0.0
        )
        try:
            candidato.save()
            flash('✅ Candidato registrado exitosamente', 'success')
            return redirect(url_for('lista_candidatos'))
        except Exception as e:
            flash(f'Error al guardar: {str(e)}', 'error')
    
    return render_template('candidatos/formulario.html', form=form, titulo='Nuevo Candidato')

@app.route('/candidatos/<int:id>/editar', methods=['GET', 'POST'])
def editar_candidato(id):
    candidato = Candidato.get_by_id(id)
    if not candidato:
        flash('Candidato no encontrado', 'error')
        return redirect(url_for('lista_candidatos'))
    
    form = CandidatoForm(obj=candidato)
    # Cargar habilidades como string
    if request.method == 'GET':
        form.habilidades.data = ', '.join(candidato.habilidades)
    
    if form.validate_on_submit():
        candidato.nombre = form.nombre.data
        candidato.apellido = form.apellido.data
        candidato.email = form.email.data
        candidato.telefono = form.telefono.data
        candidato.linkedin = form.linkedin.data
        candidato.portfolio = form.portfolio.data
        candidato.resumen = form.resumen.data
        candidato.habilidades = [h.strip() for h in form.habilidades.data.split(',')] if form.habilidades.data else []
        candidato.experiencia_anos = form.experiencia_anos.data or 0
        candidato.nivel_educativo = form.nivel_educativo.data
        candidato.ubicacion = form.ubicacion.data
        candidato.disponibilidad = form.disponibilidad.data
        candidato.salario_esperado = form.salario_esperado.data or 0.0
        
        candidato.save()
        flash('✅ Candidato actualizado exitosamente', 'success')
        return redirect(url_for('detalle_candidato', id=id))
    
    return render_template('candidatos/formulario.html', 
                         form=form, 
                         titulo='Editar Candidato', 
                         candidato=candidato)

@app.route('/candidatos/<int:id>/eliminar', methods=['POST'])
def eliminar_candidato(id):
    candidato = Candidato.get_by_id(id)
    if candidato:
        candidato.activo = False  # Soft delete
        candidato.save()
        flash('🗑️ Candidato desactivado', 'info')
    return redirect(url_for('lista_candidatos'))

# ============ RUTAS POSTULACIONES ============
@app.route('/postulaciones')
def lista_postulaciones():
    estado = request.args.get('estado')
    postulaciones = Postulacion.get_all(estado=estado)
    return render_template('postulaciones/lista.html', 
                         postulaciones=postulaciones,
                         estado_filtro=estado)

@app.route('/postulaciones/nueva', methods=['GET', 'POST'])
def nueva_postulacion():
    form = PostulacionForm()
    if form.validate_on_submit():
        postulacion = Postulacion(
            candidato_id=form.candidato_id.data,
            cargo_id=form.cargo_id.data,
            estado=form.estado.data,
            fuente_reclutamiento=form.fuente_reclutamiento.data,
            notas=form.notas.data,
            puntaje_evaluacion=form.puntaje_evaluacion.data
        )
        try:
            postulacion.save()
            flash('✅ Postulación registrada exitosamente', 'success')
            return redirect(url_for('lista_postulaciones'))
        except Exception as e:
            flash(f'Error: El candidato ya está postulado a este cargo', 'error')
    
    return render_template('postulaciones/formulario.html', form=form, titulo='Nueva Postulación')

@app.route('/postulaciones/<int:id>')
def detalle_postulacion(id):
    postulacion = Postulacion.get_by_id(id)
    if not postulacion:
        flash('Postulación no encontrada', 'error')
        return redirect(url_for('lista_postulaciones'))
    
    siguientes_estados = EstadoPipeline.get_siguientes_estados(postulacion.estado)
    return render_template('postulaciones/detalle.html', 
                         postulacion=postulacion,
                         siguientes_estados=siguientes_estados)

@app.route('/postulaciones/<int:id>/cambiar-estado', methods=['POST'])
def cambiar_estado_postulacion(id):
    postulacion = Postulacion.get_by_id(id)
    if not postulacion:
        return jsonify({'error': 'No encontrado'}), 404
    
    nuevo_estado = request.form.get('estado')
    if EstadoPipeline.puede_transicionar(postulacion.estado, nuevo_estado):
        postulacion.estado = nuevo_estado
        postulacion.save()
        flash(f'Estado actualizado a: {nuevo_estado}', 'success')
    else:
        flash('Transición de estado no válida', 'error')
    
    return redirect(url_for('detalle_postulacion', id=id))

@app.route('/postulaciones/<int:id>/eliminar', methods=['POST'])
def eliminar_postulacion(id):
    postulacion = Postulacion.get_by_id(id)
    if postulacion:
        postulacion.delete()
        flash('🗑️ Postulación eliminada', 'info')
    return redirect(url_for('lista_postulaciones'))

# API endpoints para AJAX
@app.route('/api/cargos/<int:id>/postulaciones')
def api_postulaciones_cargo(id):
    postulaciones = Postulacion.get_por_cargo(id)
    return jsonify([{
        'id': p.id,
        'candidato': p.candidato.nombre_completo if p.candidato else 'N/A',
        'estado': p.estado,
        'fecha': formatear_fecha(p.fecha_postulacion)
    } for p in postulaciones])

if __name__ == '__main__':
    app.run(debug=True, port=5000)