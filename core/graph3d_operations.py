import numpy as np
import sympy as sp
import re

class Graph3DOperations:
    def __init__(self):
        self.x = sp.Symbol('x')
        self.y = sp.Symbol('y')
        self.symbols = {'x': self.x, 'y': self.y}
    
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
    
    def generate_surface_data(self, func_str, x_min=-5, x_max=5, y_min=-5, y_max=5, points=30):
        """Genera los datos para graficar una superficie 3D
        
        Args:
            func_str: String con la función a graficar, ej: "x^2 + y^2"
            x_min: Valor mínimo de x
            x_max: Valor máximo de x
            y_min: Valor mínimo de y
            y_max: Valor máximo de y
            points: Número de puntos a calcular en cada eje
            
        Returns:
            Diccionario con los valores de x, y, z para la superficie
        """
        try:
            # Limpiar la expresión para evaluación numérica
            expr = self.limpiar_expr(func_str)
            
            # Generar valores de x e y
            x = np.linspace(x_min, x_max, points)
            y = np.linspace(y_min, y_max, points)
            X, Y = np.meshgrid(x, y)
            
            # Calcular valores de z
            Z = np.zeros_like(X)
            for i in range(points):
                for j in range(points):
                    try:
                        Z[i, j] = eval(expr, {"x": X[i, j], "y": Y[i, j], "np": np})
                    except:
                        Z[i, j] = np.nan  # Usar NaN para discontinuidades
            
            return {
                'X': X,
                'Y': Y,
                'Z': Z,
                'expr': expr,
                'latex': self.get_function_latex(func_str)
            }
        except Exception as e:
            raise ValueError(f"Error al generar datos para la gráfica 3D: {str(e)}")
    
    def generate_contour_data(self, func_str, x_min=-5, x_max=5, y_min=-5, y_max=5, points=100):
        """Genera los datos para graficar un mapa de contorno 2D
        
        Args:
            func_str: String con la función a graficar, ej: "x^2 + y^2"
            x_min: Valor mínimo de x
            x_max: Valor máximo de x
            y_min: Valor mínimo de y
            y_max: Valor máximo de y
            points: Número de puntos a calcular en cada eje
            
        Returns:
            Diccionario con los valores de x, y, z para el contorno
        """
        # Usamos la misma función que para la superficie
        return self.generate_surface_data(func_str, x_min, x_max, y_min, y_max, points) 