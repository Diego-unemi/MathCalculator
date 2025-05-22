import sympy as sp
import numpy as np

class EquationOperations:
    def __init__(self):
        self.x = sp.symbols("x")
        self.y = sp.symbols("y")
        
    def solve_linear_equation(self, a, b):
        """Resuelve una ecuación lineal de la forma ax + b = 0"""
        try:
            if a == 0:
                if b == 0:
                    return ["Infinitas soluciones"]
                else:
                    return ["Sin solución"]
            
            eq = sp.Eq(a * self.x + b, 0)
            sols = sp.solve(eq, self.x)
            return [float(sol) for sol in sols]
        except Exception as e:
            raise ValueError(f"Error al resolver la ecuación: {str(e)}")
    
    def solve_quadratic_equation(self, a, b, c):
        """Resuelve una ecuación cuadrática de la forma ax^2 + bx + c = 0"""
        try:
            if a == 0:
                return self.solve_linear_equation(b, c)
                
            eq = sp.Eq(a * self.x**2 + b * self.x + c, 0)
            sols = sp.solve(eq, self.x)
            
            # Convertir a formato complejo si es necesario
            result = []
            for sol in sols:
                if sp.im(sol) == 0:
                    result.append(float(sol))
                else:
                    real = float(sp.re(sol))
                    imag = float(sp.im(sol))
                    # Formatear complejos como "a+bi" o "a-bi"
                    if imag >= 0:
                        result.append(f"{real:.4f}+{imag:.4f}i")
                    else:
                        result.append(f"{real:.4f}{imag:.4f}i")
            
            return result
        except Exception as e:
            raise ValueError(f"Error al resolver la ecuación: {str(e)}")
    
    def solve_system_2x2(self, a1, b1, c1, a2, b2, c2):
        """Resuelve un sistema de ecuaciones 2x2
        a1*x + b1*y = c1
        a2*x + b2*y = c2
        """
        try:
            eq1 = sp.Eq(a1 * self.x + b1 * self.y, c1)
            eq2 = sp.Eq(a2 * self.x + b2 * self.y, c2)
            
            sols = sp.solve((eq1, eq2), (self.x, self.y))
            
            if not sols:
                return "Sin solución o infinitas soluciones"
            
            x_val = float(sols[self.x])
            y_val = float(sols[self.y])
            
            return {"x": x_val, "y": y_val}
        except Exception as e:
            raise ValueError(f"Error al resolver el sistema: {str(e)}")
    
    def get_equation_string(self, eq_type, *coeffs):
        """Devuelve la representación en texto de una ecuación"""
        try:
            if eq_type == "Lineal":
                a, b = coeffs
                eq = sp.Eq(a * self.x + b, 0)
            elif eq_type == "Cuadrática":
                a, b, c = coeffs
                eq = sp.Eq(a * self.x**2 + b * self.x + c, 0)
            elif eq_type == "Sistema 2x2":
                a1, b1, c1, a2, b2, c2 = coeffs
                eq1 = sp.Eq(a1 * self.x + b1 * self.y, c1)
                eq2 = sp.Eq(a2 * self.x + b2 * self.y, c2)
                return f"{sp.latex(eq1)}, {sp.latex(eq2)}"
            
            return str(eq)
        except Exception as e:
            return f"Error al formatear ecuación: {str(e)}" 