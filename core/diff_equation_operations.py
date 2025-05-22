import sympy as sp
import numpy as np
import re
from typing import Dict, Tuple, List, Union, Callable

class DiffEquationOperations:
    def __init__(self):
        pass
    
    # MÉTODO ANALÍTICO
    def normalizar_raices(self, expr_str, func_name, indep_var):
        patrones = [
            (fr'sqrt\s*\(\s*{func_name}\s*\)', f'Pow({func_name}({indep_var}), Rational(1, 2))'),
            (fr'raiz\s*\(\s*{func_name}\s*\)', f'Pow({func_name}({indep_var}), Rational(1, 2))'),
            (r'sqrt\s*\(([^)]+)\)', r'Pow(\1, Rational(1, 2))'),
            (r'raiz\s*\(([^)]+)\)', r'Pow(\1, Rational(1, 2))')
        ]
        
        for patron, reemplazo in patrones:
            expr_str = re.sub(patron, reemplazo, expr_str, flags=re.IGNORECASE)
        
        # Manejar potencias fraccionarias
        expr_str = re.sub(
            r'(\w+|\([^)]+\))\s*[\^*]{1,2}\s*\((\d+)/(\d+)\)',
            lambda m: f'Pow({m.group(1)}{"(" + indep_var + ")" if m.group(1) == func_name else ""}, Rational({m.group(2)}, {m.group(3)}))',
            expr_str
        )
        
        return expr_str

    def preparar_ecuacion(self, ecuacion_str, func_name, indep_var):
        # Eliminar espacios
        ecuacion_str = ecuacion_str.replace(' ', '')
        
        # Convertir notación de Leibniz a Derivative
        ecuacion_str = re.sub(
            fr'd2{func_name}/d{indep_var}2',
            f'Derivative({func_name}({indep_var}), {indep_var}, {indep_var})',
            ecuacion_str
        )
        ecuacion_str = re.sub(
            fr'd{func_name}/d{indep_var}',
            f'Derivative({func_name}({indep_var}), {indep_var})',
            ecuacion_str
        )
        
        # Normalizar raíces
        ecuacion_str = self.normalizar_raices(ecuacion_str, func_name, indep_var)
        
        # Asegurar que la función tenga sus argumentos
        ecuacion_str = re.sub(fr'\b{func_name}\b(?!\()', f'{func_name}({indep_var})', ecuacion_str)
        
        return ecuacion_str

    def obtener_condiciones_iniciales(self, condiciones, x, y, x0):
        """Procesa las condiciones iniciales."""
        ics = {}
        y0 = None
        for ci_str, valor in condiciones.items():
            if 'd' + y.name in ci_str:
                ics[y.diff(x).subs(x, x0)] = valor
            elif y.name in ci_str:
                ics[y.subs(x, x0)] = valor
                y0 = valor
        return ics, y0

    def evaluar_solucion(self, sol_candidata, x0, h, y0, x):
        test_points = [x0, x0 + h, x0 + 2*h]
        for test_x in test_points:
            try:
                test_val = sol_candidata.rhs.subs(x, test_x)
                if isinstance(test_val, sp.Pow):
                    # Para expresiones con potencias, evaluar numéricamente
                    test_y = complex(test_val.evalf())
                    if abs(test_y.imag) > 1e-10:  # Tolerancia para parte imaginaria
                        return False
                    test_y = test_y.real
                else:
                    test_y = float(test_val.evalf())
                
                if not np.isfinite(test_y):
                    return False
                
                if test_x == x0 and y0 is not None:
                    if (y0 > 0 and test_y < 0) or (y0 < 0 and test_y > 0):
                        return False
            except:
                return False
        return True

    def resolver_analitico(self, ecuacion_str: str, condiciones_iniciales: dict, t_total: float, h: float, func_name: str = 'y', indep_var: str = 'x'):
        try:
            # Configuración inicial
            x = sp.Symbol(indep_var)
            y_func = sp.Function(func_name)
            y = y_func(x)
            
            # Preparar ecuación
            ecuacion_str = self.preparar_ecuacion(ecuacion_str, func_name, indep_var)
            
            # Separar LHS y RHS
            if '=' in ecuacion_str:
                lhs, rhs = ecuacion_str.split('=')
                
                # Crear diccionario local con todas las funciones necesarias
                local_dict = {
                    'Derivative': sp.Derivative,
                    'Pow': sp.Pow,
                    'Rational': sp.Rational,
                    'sqrt': sp.sqrt,
                    func_name: y_func,
                    indep_var: x
                }
                
                try:
                    lhs_expr = sp.parse_expr(lhs, local_dict=local_dict)
                    rhs_expr = sp.parse_expr(rhs, local_dict=local_dict)
                    expr = lhs_expr - rhs_expr
                except Exception as e:
                    return None, None, f"Error al parsear la ecuación: {e}"
            else:
                local_dict = {
                    'Derivative': sp.Derivative,
                    'Pow': sp.Pow,
                    'Rational': sp.Rational,
                    'sqrt': sp.sqrt,
                    func_name: y_func,
                    indep_var: x
                }
                expr = sp.parse_expr(ecuacion_str, local_dict=local_dict)
            
            # Obtener x0 y y0
            x0 = float(condiciones_iniciales.get(f"{indep_var}(0)", 0.0))
            y0 = None
            for ci_str, valor in condiciones_iniciales.items():
                if ci_str == f"{func_name}(0)":
                    y0 = float(valor)
                    break
            
            # Resolver la ecuación
            try:
                soluciones = sp.dsolve(expr, y)
                if not isinstance(soluciones, list):
                    soluciones = [soluciones]
            except Exception as e:
                return None, None, f"Error al resolver la ecuación: {e}"
            
            # Buscar solución válida
            for sol in soluciones:
                if not hasattr(sol, 'rhs'):
                    continue
                
                try:
                    # Encontrar las constantes en la solución
                    constantes = [sym for sym in sol.free_symbols if sym != x and sym != y]
                    
                    if not constantes:
                        # Si no hay constantes, verificar si la solución es válida directamente
                        if self.evaluar_solucion(sol, x0, h, y0, x):
                            tiempos = np.arange(x0, x0 + t_total + h, h)
                            f = sp.lambdify(x, sol.rhs, modules=['numpy'])
                            valores = f(tiempos)
                            if np.all(np.isfinite(valores)):
                                solucion_latex = sp.latex(sol.rhs)
                                return tiempos, valores, solucion_latex
                        continue
                    
                    # Crear ecuación con la condición inicial
                    if y0 is not None:
                        try:
                            # Resolver para las constantes usando y0
                            eq = sol.rhs.subs(x, x0) - y0
                            const_sols = sp.solve(eq, constantes[0], dict=True)
                            
                            if not isinstance(const_sols, list):
                                const_sols = [const_sols]
                            
                            for const_dict in const_sols:
                                if not isinstance(const_dict, dict):
                                    continue
                                    
                                sol_candidata = sol.subs(const_dict)
                                if self.evaluar_solucion(sol_candidata, x0, h, y0, x):
                                    tiempos = np.arange(x0, x0 + t_total + h, h)
                                    f = sp.lambdify(x, sol_candidata.rhs, modules=['numpy'])
                                    valores = f(tiempos)
                                    
                                    if np.all(np.isfinite(valores)):
                                        if np.any(np.iscomplex(valores)):
                                            valores = np.real(valores)
                                        solucion_latex = sp.latex(sol_candidata.rhs)
                                        return tiempos, valores, solucion_latex
                        except Exception as e:
                            continue
                
                except Exception as e:
                    continue
            
            return None, None, "No se encontró una solución válida"
            
        except Exception as e:
            return None, None, f"Error al resolver la ecuación: {str(e)}"
    
    # MÉTODO DE EULER
    def extraer_edo_primer_orden(self, ecuacion_str: str):
        # Eliminar espacios
        ecuacion_str = ecuacion_str.replace(' ', '')
        
        # Verificar formato dy/dx = f(x,y)
        if '=' not in ecuacion_str:
            return None, "La ecuación debe contener un signo de igualdad (=)"
        
        lhs, rhs = ecuacion_str.split('=')
        
        # Verificar que el lado izquierdo sea dy/dx
        if not (lhs == 'dy/dx' or lhs == 'd(y)/d(x)' or lhs == 'dy/d(x)' or lhs == 'd(y)/dx'):
            return None, "El lado izquierdo debe ser dy/dx"
        
        # Devolver el lado derecho como la función f(x,y)
        return rhs, None
    
    def resolver_euler(self, ecuacion_str: str, condiciones_iniciales: dict, t_total: float, h: float):
        try:
            # Extraer la función f(x,y) de la ecuación
            f_str, error = self.extraer_edo_primer_orden(ecuacion_str)
            if error:
                return None, None, error
            
            # Crear una función lambda para f(x,y)
            try:
                f = lambda x, y: eval(f_str, {"x": x, "y": y, "sin": np.sin, "cos": np.cos, "tan": np.tan, 
                                             "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi, "e": np.e})
            except Exception as e:
                return None, None, f"Error al crear la función: {str(e)}"
            
            # Obtener condiciones iniciales
            x0 = float(condiciones_iniciales.get("x(0)", 0.0))
            y0 = float(condiciones_iniciales.get("y(0)", 0.0))
            
            # Crear arrays para almacenar los resultados
            t_puntos = np.arange(x0, x0 + t_total + h/2, h)  # +h/2 para evitar problemas de redondeo
            n = len(t_puntos)
            y_valores = np.zeros(n)
            y_valores[0] = y0
            
            # Método de Euler
            for i in range(1, n):
                y_valores[i] = y_valores[i-1] + h * f(t_puntos[i-1], y_valores[i-1])
            
            return t_puntos, y_valores, "Solución numérica usando el método de Euler"
            
        except Exception as e:
            return None, None, f"Error al resolver con Euler: {str(e)}"
    
    # MÉTODO DE RUNGE-KUTTA
    def resolver_runge_kutta(self, ecuacion_str: str, condiciones_iniciales: dict, t_total: float, h: float):
        try:
            # Extraer la función f(x,y) de la ecuación
            f_str, error = self.extraer_edo_primer_orden(ecuacion_str)
            if error:
                return None, None, error
            
            # Crear una función lambda para f(x,y)
            try:
                f = lambda x, y: eval(f_str, {"x": x, "y": y, "sin": np.sin, "cos": np.cos, "tan": np.tan, 
                                             "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi, "e": np.e})
            except Exception as e:
                return None, None, f"Error al crear la función: {str(e)}"
            
            # Obtener condiciones iniciales
            x0 = float(condiciones_iniciales.get("x(0)", 0.0))
            y0 = float(condiciones_iniciales.get("y(0)", 0.0))
            
            # Crear arrays para almacenar los resultados
            t_puntos = np.arange(x0, x0 + t_total + h/2, h)  # +h/2 para evitar problemas de redondeo
            n = len(t_puntos)
            y_valores = np.zeros(n)
            y_valores[0] = y0
            
            # Método de Runge-Kutta de 4° orden
            for i in range(1, n):
                x = t_puntos[i-1]
                y = y_valores[i-1]
                
                k1 = h * f(x, y)
                k2 = h * f(x + h/2, y + k1/2)
                k3 = h * f(x + h/2, y + k2/2)
                k4 = h * f(x + h, y + k3)
                
                y_valores[i] = y + (k1 + 2*k2 + 2*k3 + k4) / 6
            
            return t_puntos, y_valores, "Solución numérica usando el método de Runge-Kutta de 4° orden"
            
        except Exception as e:
            return None, None, f"Error al resolver con Runge-Kutta: {str(e)}"

    def resolver_euler_heun(self, ecuacion_str: str, condiciones_iniciales: dict, t_total: float, h: float):
        try:
            # Extraer la función f(x,y) de la ecuación
            f_str, error = self.extraer_edo_primer_orden(ecuacion_str)
            if error:
                return None, None, error
            
            # Crear una función lambda para f(x,y)
            try:
                f = lambda x, y: eval(f_str, {"x": x, "y": y, "sin": np.sin, "cos": np.cos, "tan": np.tan, 
                                             "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi, "e": np.e})
            except Exception as e:
                return None, None, f"Error al crear la función: {str(e)}"
            
            # Obtener condiciones iniciales
            x0 = float(condiciones_iniciales.get("x(0)", 0.0))
            y0 = float(condiciones_iniciales.get("y(0)", 0.0))
            
            # Crear arrays para almacenar los resultados
            t_puntos = np.arange(x0, x0 + t_total + h/2, h)
            n = len(t_puntos)
            y_valores = np.zeros(n)
            y_valores[0] = y0
            
            # Método de Euler mejorado (Heun)
            for i in range(1, n):
                x = t_puntos[i-1]
                y = y_valores[i-1]
                
                # Predictor (Euler)
                y_pred = y + h * f(x, y)
                
                # Corrector (Heun)
                y_valores[i] = y + h * (f(x, y) + f(x + h, y_pred)) / 2
            
            return t_puntos, y_valores, "Solución numérica usando el método de Euler mejorado (Heun)"
            
        except Exception as e:
            return None, None, f"Error al resolver con Euler-Heun: {str(e)}"

    def resolver_taylor_orden2(self, ecuacion_str: str, condiciones_iniciales: dict, t_total: float, h: float):
        try:
            # Extraer la función f(x,y) de la ecuación
            f_str, error = self.extraer_edo_primer_orden(ecuacion_str)
            if error:
                return None, None, error
            
            # Crear una función lambda para f(x,y)
            try:
                f = lambda x, y: eval(f_str, {"x": x, "y": y, "sin": np.sin, "cos": np.cos, "tan": np.tan, 
                                             "exp": np.exp, "log": np.log, "sqrt": np.sqrt, "pi": np.pi, "e": np.e})
            except Exception as e:
                return None, None, f"Error al crear la función: {str(e)}"
            
            # Obtener condiciones iniciales
            x0 = float(condiciones_iniciales.get("x(0)", 0.0))
            y0 = float(condiciones_iniciales.get("y(0)", 0.0))
            
            # Crear arrays para almacenar los resultados
            t_puntos = np.arange(x0, x0 + t_total + h/2, h)
            n = len(t_puntos)
            y_valores = np.zeros(n)
            y_valores[0] = y0
            
            # Método de Taylor de orden 2
            for i in range(1, n):
                x = t_puntos[i-1]
                y = y_valores[i-1]
                
                # Calcular derivadas
                f_xy = f(x, y)
                
                # Aproximación de la segunda derivada usando diferencias finitas
                h_small = h/100  
                f_xy_plus = f(x + h_small, y + h_small * f_xy)
                f_xy_minus = f(x - h_small, y - h_small * f_xy)
                f_xy_prime = (f_xy_plus - f_xy_minus) / (2 * h_small)
                
                # Fórmula de Taylor de orden 2
                y_valores[i] = y + h * f_xy + (h**2/2) * f_xy_prime
            
            return t_puntos, y_valores, "Solución numérica usando el método de Taylor de orden 2"
            
        except Exception as e:
            return None, None, f"Error al resolver con Taylor: {str(e)}"

    def resolver_minimos_cuadrados(self, ecuacion_str: str, condiciones_iniciales: dict, t_total: float, h: float):
        try:
            # Primero obtener la solución analítica
            t_analitico, y_analitico, _ = self.resolver_analitico(
                ecuacion_str, condiciones_iniciales, t_total, h, "y", "x"
            )
            
            if t_analitico is None or y_analitico is None:
                return None, None, "No se pudo obtener la solución analítica para el ajuste"
            
            # Crear puntos para el ajuste
            x = t_analitico
            y = y_analitico
            
            # Calcular la regresión lineal (y = mx + b)
            n = len(x)
            sum_x = np.sum(x)
            sum_y = np.sum(y)
            sum_xy = np.sum(x * y)
            sum_xx = np.sum(x * x)
            
            # Calcular pendiente (m) y ordenada al origen (b)
            m = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
            b = (sum_y - m * sum_x) / n
            
            # Calcular los valores ajustados (y = mx + b)
            y_ajustado = m * x + b
            
            # Calcular el coeficiente de determinación (R²)
            y_mean = np.mean(y)
            ss_tot = np.sum((y - y_mean) ** 2)
            ss_res = np.sum((y - y_ajustado) ** 2)
            r_squared = 1 - (ss_res / ss_tot)
            
            return x, y_ajustado, f"Solución usando regresión lineal (y = {m:.4f}x + {b:.4f}, R² = {r_squared:.4f})"
            
        except Exception as e:
            return None, None, f"Error al resolver con mínimos cuadrados: {str(e)}" 