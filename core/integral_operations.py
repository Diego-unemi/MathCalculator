import sympy as sp
import numpy as np
from sympy.utilities.lambdify import lambdify

class IntegralOperations:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.symbols = {'x': self.x}
    
    def parse_function(self, func_str):
        try:
            # Reemplazar X por x para evitar errores de mayúsculas
            func_str = func_str.replace('X', 'x')
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
    
    def get_numpy_function(self, func_str):
        try:
            expr = self.parse_function(func_str)
            # Usar lambdify con módulos específicos para mejor compatibilidad
            return lambdify(self.x, expr, modules=['numpy', 'math'])
        except Exception as e:
            raise ValueError(f"Error al convertir la función a formato numpy: {str(e)}")
    
    def compute_indefinite_integral(self, func_str):
        try:
            expr = self.parse_function(func_str)
            integral = sp.integrate(expr, self.x)
            return {
                'expression': sp.latex(integral),
                'with_constant': sp.latex(integral) + " + C"
            }
        except Exception as e:
            raise ValueError(f"Error al calcular la integral indefinida: {str(e)}")
    
    def compute_definite_integral(self, func_str, lower_bound, upper_bound):
        try:
            expr = self.parse_function(func_str)
            
            # Convertir límites a valores simbólicos si es necesario
            try:
                lower = float(lower_bound)
            except:
                lower = sp.sympify(lower_bound)
                
            try:
                upper = float(upper_bound)
            except:
                upper = sp.sympify(upper_bound)
            
            integral = sp.integrate(expr, (self.x, lower, upper))
            
            # Convertir a número flotante si es posible
            try:
                result = float(integral)
            except:
                result = integral
                
            return {
                'expression': sp.latex(expr),
                'bounds': (lower_bound, upper_bound),
                'result': result,
                'result_latex': sp.latex(integral)
            }
        except Exception as e:
            raise ValueError(f"Error al calcular la integral definida: {str(e)}")
    
    def get_function_latex(self, func_str):
        """Convierte una función a formato LaTeX"""
        try:
            expr = self.parse_function(func_str)
            return sp.latex(expr)
        except Exception as e:
            raise ValueError(f"Error al convertir a LaTeX: {str(e)}") 