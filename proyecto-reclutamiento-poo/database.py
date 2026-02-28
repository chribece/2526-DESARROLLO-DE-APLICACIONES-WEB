import sqlite3
from contextlib import contextmanager
from config import Config

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self.db_path = Config.DATABASE_PATH
        self._initialized = True
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def init_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla Cargos/Posiciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cargos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descripcion TEXT,
                    departamento TEXT NOT NULL,
                    salario_minimo REAL,
                    salario_maximo REAL,
                    tipo_contrato TEXT CHECK(tipo_contrato IN ('Tiempo completo', 'Medio tiempo', 'Freelance', 'Prácticas')),
                    ubicacion TEXT,
                    estado TEXT DEFAULT 'Activo' CHECK(estado IN ('Activo', 'Cerrado', 'Pausado')),
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_cierre DATE
                )
            ''')
            
            # Tabla Candidatos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS candidatos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    telefono TEXT,
                    linkedin TEXT,
                    portfolio TEXT,
                    resumen TEXT,
                    habilidades TEXT, -- JSON array
                    experiencia_anos INTEGER DEFAULT 0,
                    nivel_educativo TEXT,
                    ubicacion TEXT,
                    disponibilidad TEXT CHECK(disponibilidad IN ('Inmediata', '2 semanas', '1 mes', 'Más de 1 mes')),
                    salario_esperado REAL,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    activo BOOLEAN DEFAULT 1
                )
            ''')
            
            # Tabla Postulaciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS postulaciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidato_id INTEGER NOT NULL,
                    cargo_id INTEGER NOT NULL,
                    fecha_postulacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    estado TEXT DEFAULT 'Recibido' CHECK(estado IN ('Recibido', 'En revisión', 'Entrevista técnica', 'Entrevista RRHH', 'Oferta', 'Contratado', 'Rechazado', 'Descartado')),
                    fuente_reclutamiento TEXT, -- LinkedIn, Indeed, Referido, etc.
                    notas TEXT,
                    puntaje_evaluacion INTEGER CHECK(puntaje_evaluacion BETWEEN 1 AND 10),
                    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (candidato_id) REFERENCES candidatos(id) ON DELETE CASCADE,
                    FOREIGN KEY (cargo_id) REFERENCES cargos(id) ON DELETE CASCADE,
                    UNIQUE(candidato_id, cargo_id)
                )
            ''')
            
            # Tabla Documentos (CVs, certificados)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS documentos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    candidato_id INTEGER NOT NULL,
                    tipo TEXT NOT NULL, -- CV, Certificado, Carta, Otro
                    nombre_archivo TEXT NOT NULL,
                    ruta_archivo TEXT NOT NULL,
                    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (candidato_id) REFERENCES candidatos(id) ON DELETE CASCADE
                )
            ''')
            
            # Tabla Historial de Entrevistas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS entrevistas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    postulacion_id INTEGER NOT NULL,
                    fecha_programada TIMESTAMP NOT NULL,
                    tipo_entrevista TEXT CHECK(tipo_entrevista IN ('Presencial', 'Virtual', 'Telefónica')),
                    entrevistador TEXT,
                    feedback TEXT,
                    resultado TEXT CHECK(resultado IN ('Pendiente', 'Aprobado', 'No aprobado', 'Reprogramar')),
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (postulacion_id) REFERENCES postulaciones(id) ON DELETE CASCADE
                )
            ''')
            
            # Índices optimizados
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_postulaciones_candidato ON postulaciones(candidato_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_postulaciones_cargo ON postulaciones(cargo_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_postulaciones_estado ON postulaciones(estado)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_candidatos_email ON candidatos(email)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_cargos_estado ON cargos(estado)')
            
            print("✅ Base de datos inicializada correctamente")

# Instancia singleton
db = DatabaseManager()