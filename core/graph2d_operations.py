import numpy as np
import sympy as sp
import re

class Graph2DOperations:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.symbols = {'x': self.x}
    
    def limpiar_expr(self, func_str):
        """Limpia la expresión para hacerla compatible con evaluación numérica"""
        expr = func_str.replace("^", "**")
        # Lista de funciones trigonométricas y otras funciones matemáticas
        funciones = ['sin', 'cos', 'tan', 'log', 'exp', 'sqrt']
        
        # Primero reemplazamos las funciones trigonométricas con un marcador temporal
        for func in funciones:
            expr = expr.replace(func, f"__{func}__")
        
        # Aplicamos las reglas de multiplicación
        expr = re.sub(r"(\d)([a-zA-Z(])", r"\1*\2", expr)         # 2x → 2*x, 3sin(x) → 3*sin(x)
        expr = re.sub(r"([a-zA-Z\)])(\()", r"\1*(", expr)         # x(y+1) → x*(y+1)
        expr = re.sub(r"(\))([a-zA-Z\(])", r"\1*\2", expr)        # (x+1)sin(x) → (x+1)*sin(x)
        expr = re.sub(r"([a-zA-Z])(\d)", r"\1*\2", expr)          # x2 → x*2
        
        # Restauramos las funciones trigonométricas
        for func in funciones:
            expr = expr.replace(f"__{func}__", f"np.{func}")
        
        return expr
    
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
    
    def get_function_latex(self, func_str):
        """Convierte una función a formato LaTeX"""
        try:
            expr = self.parse_function(func_str)
            return sp.latex(expr)
        except Exception as e:
            raise ValueError(f"Error al convertir a LaTeX: {str(e)}")
    
    def generate_plot_data(self, func_str, x_min=-10, x_max=10, points=400):
        """Genera los datos para graficar una función 2D
        
        Args:
            func_str: String con la función a graficar, ej: "x^2 + 2*x + 1"
            x_min: Valor mínimo de x
            x_max: Valor máximo de x
            points: Número de puntos a calcular
            
        Returns:
            Diccionario con los valores de x e y
        """
        try:
            # Limpiar la expresión para evaluación numérica
            expr = self.limpiar_expr(func_str)
            
            # Generar valores de x
            x_vals = np.linspace(x_min, x_max, points)
            
            # Calcular valores de y
            y_vals = []
            for x in x_vals:
                try:
                    y = eval(expr, {"x": x, "np": np})
                    y_vals.append(y)
                except:
                    y_vals.append(np.nan)  # Usar NaN para discontinuidades
            
            return {
                'x': x_vals.tolist(),
                'y': y_vals,
                'expr': expr,
                'latex': self.get_function_latex(func_str)
            }
        except Exception as e:
            raise ValueError(f"Error al generar datos para la gráfica: {str(e)}") 