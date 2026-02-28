from collections import defaultdict, deque, namedtuple
from typing import List, Dict, Any, Optional, Callable
from functools import wraps
from datetime import datetime, timedelta
import re

# Estructuras de datos optimizadas

class PriorityQueue:
    """Cola de prioridad para gestión de candidatos por puntaje"""
    def __init__(self):
        self._queue = []
        self._index = 0
    
    def push(self, item: Any, priority: int):
        # Usamos negative priority para que heapq funcione como max-heap
        import heapq
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1
    
    def pop(self) -> Any:
        import heapq
        return heapq.heappop(self._queue)[-1]
    
    def __len__(self):
        return len(self._queue)


class LRUCache:
    """Cache LRU para optimizar consultas frecuentes"""
    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.cache = {}
        self.order = deque()
    
    def get(self, key: str) -> Any:
        if key in self.cache:
            self.order.remove(key)
            self.order.append(key)
            return self.cache[key]
        return None
    
    def put(self, key: str, value: Any):
        if key in self.cache:
            self.order.remove(key)
        elif len(self.cache) >= self.capacity:
            oldest = self.order.popleft()
            del self.cache[oldest]
        
        self.cache[key] = value
        self.order.append(key)
    
    def clear(self):
        self.cache.clear()
        self.order.clear()


class EstadoPipeline:
    """Máquina de estados para el pipeline de reclutamiento"""
    ESTADOS = ['Recibido', 'En revisión', 'Entrevista técnica', 
               'Entrevista RRHH', 'Oferta', 'Contratado']
    
    TRANSICIONES_VALIDAS = {
        'Recibido': ['En revisión', 'Rechazado', 'Descartado'],
        'En revisión': ['Entrevista técnica', 'Rechazado', 'Descartado'],
        'Entrevista técnica': ['Entrevista RRHH', 'Rechazado', 'Descartado'],
        'Entrevista RRHH': ['Oferta', 'Rechazado', 'Descartado'],
        'Oferta': ['Contratado', 'Rechazado'],
        'Contratado': [],
        'Rechazado': [],
        'Descartado': []
    }
    
    @classmethod
    def puede_transicionar(cls, estado_actual: str, nuevo_estado: str) -> bool:
        return nuevo_estado in cls.TRANSICIONES_VALIDAS.get(estado_actual, [])
    
    @classmethod
    def get_siguientes_estados(cls, estado_actual: str) -> List[str]:
        return cls.TRANSICIONES_VALIDAS.get(estado_actual, [])


# Funciones utilitarias

def normalizar_texto(texto: str) -> str:
    """Normaliza texto para búsquedas"""
    if not texto:
        return ""
    texto = texto.lower().strip()
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto


def calcular_match(candidato_habilidades: List[str], requisitos: List[str]) -> float:
    """Calcula porcentaje de match entre habilidades del candidato y requisitos"""
    if not requisitos:
        return 0.0
    
    candidato_set = set(normalizar_texto(h) for h in candidato_habilidades)
    requisitos_set = set(normalizar_texto(r) for r in requisitos)
    
    if not candidato_set:
        return 0.0
    
    matches = candidato_set.intersection(requisitos_set)
    return (len(matches) / len(requisitos_set)) * 100


def formatear_fecha(fecha: datetime) -> str:
    """Formatea fecha de manera amigable"""
    if not fecha:
        return "N/A"
    
    hoy = datetime.now()
    diff = hoy - fecha
    
    if diff.days == 0:
        return "Hoy"
    elif diff.days == 1:
        return "Ayer"
    elif diff.days < 7:
        return f"Hace {diff.days} días"
    elif diff.days < 30:
        semanas = diff.days // 7
        return f"Hace {semanas} semana{'s' if semanas > 1 else ''}"
    else:
        return fecha.strftime("%d/%m/%Y")


def validar_email(email: str) -> bool:
    """Validación robusta de email"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None


def generar_slug(texto: str) -> str:
    """Genera slug URL-friendly"""
    texto = normalizar_texto(texto)
    texto = re.sub(r'\s+', '-', texto)
    return texto[:50]


# Decoradores

def timer(func: Callable) -> Callable:
    """Mide tiempo de ejecución"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = datetime.now()
        resultado = func(*args, **kwargs)
        fin = datetime.now()
        print(f"⏱️ {func.__name__} tomó {(fin - inicio).total_seconds():.4f}s")
        return resultado
    return wrapper


def memoize(func: Callable) -> Callable:
    """Cache simple para funciones puras"""
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


# Named tuples para estructuras de datos ligeras
ResumenCandidato = namedtuple('ResumenCandidato', 
                             ['id', 'nombre', 'match_score', 'estado_postulacion'])

MetricasPipeline = namedtuple('MetricasPipeline',
                             ['total', 'por_estado', 'tiempo_promedio', 'tasa_conversion'])


class ReporteGenerator:
    """Generador de reportes eficiente"""
    
    @staticmethod
    def generar_reporte_funnel(postulaciones: List[Any]) -> Dict[str, int]:
        """Genera reporte de funnel de conversión"""
        funnel = defaultdict(int)
        for p in postulaciones:
            funnel[p.estado] += 1
        return dict(funnel)
    
    @staticmethod
    def top_candidatos_por_cargo(cargo_id: int, n: int = 10) -> List[ResumenCandidato]:
        """Obtiene top N candidatos para un cargo específico"""
        from models import Postulacion
        
        postulaciones = Postulacion.get_por_cargo(cargo_id)
        # Ordenar por puntaje de evaluación
        postulaciones.sort(key=lambda x: x.puntaje_evaluacion or 0, reverse=True)
        
        resultado = []
        for p in postulaciones[:n]:
            if p.candidato:
                match = calcular_match(
                    p.candidato.habilidades,
                    p.cargo.descripcion.split() if p.cargo else []
                )
                resultado.append(ResumenCandidato(
                    id=p.candidato.id,
                    nombre=p.candidato.nombre_completo,
                    match_score=match,
                    estado_postulacion=p.estado
                ))
        return resultado