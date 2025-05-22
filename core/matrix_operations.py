import numpy as np
from fractions import Fraction

class MatrixOperations:
    def calculate_determinant(self, matrix):
        try:
            det = np.linalg.det(matrix)
            return self.decimal_to_fraction(det)
        except:
            return None

    def calculate_inverse(self, matrix):
        try:
            # Verificamos si la matriz es singular
            det = np.linalg.det(matrix)
            if abs(det) < 1e-10:
                raise ValueError("La matriz es singular, no tiene inversa.")
                
            # Calculamos la inversa
            inv = np.linalg.inv(matrix)
            return self.format_matrix(inv)
        except Exception as e:
            raise ValueError(f"Error al calcular la inversa: {str(e)}")

    def add_matrices(self, matrix_a, matrix_b):
        try:
            result = matrix_a + matrix_b
            return self.format_matrix(result)
        except:
            raise ValueError("No se pudieron sumar las matrices. Asegúrese de que tengan las mismas dimensiones.")

    def subtract_matrices(self, matrix_a, matrix_b):
        try:
            result = matrix_a - matrix_b
            return self.format_matrix(result)
        except:
            raise ValueError("No se pudieron restar las matrices. Asegúrese de que tengan las mismas dimensiones.")

    def multiply_matrices(self, matrix_a, matrix_b):
        try:
            result = np.matmul(matrix_a, matrix_b)
            return self.format_matrix(result)
        except:
            raise ValueError("No se pudieron multiplicar las matrices. Asegúrese de que las dimensiones sean compatibles.")

    def decimal_to_fraction(self, decimal, max_denominator=100):
        try:
            # Si el número es muy cercano a un entero, lo devolvemos como entero
            if abs(decimal - round(decimal)) < 1e-10:
                return round(decimal)
            
            # Convertimos a fracción
            frac = Fraction(decimal).limit_denominator(max_denominator)
            
            # Si el denominador es 1, devolvemos solo el numerador
            if frac.denominator == 1:
                return frac.numerator
            
            # Si el numerador es negativo, movemos el signo al numerador
            if frac.denominator < 0:
                frac = Fraction(-frac.numerator, -frac.denominator)
            
            return frac
        except:
            return decimal

    def format_matrix(self, matrix):
        if matrix is None:
            return None
        return np.array([[self.decimal_to_fraction(x) for x in row] for row in matrix]) 