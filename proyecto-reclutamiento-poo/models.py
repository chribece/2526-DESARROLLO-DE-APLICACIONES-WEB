import sqlite3
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import json
from database import db
@dataclass
class Cargo:
    id: Optional[int] = None
    titulo: str = ""
    descripcion: str = ""
    departamento: str = ""
    salario_minimo: float = 0.0
    salario_maximo: float = 0.0
    tipo_contrato: str = "Tiempo completo"
    ubicacion: str = ""
    estado: str = "Activo"
    fecha_creacion: Optional[datetime] = None
    fecha_cierre: Optional[date] = None
    

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Cargo':
        # Convertir fecha_cierre de string a date si es necesario
        fecha_cierre = row['fecha_cierre']
        if fecha_cierre and isinstance(fecha_cierre, str):
            try:
                fecha_cierre = datetime.strptime(fecha_cierre, '%Y-%m-%d').date()
            except ValueError:
                fecha_cierre = None
        
        return cls(
            id=row['id'],
            titulo=row['titulo'],
            descripcion=row['descripcion'],
            departamento=row['departamento'],
            salario_minimo=row['salario_minimo'] or 0.0,
            salario_maximo=row['salario_maximo'] or 0.0,
            tipo_contrato=row['tipo_contrato'],
            ubicacion=row['ubicacion'],
            estado=row['estado'],
            fecha_creacion=row['fecha_creacion'],
            fecha_cierre=fecha_cierre
        )

    
    def save(self) -> int:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if self.id:
                cursor.execute('''
                    UPDATE cargos SET titulo=?, descripcion=?, departamento=?, 
                    salario_minimo=?, salario_maximo=?, tipo_contrato=?, 
                    ubicacion=?, estado=?, fecha_cierre=? WHERE id=?
                ''', (self.titulo, self.descripcion, self.departamento,
                      self.salario_minimo, self.salario_maximo, self.tipo_contrato,
                      self.ubicacion, self.estado, self.fecha_cierre, self.id))
                return self.id
            else:
                cursor.execute('''
                    INSERT INTO cargos (titulo, descripcion, departamento, salario_minimo, 
                    salario_maximo, tipo_contrato, ubicacion, estado, fecha_cierre)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (self.titulo, self.descripcion, self.departamento, self.salario_minimo,
                      self.salario_maximo, self.tipo_contrato, self.ubicacion, self.estado, self.fecha_cierre))
                return cursor.lastrowid
    
    @classmethod
    def get_by_id(cls, id: int) -> Optional['Cargo']:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM cargos WHERE id = ?', (id,))
            row = cursor.fetchone()
            return cls.from_row(row) if row else None
    
    @classmethod
    def get_all(cls, estado: Optional[str] = None) -> List['Cargo']:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if estado:
                cursor.execute('SELECT * FROM cargos WHERE estado = ? ORDER BY fecha_creacion DESC', (estado,))
            else:
                cursor.execute('SELECT * FROM cargos ORDER BY fecha_creacion DESC')
            return [cls.from_row(row) for row in cursor.fetchall()]
    
    def delete(self) -> bool:
        if not self.id:
            return False
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM cargos WHERE id = ?', (self.id,))
            return cursor.rowcount > 0
    
    def get_postulaciones_count(self) -> int:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM postulaciones WHERE cargo_id = ?', (self.id,))
            return cursor.fetchone()[0]


@dataclass
class Candidato:
    id: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    email: str = ""
    telefono: str = ""
    linkedin: str = ""
    portfolio: str = ""
    resumen: str = ""
    habilidades: List[str] = field(default_factory=list)
    experiencia_anos: int = 0
    nivel_educativo: str = ""
    ubicacion: str = ""
    disponibilidad: str = "2 semanas"
    salario_esperado: float = 0.0
    fecha_registro: Optional[datetime] = None
    activo: bool = True
    
    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"
    
    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Candidato':
        habilidades = []
        if row['habilidades']:
            try:
                habilidades = json.loads(row['habilidades'])
            except:
                habilidades = row['habilidades'].split(',')
        
        return cls(
            id=row['id'],
            nombre=row['nombre'],
            apellido=row['apellido'],
            email=row['email'],
            telefono=row['telefono'],
            linkedin=row['linkedin'],
            portfolio=row['portfolio'],
            resumen=row['resumen'],
            habilidades=habilidades,
            experiencia_anos=row['experiencia_anos'] or 0,
            nivel_educativo=row['nivel_educativo'],
            ubicacion=row['ubicacion'],
            disponibilidad=row['disponibilidad'],
            salario_esperado=row['salario_esperado'] or 0.0,
            fecha_registro=row['fecha_registro'],
            activo=bool(row['activo'])
        )
    
    def save(self) -> int:
        habilidades_json = json.dumps(self.habilidades) if self.habilidades else '[]'
        
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if self.id:
                cursor.execute('''
                    UPDATE candidatos SET nombre=?, apellido=?, email=?, telefono=?, 
                    linkedin=?, portfolio=?, resumen=?, habilidades=?, experiencia_anos=?, 
                    nivel_educativo=?, ubicacion=?, disponibilidad=?, salario_esperado=?, activo=?
                    WHERE id=?
                ''', (self.nombre, self.apellido, self.email, self.telefono,
                      self.linkedin, self.portfolio, self.resumen, habilidades_json,
                      self.experiencia_anos, self.nivel_educativo, self.ubicacion,
                      self.disponibilidad, self.salario_esperado, self.activo, self.id))
                return self.id
            else:
                cursor.execute('''
                    INSERT INTO candidatos (nombre, apellido, email, telefono, linkedin, 
                    portfolio, resumen, habilidades, experiencia_anos, nivel_educativo, 
                    ubicacion, disponibilidad, salario_esperado, activo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (self.nombre, self.apellido, self.email, self.telefono, self.linkedin,
                      self.portfolio, self.resumen, habilidades_json, self.experiencia_anos,
                      self.nivel_educativo, self.ubicacion, self.disponibilidad, 
                      self.salario_esperado, self.activo))
                return cursor.lastrowid
    
    @classmethod
    def get_by_id(cls, id: int) -> Optional['Candidato']:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM candidatos WHERE id = ?', (id,))
            row = cursor.fetchone()
            return cls.from_row(row) if row else None
    
    @classmethod
    def get_all(cls, activo: Optional[bool] = None) -> List['Candidato']:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if activo is not None:
                cursor.execute('SELECT * FROM candidatos WHERE activo = ? ORDER BY fecha_registro DESC', (int(activo),))
            else:
                cursor.execute('SELECT * FROM candidatos ORDER BY fecha_registro DESC')
            return [cls.from_row(row) for row in cursor.fetchall()]
    
    @classmethod
    def buscar_por_habilidad(cls, habilidad: str) -> List['Candidato']:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM candidatos 
                WHERE habilidades LIKE ? AND activo = 1 
                ORDER BY experiencia_anos DESC
            ''', (f'%{habilidad}%',))
            return [cls.from_row(row) for row in cursor.fetchall()]
    
    def delete(self) -> bool:
        if not self.id:
            return False
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM candidatos WHERE id = ?', (self.id,))
            return cursor.rowcount > 0


@dataclass
class Postulacion:
    id: Optional[int] = None
    candidato_id: int = 0
    cargo_id: int = 0
    fecha_postulacion: Optional[datetime] = None
    estado: str = "Recibido"
    fuente_reclutamiento: str = ""
    notas: str = ""
    puntaje_evaluacion: Optional[int] = None
    fecha_actualizacion: Optional[datetime] = None
    
    # Campos relacionados (no en DB)
    candidato: Optional[Candidato] = None
    cargo: Optional[Cargo] = None
    
    @classmethod
    def from_row(cls, row: sqlite3.Row) -> 'Postulacion':
        return cls(
            id=row['id'],
            candidato_id=row['candidato_id'],
            cargo_id=row['cargo_id'],
            fecha_postulacion=row['fecha_postulacion'],
            estado=row['estado'],
            fuente_reclutamiento=row['fuente_reclutamiento'],
            notas=row['notas'],
            puntaje_evaluacion=row['puntaje_evaluacion'],
            fecha_actualizacion=row['fecha_actualizacion']
        )
    
    def save(self) -> int:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if self.id:
                cursor.execute('''
                    UPDATE postulaciones SET estado=?, fuente_reclutamiento=?, 
                    notas=?, puntaje_evaluacion=?, fecha_actualizacion=CURRENT_TIMESTAMP
                    WHERE id=?
                ''', (self.estado, self.fuente_reclutamiento, self.notas, 
                      self.puntaje_evaluacion, self.id))
                return self.id
            else:
                cursor.execute('''
                    INSERT INTO postulaciones (candidato_id, cargo_id, estado, 
                    fuente_reclutamiento, notas, puntaje_evaluacion)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (self.candidato_id, self.cargo_id, self.estado,
                      self.fuente_reclutamiento, self.notas, self.puntaje_evaluacion))
                return cursor.lastrowid
    
    @classmethod
    def get_by_id(cls, id: int) -> Optional['Postulacion']:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM postulaciones WHERE id = ?', (id,))
            row = cursor.fetchone()
            if row:
                postulacion = cls.from_row(row)
                postulacion.cargar_relaciones()
                return postulacion
            return None
    
    @classmethod
    def get_all(cls, estado: Optional[str] = None) -> List['Postulacion']:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            if estado:
                cursor.execute('''
                    SELECT p.* FROM postulaciones p
                    JOIN candidatos c ON p.candidato_id = c.id
                    WHERE p.estado = ? AND c.activo = 1
                    ORDER BY p.fecha_postulacion DESC
                ''', (estado,))
            else:
                cursor.execute('''
                    SELECT p.* FROM postulaciones p
                    JOIN candidatos c ON p.candidato_id = c.id
                    WHERE c.activo = 1
                    ORDER BY p.fecha_postulacion DESC
                ''')
            
            postulaciones = []
            for row in cursor.fetchall():
                postulacion = cls.from_row(row)
                postulacion.cargar_relaciones()
                postulaciones.append(postulacion)
            return postulaciones
    
    def cargar_relaciones(self):
        self.candidato = Candidato.get_by_id(self.candidato_id)
        self.cargo = Cargo.get_by_id(self.cargo_id)
    
    @classmethod
    def get_por_cargo(cls, cargo_id: int) -> List['Postulacion']:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM postulaciones WHERE cargo_id = ? ORDER BY fecha_postulacion DESC
            ''', (cargo_id,))
            return [cls.from_row(row) for row in cursor.fetchall()]
    
    @classmethod
    def get_por_candidato(cls, candidato_id: int) -> List['Postulacion']:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM postulaciones WHERE candidato_id = ? ORDER BY fecha_postulacion DESC
            ''', (candidato_id,))
            return [cls.from_row(row) for row in cursor.fetchall()]
    
    def avanzar_estado(self) -> bool:
        estados = ['Recibido', 'En revisión', 'Entrevista técnica', 'Entrevista RRHH', 'Oferta', 'Contratado']
        if self.estado in estados:
            idx = estados.index(self.estado)
            if idx < len(estados) - 1:
                self.estado = estados[idx + 1]
                self.save()
                return True
        return False
    
    def delete(self) -> bool:
        if not self.id:
            return False
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM postulaciones WHERE id = ?', (self.id,))
            return cursor.rowcount > 0


class EstadisticasRRHH:
    @staticmethod
    def get_dashboard_stats() -> Dict[str, Any]:
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Totales
            cursor.execute('SELECT COUNT(*) FROM cargos WHERE estado = "Activo"')
            cargos_activos = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM candidatos WHERE activo = 1')
            total_candidatos = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM postulaciones')
            total_postulaciones = cursor.fetchone()[0]
            
            # Postulaciones por estado
            cursor.execute('''
                SELECT estado, COUNT(*) as total 
                FROM postulaciones 
                GROUP BY estado
            ''')
            por_estado = {row['estado']: row['total'] for row in cursor.fetchall()}
            
            # Últimas postulaciones
            cursor.execute('''
                SELECT p.*, c.nombre, c.apellido, cg.titulo 
                FROM postulaciones p
                JOIN candidatos c ON p.candidato_id = c.id
                JOIN cargos cg ON p.cargo_id = cg.id
                ORDER BY p.fecha_postulacion DESC
                LIMIT 5
            ''')
            ultimas = cursor.fetchall()
            
            return {
                'cargos_activos': cargos_activos,
                'total_candidatos': total_candidatos,
                'total_postulaciones': total_postulaciones,
                'por_estado': por_estado,
                'ultimas_postulaciones': ultimas
            }