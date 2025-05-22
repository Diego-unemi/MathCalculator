import sympy as sp
import numpy as np
from sympy.parsing.sympy_parser import parse_expr

class DerivativeOperations:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.symbols = {'x': self.x}
    
    def parse_function(self, func_str):
        try:
            func_str = func_str.replace('^', '**')
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
            
            expr = eval(func_str, {"sp": sp, "Symbol": sp.Symbol}, self.symbols)
            return expr
        except Exception as e:
            raise ValueError(f"Error al parsear la función: {str(e)}")
    
    def compute_derivative(self, func_str, order=1, evaluate_at=None):
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
        try:
            expr = self.parse_function(func_str)
            return sp.latex(expr)
        except Exception as e:
            raise ValueError(f"Error al convertir a LaTeX: {str(e)}") 