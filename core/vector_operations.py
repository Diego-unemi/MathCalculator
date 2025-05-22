import numpy as np

class VectorOperations:
    def parse_vector(self, entry_text):
        """Convierte una cadena de texto en un vector numpy"""
        try:
            return np.array([float(x.strip()) for x in entry_text.split(",")])
        except:
            raise ValueError("Entrada no válida. Usa números separados por comas.")

    def add_vectors(self, A, B):
        """Suma dos vectores"""
        try:
            if len(A) != len(B):
                raise ValueError("Los vectores deben tener la misma dimensión")
            return A + B
        except Exception as e:
            raise ValueError(f"Error al sumar vectores: {str(e)}")

    def subtract_vectors(self, A, B):
        """Resta dos vectores"""
        try:
            if len(A) != len(B):
                raise ValueError("Los vectores deben tener la misma dimensión")
            return A - B
        except Exception as e:
            raise ValueError(f"Error al restar vectores: {str(e)}")

    def dot_product(self, A, B):
        """Calcula el producto escalar de dos vectores"""
        try:
            if len(A) != len(B):
                raise ValueError("Los vectores deben tener la misma dimensión")
            return np.dot(A, B)
        except Exception as e:
            raise ValueError(f"Error al calcular el producto escalar: {str(e)}")

    def cross_product(self, A, B):
        """Calcula el producto vectorial de dos vectores"""
        try:
            if len(A) != 3 or len(B) != 3:
                raise ValueError("Los vectores deben ser tridimensionales para el producto vectorial")
            return np.cross(A, B)
        except Exception as e:
            raise ValueError(f"Error al calcular el producto vectorial: {str(e)}")
            
    def vector_magnitude(self, A):
        """Calcula la magnitud (módulo) de un vector"""
        try:
            return np.linalg.norm(A)
        except Exception as e:
            raise ValueError(f"Error al calcular la magnitud: {str(e)}")
            
    def unit_vector(self, A):
        """Calcula el vector unitario"""
        try:
            mag = np.linalg.norm(A)
            if mag == 0:
                raise ValueError("No se puede calcular el vector unitario de un vector nulo")
            return A / mag
        except Exception as e:
            raise ValueError(f"Error al calcular el vector unitario: {str(e)}")
            
    def angle_between_vectors(self, A, B):
        """Calcula el ángulo entre dos vectores (en radianes)"""
        try:
            dot = np.dot(A, B)
            norm_a = np.linalg.norm(A)
            norm_b = np.linalg.norm(B)
            
            if norm_a == 0 or norm_b == 0:
                raise ValueError("No se puede calcular el ángulo con vectores nulos")
            
            cos_angle = dot / (norm_a * norm_b)
            # Ajustar por errores de precisión
            if cos_angle > 1.0:
                cos_angle = 1.0
            elif cos_angle < -1.0:
                cos_angle = -1.0
                
            return np.arccos(cos_angle)
        except Exception as e:
            raise ValueError(f"Error al calcular el ángulo: {str(e)}") 