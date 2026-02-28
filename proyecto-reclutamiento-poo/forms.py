from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FloatField, IntegerField, DateField, EmailField, URLField
from wtforms.validators import DataRequired, Email, Optional, NumberRange, Length, URL
from datetime import date

class CargoForm(FlaskForm):
    titulo = StringField('Título del Cargo', validators=[
        DataRequired(message='El título es obligatorio'),
        Length(min=3, max=100)
    ])
    descripcion = TextAreaField('Descripción', validators=[
        Length(max=2000)
    ])
    departamento = StringField('Departamento', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    salario_minimo = FloatField('Salario Mínimo', validators=[
        Optional(),
        NumberRange(min=0, message='Debe ser un valor positivo')
    ])
    salario_maximo = FloatField('Salario Máximo', validators=[
        Optional(),
        NumberRange(min=0, message='Debe ser un valor positivo')
    ])
    tipo_contrato = SelectField('Tipo de Contrato', choices=[
        ('Tiempo completo', 'Tiempo completo'),
        ('Medio tiempo', 'Medio tiempo'),
        ('Freelance', 'Freelance'),
        ('Prácticas', 'Prácticas')
    ], validators=[DataRequired()])
    ubicacion = StringField('Ubicación', validators=[
        Optional(),
        Length(max=100)
    ])
    estado = SelectField('Estado', choices=[
        ('Activo', 'Activo'),
        ('Pausado', 'Pausado'),
        ('Cerrado', 'Cerrado')
    ], default='Activo')
    fecha_cierre = DateField('Fecha de Cierre', validators=[Optional()], format='%Y-%m-%d')


class CandidatoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    apellido = StringField('Apellido', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message='Email no válido')
    ])
    telefono = StringField('Teléfono', validators=[
        Optional(),
        Length(max=20)
    ])
    linkedin = URLField('LinkedIn', validators=[
        Optional(),
        URL(message='URL no válida')
    ])
    portfolio = URLField('Portfolio/Website', validators=[
        Optional(),
        URL(message='URL no válida')
    ])
    resumen = TextAreaField('Resumen Profesional', validators=[
        Optional(),
        Length(max=3000)
    ])
    habilidades = StringField('Habilidades (separadas por coma)', validators=[
        Optional(),
        Length(max=500)
    ])
    experiencia_anos = IntegerField('Años de Experiencia', validators=[
        Optional(),
        NumberRange(min=0, max=50)
    ])
    nivel_educativo = SelectField('Nivel Educativo', choices=[
        ('', 'Seleccione...'),
        ('Técnico', 'Técnico'),
        ('Universitario', 'Universitario'),
        ('Posgrado', 'Posgrado'),
        ('Doctorado', 'Doctorado')
    ], validators=[Optional()])
    ubicacion = StringField('Ubicación', validators=[
        Optional(),
        Length(max=100)
    ])
    disponibilidad = SelectField('Disponibilidad', choices=[
        ('Inmediata', 'Inmediata'),
        ('2 semanas', '2 semanas'),
        ('1 mes', '1 mes'),
        ('Más de 1 mes', 'Más de 1 mes')
    ], default='2 semanas')
    salario_esperado = FloatField('Salario Esperado', validators=[
        Optional(),
        NumberRange(min=0)
    ])


class PostulacionForm(FlaskForm):
    candidato_id = SelectField('Candidato', coerce=int, validators=[DataRequired()])
    cargo_id = SelectField('Cargo', coerce=int, validators=[DataRequired()])
    estado = SelectField('Estado', choices=[
        ('Recibido', 'Recibido'),
        ('En revisión', 'En revisión'),
        ('Entrevista técnica', 'Entrevista técnica'),
        ('Entrevista RRHH', 'Entrevista RRHH'),
        ('Oferta', 'Oferta'),
        ('Contratado', 'Contratado'),
        ('Rechazado', 'Rechazado'),
        ('Descartado', 'Descartado')
    ], default='Recibido')
    fuente_reclutamiento = SelectField('Fuente', choices=[
        ('', 'Seleccione...'),
        ('LinkedIn', 'LinkedIn'),
        ('Indeed', 'Indeed'),
        ('Referido', 'Referido interno'),
        ('Web corporativa', 'Web corporativa'),
        ('Bolsa de empleo', 'Bolsa de empleo'),
        ('Otro', 'Otro')
    ], validators=[Optional()])
    notas = TextAreaField('Notas', validators=[Optional(), Length(max=2000)])
    puntaje_evaluacion = IntegerField('Puntaje (1-10)', validators=[
        Optional(),
        NumberRange(min=1, max=10)
    ])
    
    def __init__(self, *args, **kwargs):
        super(PostulacionForm, self).__init__(*args, **kwargs)
        # Cargar opciones dinámicas
        from models import Candidato, Cargo
        self.candidato_id.choices = [(c.id, f"{c.nombre} {c.apellido} - {c.email}") 
                                     for c in Candidato.get_all(activo=True)]
        self.cargo_id.choices = [(c.id, f"{c.titulo} ({c.departamento})") 
                                for c in Cargo.get_all(estado='Activo')]


class BusquedaCandidatoForm(FlaskForm):
    query = StringField('Buscar', validators=[Optional()])
    habilidad = StringField('Habilidad', validators=[Optional()])
    experiencia_min = IntegerField('Exp. Mínima', validators=[Optional(), NumberRange(min=0)])
    disponibilidad = SelectField('Disponibilidad', choices=[
        ('', 'Todas'),
        ('Inmediata', 'Inmediata'),
        ('2 semanas', '2 semanas'),
        ('1 mes', '1 mes'),
        ('Más de 1 mes', 'Más de 1 mes')
    ], validators=[Optional()])