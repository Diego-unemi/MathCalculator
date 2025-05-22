import sympy as sp
import numpy as np
from sympy.parsing.sympy_parser import parse_expr

class DerivativeOperations:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.symbols = {'x': self.x}
    
    def parse_function(self, func_str):
        """Convierte una cadena de texto en una expresión simbólica"""
        try:
            # Reemplazar ^ por ** para la potencia
            func_str = func_str.replace('^', '**')
            # Reemplazar funciones comunes con sus equivalentes en sympy
            for old, new in [
                ('sin', 'sp.sin'),
                ('cos', 'sp.cos'),
                ('tan', 'sp.tan'),
                ('asin', 'sp.asin'),
                ('acos', 'sp.acos'),
                ('atan', 'sp.atan'),
                ('log', 'sp.log'),
                ('ln', 'sp.ln'),
                ('exp', 'sp.exp'),
                ('sqrt', 'sp.sqrt'),
                ('pi', 'sp.pi'),
                ('e', 'sp.E')
            ]:
                func_str = func_str.replace(old, new)
            
            # Convertir la expresión a una expresión sympy
            expr = eval(func_str, {"sp": sp, "Symbol": sp.Symbol}, self.symbols)
            return expr
        except Exception as e:
            raise ValueError(f"Error al parsear la función: {str(e)}")
    
    def compute_derivative(self, func_str, order=1, evaluate_at=None):
        """Calcula la derivada de una función
        
        Args:
            func_str: String con la función a derivar, ej: "x^2 + 2*x + 1"
            order: Orden de la derivada (1 para primera derivada, 2 para segunda, etc.)
            evaluate_at: Valor de x donde evaluar la derivada (opcional)
            
        Returns:
            Expresión simbólica de la derivada y su valor evaluado si se especifica
        """
        try:
            expr = self.parse_function(func_str)
            
            # Calcular la derivada del orden especificado
            derivative = expr
            for _ in range(order):
                derivative = sp.diff(derivative, self.x)
            
            # Evaluar en el punto si se especifica
            if evaluate_at is not None:
                evaluated = derivative.subs(self.x, evaluate_at)
                # Convertir a número flotante si es posible
                try:
                    evaluated = float(evaluated)
                except:
                    pass
                return {
                    'expression': sp.latex(derivative),
                    'evaluated': evaluated
                }
            
            return {
                'expression': sp.latex(derivative)
            }
        except Exception as e:
            raise ValueError(f"Error al calcular la derivada: {str(e)}")
    
    def get_function_latex(self, func_str):
        """Convierte una función a formato LaTeX"""
        try:
            expr = self.parse_function(func_str)
            return sp.latex(expr)
        except Exception as e:
            raise ValueError(f"Error al convertir a LaTeX: {str(e)}") 