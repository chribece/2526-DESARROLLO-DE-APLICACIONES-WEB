import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-2024-reclutamiento'
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'reclutamiento.db')
    DEBUG = True
    
    # Colores corporativos para uso en templates
    COLORS = {
        'primary': '#f2a517',      # Amarillo/Dorado
        'secondary': '#ef9120',    # Naranja
        'dark': '#161930',         # Azul oscuro/Navy
        'light': '#dcdde3'         # Gris claro
    }