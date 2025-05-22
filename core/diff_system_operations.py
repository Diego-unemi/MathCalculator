import sympy as sp
import numpy as np
import re
import logging
from typing import Dict, Tuple, List, Union

logger = logging.getLogger(__name__)

class DiffSystemOperations:
    def __init__(self):
        self.t = sp.Symbol('t')
        self.x = sp.Function('x')(self.t)
        self.y = sp.Function('y')(self.t)
    
    def _preprocesar_ecuacion(self, eq: str) -> str:
        try:
            eq = eq.strip()
            
            if '=' not in eq:
                raise ValueError("La ecuación debe contener un signo igual (=)")
            
            lhs, rhs = eq.split('=')
            lhs = lhs.strip()
            rhs = rhs.strip()
            
            lhs = lhs.lower()
            if lhs in ['dx/dt', 'dx/d(t)', 'd(x)/dt', 'd(x)/d(t)']:
                lhs = 'Derivative(x(t), t)'
            elif lhs in ['dy/dt', 'dy/d(t)', 'd(y)/dt', 'd(y)/d(t)']:
                lhs = 'Derivative(y(t), t)'
            else:
                raise ValueError("El lado izquierdo debe ser dx/dt o dy/dt")
            
            rhs = re.sub(r'(\d),(\d)', r'\1.\2', rhs)
            rhs = re.sub(r'(\d*\.?\d+)([a-zA-Z])', r'\1*\2', rhs)
            rhs = re.sub(r'([a-zA-Z])\s+([a-zA-Z])', r'\1*\2', rhs)
            rhs = re.sub(r'(\))(\w)', r'\1*\2', rhs)
            rhs = re.sub(r'(\d*\.?\d+)(\()', r'\1*\2', rhs)
            
            return f"{lhs} = {rhs}"
        except Exception as e:
            raise ValueError(f"Error al preprocesar la ecuación: {str(e)}")
    
    def preparar_sistema(self, sistema_str: str) -> Tuple[sp.Matrix, sp.Matrix]:
        """Prepara el sistema de ecuaciones diferenciales en formato matricial."""
        try:
            # Convertir el string del sistema en ecuaciones
            ecuaciones = sistema_str.strip().split('\n')
            if len(ecuaciones) != 2:
                raise ValueError("El sistema debe tener exactamente dos ecuaciones, una por línea.")
            
            # Preprocesar ecuaciones
            eq1 = self._preprocesar_ecuacion(ecuaciones[0])
            eq2 = self._preprocesar_ecuacion(ecuaciones[1])
            
            # Parsear expresiones
            try:
                eq1 = sp.parse_expr(eq1)
                eq2 = sp.parse_expr(eq2)
            except Exception as e:
                raise ValueError(f"Error al parsear las ecuaciones: {str(e)}")
            
            # Extraer coeficientes de x y y
            A = sp.Matrix([
                [-sp.diff(eq1, self.x), -sp.diff(eq1, self.y)],
                [-sp.diff(eq2, self.x), -sp.diff(eq2, self.y)]
            ])
            
            # Extraer términos independientes
            b = sp.Matrix([
                -eq1.subs({sp.diff(self.x, self.t): 0, sp.diff(self.y, self.t): 0}),
                -eq2.subs({sp.diff(self.x, self.t): 0, sp.diff(self.y, self.t): 0})
            ])
            
            return A, b
            
        except Exception as e:
            logger.error(f"Error al preparar el sistema: {str(e)}")
            raise ValueError(f"Error al preparar el sistema: {str(e)}")
    
    def _convertir_a_complejo(self, expr):
        """
        Convierte una expresión simbólica de SymPy a un número complejo de Python.
        
        Args:
            expr: Expresión simbólica de SymPy
            
        Returns:
            Número complejo de Python
        """
        try:
            # Evaluar la expresión simbólica numéricamente
            expr_eval = sp.N(expr)
            # Si es un número real simple
            if isinstance(expr_eval, (sp.core.numbers.Float, sp.core.numbers.Integer)):
                return complex(float(expr_eval), 0)
            # Si es un número complejo de sympy
            if isinstance(expr_eval, sp.core.numbers.ComplexInfinity):
                raise ValueError("Complejo infinito no soportado")
            # Si es una expresión con I o compleja
            try:
                valor = complex(expr_eval)
                return valor
            except Exception:
                # Si falla, intentar extraer parte real e imaginaria
                try:
                    real = float(expr_eval.as_real_imag()[0])
                    imag = float(expr_eval.as_real_imag()[1])
                    return complex(real, imag)
                except Exception:
                    # Último intento: evaluar como float
                    return complex(float(expr_eval))
        except Exception as e:
            logger.error(f"Error al convertir expresión a complejo: {str(e)}")
            raise ValueError(f"No se pudo convertir la expresión a número complejo: {expr}")

    def calcular_valores_propios(self, A):
        """
        Calcula los valores propios de la matriz A.
        
        Args:
            A: Matriz del sistema
            
        Returns:
            Lista de valores propios ordenados por parte real descendente
        """
        try:
            # Obtener valores propios
            valores_propios = A.eigenvals()
            
            # Convertir a lista y ordenar por parte real descendente
            valores_propios_lista = []
            for valor, _ in valores_propios.items():
                try:
                    # Convertir a número complejo
                    valor_complejo = self._convertir_a_complejo(valor)
                    
                    # Redondear a 6 decimales
                    valor_real = round(valor_complejo.real, 6)
                    valor_imag = round(valor_complejo.imag, 6)
                    
                    # Si la parte imaginaria es muy pequeña, considerarla como 0
                    if abs(valor_imag) < 1e-10:
                        valores_propios_lista.append((valor_real, 0))
                    else:
                        valores_propios_lista.append((valor_real, valor_imag))
                        
                except Exception as e:
                    logger.warning(f"Error al procesar valor propio {valor}: {str(e)}")
                    continue
            
            # Ordenar por parte real descendente
            valores_propios_lista.sort(key=lambda x: x[0], reverse=True)
            
            # Convertir a formato de string
            valores_propios_str = []
            for real, imag in valores_propios_lista:
                if abs(imag) < 1e-10:
                    valores_propios_str.append(f"λ = {real:.6f}")
                else:
                    signo = '+' if imag >= 0 else '-'
                    valores_propios_str.append(f"λ = {real:.6f} {signo} {abs(imag):.6f}i")
            
            return valores_propios_str
            
        except Exception as e:
            logger.error(f"Error al calcular valores propios: {str(e)}")
            raise ValueError(f"Error al calcular valores propios: {str(e)}")
    
    def calcular_vectores_propios(self, A: sp.Matrix) -> List[Tuple[str, int, List[List[complex]]]]:
        """Calcula los vectores propios de la matriz del sistema y los devuelve como listas de números (no strings)."""
        try:
            eigenvects = A.eigenvects()
            vectores_propios_formateados = []
            for valor_propio, multiplicidad, vectores in eigenvects:
                try:
                    vectores_numericos = []
                    for v in vectores:
                        v_num = []
                        for comp in v:
                            try:
                                comp_complejo = self._convertir_a_complejo(comp)
                                comp_real = round(comp_complejo.real, 6)
                                comp_imag = round(comp_complejo.imag, 6)
                                if abs(comp_imag) < 1e-10:
                                    v_num.append(comp_real)
                                else:
                                    v_num.append(complex(comp_real, comp_imag))
                            except Exception as e:
                                logger.warning(f"Error al procesar componente {comp}: {str(e)}")
                                continue
                        if len(v_num) == 2:
                            vectores_numericos.append(v_num)
                    valor_complejo = self._convertir_a_complejo(valor_propio)
                    valor_real = round(valor_complejo.real, 6)
                    valor_imag = round(valor_complejo.imag, 6)
                    if abs(valor_imag) < 1e-10:
                        valor_str = f"{valor_real:.6f}"
                    else:
                        signo = '+' if valor_imag >= 0 else '-'
                        valor_str = f"{valor_real:.6f} {signo} {abs(valor_imag):.6f}i"
                    if vectores_numericos:
                        vectores_propios_formateados.append((valor_str, multiplicidad, vectores_numericos))
                except Exception as e:
                    logger.warning(f"Error al procesar vector propio para valor {valor_propio}: {str(e)}")
                    continue
            if not vectores_propios_formateados:
                raise ValueError("No se pudieron procesar los vectores propios")
            return vectores_propios_formateados
        except Exception as e:
            logger.error(f"Error al calcular vectores propios: {str(e)}")
            raise ValueError(f"Error al calcular vectores propios: {str(e)}")
    
    def resolver_sistema(self, sistema_str: str, condiciones_iniciales: Dict[str, float], t_total: float, h: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray, Dict]:
        """Resuelve el sistema de ecuaciones diferenciales y retorna la solución y análisis."""
        try:
            if t_total <= 0 or h <= 0:
                raise ValueError("El tiempo total y el paso deben ser positivos")
            A, b = self.preparar_sistema(sistema_str)
            valores_propios = self.calcular_valores_propios(A)
            vectores_propios = self.calcular_vectores_propios(A)
            lambda1_str = valores_propios[0].split('=')[1].strip()
            lambda2_str = valores_propios[1].split('=')[1].strip()
            
            def parse_lambda(lstr):
                lstr = lstr.replace(' ', '')
                if 'i' in lstr:
                    lstr = lstr.replace('i','j')
                    lstr = re.sub(r'([+-])j', r'\g<1>1j', lstr)
                    lstr = re.sub(r'^j', '1j', lstr)
                    lstr = re.sub(r'^-j', '-1j', lstr)
                    match = re.match(r'^([+-]?\d*\.?\d+)([+-]\d*\.?\d+)j$', lstr)
                    if match:
                        real = float(match.group(1))
                        imag = float(match.group(2))
                        return complex(real, imag)
                    match_imag = re.match(r'^([+-]?\d*\.?\d+)j$', lstr)
                    if match_imag:
                        return complex(0, float(match_imag.group(1)))
                    match_real = re.match(r'^([+-]?\d*\.?\d+)$', lstr)
                    if match_real:
                        return float(match_real.group(1))
                    try:
                        return complex(lstr)
                    except Exception as e:
                        logger.error(f"parse_lambda: string no reconocido: {lstr}")
                        raise
                else:
                    return float(lstr)
            lambda1 = parse_lambda(lambda1_str)
            lambda2 = parse_lambda(lambda2_str)
            v1 = vectores_propios[0][2][0]
            v2 = vectores_propios[1][2][0]
            v1_arr = np.array([complex(x) for x in v1])
            v2_arr = np.array([complex(x) for x in v2])
            v1_norm = v1_arr / np.linalg.norm(v1_arr)
            v2_norm = v2_arr / np.linalg.norm(v2_arr)
            C1, C2 = sp.symbols('C1 C2')
            t = sp.Symbol('t')
            x_sol = C1 * v1_norm[0] * sp.exp(lambda1 * t) + C2 * v2_norm[0] * sp.exp(lambda2 * t)
            y_sol = C1 * v1_norm[1] * sp.exp(lambda1 * t) + C2 * v2_norm[1] * sp.exp(lambda2 * t)
            x0 = condiciones_iniciales.get('x(0)', 0)
            y0 = condiciones_iniciales.get('y(0)', 0)
            const_sols = sp.solve([
                x_sol.subs(t, 0) - x0,
                y_sol.subs(t, 0) - y0
            ], [C1, C2])
            if const_sols is False or const_sols is None:
                raise ValueError("No se pudieron determinar las constantes de integración.")
            t_puntos = np.arange(0, t_total + h, h)
            try:
                x_sol_final = sp.lambdify(t, x_sol.subs(const_sols), 'numpy')
                y_sol_final = sp.lambdify(t, y_sol.subs(const_sols), 'numpy')
                x_valores = x_sol_final(t_puntos)
                y_valores = y_sol_final(t_puntos)
                if np.any(np.iscomplex(x_valores)):
                    x_valores = np.real(x_valores)
                if np.any(np.iscomplex(y_valores)):
                    y_valores = np.real(y_valores)
                x_valores = np.round(x_valores, 6)
                y_valores = np.round(y_valores, 6)
            except Exception as eval_err:
                logger.error(f"Error al evaluar la solución: {str(eval_err)}")
                raise ValueError(f"Error al evaluar la solución: {str(eval_err)}")
            if x_valores is None or y_valores is None:
                raise ValueError("La solución no pudo ser evaluada numéricamente.")
            
            info_valores_propios = "\n".join(valores_propios)
            def format_vector(v):
                return f"[{v[0]}, {v[1]}]"
            info_vectores_propios = "\n".join([
                f"Para {v[0]}:\n" + "\n".join([f"  Vector: {format_vector(vec)}" for vec in v[2]])
                for v in vectores_propios
            ])
            info_adicional = {
                'matriz_sistema': str(A),
                'vector_independiente': str(b),
                'valores_propios': info_valores_propios,
                'vectores_propios': info_vectores_propios,
                'solucion_x': str(x_sol.subs(const_sols)),
                'solucion_y': str(y_sol.subs(const_sols))
            }
            return t_puntos, x_valores, y_valores, info_adicional
        except Exception as e:
            logger.error(f"Error al resolver el sistema: {str(e)}")
            raise ValueError(f"Error al resolver el sistema: {str(e)}")
    
    def analizar_estabilidad(self, valores_propios: List[sp.Expr]) -> str:
        """Analiza la estabilidad del sistema basado en los valores propios."""
        try:
            vals = [complex(str(v)) for v in valores_propios]
            
            if all(v.real < 0 for v in vals):
                return "El sistema es asintóticamente estable (sumidero)"
            elif all(v.real > 0 for v in vals):
                return "El sistema es inestable (fuente)"
            elif any(v.real == 0 for v in vals):
                return "El sistema es marginalmente estable (centro)"
            else:
                return "El sistema tiene comportamiento mixto"
                
        except Exception as e:
            logger.error(f"Error al analizar estabilidad: {str(e)}")
            raise ValueError(f"Error al analizar estabilidad: {str(e)}") 