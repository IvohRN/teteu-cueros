"""
Modelos de datos para la aplicación Teteu Cueros
"""

import uuid
from datetime import datetime
from typing import Optional, Dict, Any

class Personalizacion:
    """Modelo para representar una personalización de cartera"""
    
    def __init__(self, producto: str, color: str, herrajes: str, id_personalizacion: Optional[str] = None):
        """
        Inicializar una nueva personalización
        
        Args:
            producto: Nombre del producto (ej: "Cartera Clásica")
            color: Color seleccionado
            herrajes: Tipo de herrajes seleccionado
            id_personalizacion: ID único (se genera automáticamente si no se proporciona)
        """
        self.id = id_personalizacion or str(uuid.uuid4())
        self.producto = producto
        self.color = color
        self.herrajes = herrajes
        self.fecha_creacion = datetime.utcnow()
        self.activa = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir personalización a diccionario"""
        return {
            'id': self.id,
            'producto': self.producto,
            'color': self.color,
            'herrajes': self.herrajes,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'activa': self.activa
        }
    
    def get_imagen_path(self) -> str:
        """Obtener la ruta de la imagen de la personalización"""
        # Determinar modelo
        modelo = 'modelo1'
        if self.producto and 'urbana' in self.producto.lower():
            modelo = 'modelo2'
        
        # Mapear color a nombre de archivo
        color_file = self._map_color_to_file(self.color)
        
        # Mapear herrajes a nombre de archivo
        herrajes_file = self._map_herrajes_to_file(self.herrajes)
        
        return f"/static/{modelo}_{color_file}_{herrajes_file}.jpg"
    
    def _map_color_to_file(self, color: str) -> str:
        """Mapear color a nombre de archivo"""
        color_map = {
            'negro': 'negro',
            'marron': 'marron',
            'marron claro': 'marron_claro'
        }
        return color_map.get(color, 'negro')
    
    def _map_herrajes_to_file(self, herrajes: str) -> str:
        """Mapear herrajes a nombre de archivo"""
        herrajes_map = {
            'plata': 'plata',
            'dorado': 'dorado'
        }
        return herrajes_map.get(herrajes, 'plata')
    
    def is_valid(self) -> bool:
        """Verificar si la personalización es válida"""
        from config import Config
        
        return (
            self.producto and
            self.color in Config.COLORES_DISPONIBLES and
            self.herrajes in Config.HERRAJES_DISPONIBLES
        )
    
    def __str__(self) -> str:
        return f"Personalizacion(id={self.id}, producto={self.producto}, color={self.color}, herrajes={self.herrajes})"
    
    def __repr__(self) -> str:
        return self.__str__()

class PersonalizacionManager:
    """Gestor de personalizaciones en memoria"""
    
    def __init__(self):
        self.personalizaciones: Dict[str, Personalizacion] = {}
    
    def crear_personalizacion(self, producto: str, color: str, herrajes: str) -> Personalizacion:
        """Crear una nueva personalización"""
        personalizacion = Personalizacion(producto, color, herrajes)
        
        if not personalizacion.is_valid():
            raise ValueError("Datos de personalización inválidos")
        
        self.personalizaciones[personalizacion.id] = personalizacion
        return personalizacion
    
    def obtener_personalizacion(self, id_personalizacion: str) -> Optional[Personalizacion]:
        """Obtener una personalización por ID"""
        return self.personalizaciones.get(id_personalizacion)
    
    def eliminar_personalizacion(self, id_personalizacion: str) -> bool:
        """Eliminar una personalización"""
        if id_personalizacion in self.personalizaciones:
            del self.personalizaciones[id_personalizacion]
            return True
        return False
    
    def listar_personalizaciones(self) -> list:
        """Listar todas las personalizaciones"""
        return list(self.personalizaciones.values())
    
    def limpiar_personalizaciones_expiradas(self):
        """Limpiar personalizaciones expiradas"""
        from config import Config
        from datetime import datetime, timedelta
        
        ahora = datetime.utcnow()
        expiradas = []
        
        for id_personalizacion, personalizacion in self.personalizaciones.items():
            if ahora - personalizacion.fecha_creacion > Config.PERSONALIZACION_EXPIRY:
                expiradas.append(id_personalizacion)
        
        for id_personalizacion in expiradas:
            del self.personalizaciones[id_personalizacion]
        
        return len(expiradas)
