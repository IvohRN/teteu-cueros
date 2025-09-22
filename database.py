"""
Configuración de base de datos para Tetey Cueros
"""

import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
import os

class DatabaseManager:
    """Gestor de base de datos SQLite"""
    
    def __init__(self, db_path: str = "tetey_cueros.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializar la base de datos y crear tablas"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Crear tabla de personalizaciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS personalizaciones (
                    id TEXT PRIMARY KEY,
                    producto TEXT NOT NULL,
                    color TEXT NOT NULL,
                    herrajes TEXT NOT NULL,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    activa BOOLEAN DEFAULT 1
                )
            ''')
            
            # Crear índices para mejor rendimiento
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_fecha_creacion ON personalizaciones(fecha_creacion)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_activa ON personalizaciones(activa)')
            
            conn.commit()
    
    def crear_personalizacion(self, id_personalizacion: str, producto: str, color: str, herrajes: str) -> bool:
        """Crear una nueva personalización"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO personalizaciones (id, producto, color, herrajes)
                    VALUES (?, ?, ?, ?)
                ''', (id_personalizacion, producto, color, herrajes))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al crear personalización: {e}")
            return False
    
    def obtener_personalizacion(self, id_personalizacion: str) -> Optional[Dict[str, Any]]:
        """Obtener una personalización por ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM personalizaciones 
                    WHERE id = ? AND activa = 1
                ''', (id_personalizacion,))
                
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
        except Exception as e:
            print(f"Error al obtener personalización: {e}")
            return None
    
    def listar_personalizaciones(self, limite: int = 100) -> List[Dict[str, Any]]:
        """Listar personalizaciones activas"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM personalizaciones 
                    WHERE activa = 1 
                    ORDER BY fecha_creacion DESC 
                    LIMIT ?
                ''', (limite,))
                
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Error al listar personalizaciones: {e}")
            return []
    
    def eliminar_personalizacion(self, id_personalizacion: str) -> bool:
        """Eliminar una personalización (marcar como inactiva)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE personalizaciones 
                    SET activa = 0 
                    WHERE id = ?
                ''', (id_personalizacion,))
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Error al eliminar personalización: {e}")
            return False
    
    def limpiar_personalizaciones_expiradas(self, dias_expiracion: int = 30) -> int:
        """Limpiar personalizaciones expiradas"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE personalizaciones 
                    SET activa = 0 
                    WHERE fecha_creacion < datetime('now', '-{} days')
                '''.format(dias_expiracion))
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"Error al limpiar personalizaciones: {e}")
            return 0
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtener estadísticas de la base de datos"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total de personalizaciones
                cursor.execute('SELECT COUNT(*) FROM personalizaciones WHERE activa = 1')
                total_activas = cursor.fetchone()[0]
                
                # Personalizaciones por color
                cursor.execute('''
                    SELECT color, COUNT(*) as cantidad 
                    FROM personalizaciones 
                    WHERE activa = 1 
                    GROUP BY color
                ''')
                por_color = dict(cursor.fetchall())
                
                # Personalizaciones por herrajes
                cursor.execute('''
                    SELECT herrajes, COUNT(*) as cantidad 
                    FROM personalizaciones 
                    WHERE activa = 1 
                    GROUP BY herrajes
                ''')
                por_herrajes = dict(cursor.fetchall())
                
                return {
                    'total_activas': total_activas,
                    'por_color': por_color,
                    'por_herrajes': por_herrajes
                }
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {}
