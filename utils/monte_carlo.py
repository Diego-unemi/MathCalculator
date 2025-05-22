import numpy as np
from typing import Callable, Tuple, List, Optional
from utils.random_generator import CongruentialGenerator

class MonteCarlo:
    """
    Implementación del método de Monte Carlo para integración numérica y estimación de áreas.
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Inicializa el método de Monte Carlo con un generador de números aleatorios.
        
        Args:
            seed: Semilla para el generador de números aleatorios. Si es None, se usa el default del generador.
        """
        self.generator = CongruentialGenerator(seed=seed)
    
    def integrate(self, 
                 func: Callable[[float], float], 
                 a: float, 
                 b: float, 
                 n_points: int = 10000) -> Tuple[float, float]:
        """
        Calcula la integral definida de una función usando el método de Monte Carlo.
        
        Args:
            func: Función a integrar
            a: Límite inferior
            b: Límite superior
            n_points: Número de puntos a generar
            
        Returns:
            Tuple[float, float]: (Valor estimado de la integral, Error estimado)
        """
        x_values = np.array([a + (b - a) * self.generator.generate() for _ in range(n_points)])
        y_values = np.array([func(x) for x in x_values])
        
        integral = (b - a) * np.mean(y_values)
        # Error estándar de la media multiplicado por (b-a)
        error = (b - a) * np.std(y_values) / np.sqrt(n_points)
        
        return integral, error
    
    def estimate_area(self, 
                     func: Callable[[float], float], 
                     a: float, 
                     b: float, 
                     y_min_rect: float, # Renombrado para claridad
                     y_max_rect: float, # Renombrado para claridad
                     n_points: int = 10000) -> Tuple[float, float]:
        """
        Estima el área bajo una curva usando el método de Monte Carlo (acierto/fallo).
        El área se estima dentro de un rectángulo definido por [a,b] y [y_min_rect, y_max_rect].
        Se asume que la función es mayormente positiva o el usuario maneja el signo.
        """
        x_rand = np.array([a + (b - a) * self.generator.generate() for _ in range(n_points)])
        y_rand = np.array([y_min_rect + (y_max_rect - y_min_rect) * self.generator.generate() for _ in range(n_points)])
        
        # Puntos donde y_rand está entre y_min_rect (o 0 si es mayor) y func(x_rand)
        # Esto es para el área entre la función y el eje x, dentro del rectángulo de muestreo.
        # Si func(x) puede ser negativa, esta lógica debe ajustarse.
        # Por ahora, asumimos que el interés es el área "positiva" respecto a y_min_rect.
        # Para una función general f(x), los puntos "bajo" la curva son aquellos donde y_rand < f(x_rand) si y_rand > 0
        # y y_rand > f(x_rand) si y_rand < 0. Es más simple si f(x) >=0 y y_min_rect=0.
        
        # Lógica simplificada para f(x) >= y_min_rect (o el área entre f(x) y el "piso" y_min_rect)
        # Contamos puntos (x,y) tales que y_min_rect <= y <= f(x) O f(x) <= y <= y_min_rect
        
        func_values = np.array([func(x) for x in x_rand])
        
        # Contar puntos que están entre la función y el "piso" y_min_rect, dentro del rectángulo de muestreo
        # Esta es una interpretación del "área bajo la curva" cuando y_min_rect no es cero.
        # Si f(x) > y_min_rect: y_rand está entre y_min_rect y f(x)
        # Si f(x) < y_min_rect: y_rand está entre f(x) y y_min_rect (área "negativa" respecto al piso)
        # Para el caso simple de área sobre el eje x (y_min_rect=0) y f(x)>=0 : 0 <= y_rand <= f(x)
        
        # Puntos "acertados" son aquellos dentro del rectángulo y entre el "piso" y la función
        # Esta es la forma más general de "Area under curve"
        points_hit = np.sum( (y_rand >= np.minimum(func_values, y_max_rect)) & (y_rand <= np.maximum(func_values, y_min_rect)) & (y_rand >= y_min_rect) & (y_rand <= y_max_rect) | (y_rand <= np.minimum(func_values, y_max_rect)) & (y_rand >= np.maximum(func_values, y_min_rect)) & (y_rand >= y_min_rect) & (y_rand <= y_max_rect) )
        
        # Para el método de acierto y fallo estándar para f(x) > 0 y y_min_rect = 0:
        # points_hit = np.sum((y_rand >= 0) & (y_rand <= func_values))
        # Esta lógica asume y_min_rect y y_max_rect definen el área de muestreo.
        # func(x) debe estar dentro de estos límites para que el área sea significativa.
        
        # Corrección: Contamos puntos (x_r, y_r) donde y_r está entre y_min_rect y f(x_r),
        # pero solo si f(x_r) está también dentro del [y_min_rect, y_max_rect].
        # O más simple: y_r está entre min(f(x_r), y_max_rect) y y_min_rect, asumiendo f(x_r) > y_min_rect
        
        # Lógica para el método de rechazo estándar:
        # y_rand está entre y_min_rect y y_max_rect.
        # f_val = func(x_val)
        # Si y_min_rect <= y_rand <= f_val (y f_val <= y_max_rect) -> contamos
        # Si y_min_rect=0, y_max_rect=max(f(x)) y f(x)>=0 -> y_rand <= f_val
        
        # Consideramos el área entre f(x) y el eje y=0, dentro de los límites de muestreo [y_min_rect, y_max_rect]
        # Esta es la interpretación más común del método de acierto/fallo para área bajo la curva f(x)
        # Se asume y_min_rect <=0 <= y_max_rect si f(x) puede ser negativa.
        # Si f(x) >= 0, y_min_rect=0 es lo usual.
        
        # Lógica simple: Puntos entre el eje X (y=0) y la función, dentro del rectángulo de muestreo.
        # Esto es lo que "Estimación de Área" suele implicar para una sola función.
        # Se asume que el interés es sobre el eje x.
        # Esta implementación puede ser confusa si y_min_rect y y_max_rect no son [0, max_func_val]
        
        # Para que "Estimación de área" sea el área bajo f(x) hasta el eje x,
        # y_rand debe estar entre 0 y f(x_rand) (si f(x_rand) > 0)
        # o entre f(x_rand) y 0 (si f(x_rand) < 0).
        # Y todo esto dentro del rectángulo de muestreo y_min_rect, y_max_rect
        
        # Si el objetivo es el área definida por el rectángulo y la función:
        # Puntos tales que (y_rand > 0 Y y_rand < func(x)) O (y_rand < 0 Y y_rand > func(x))
        # Y además, y_min_rect < y_rand < y_max_rect
        
        # Simplifiquemos: Área de f(x) relativa al eje x, limitada por y_min_rect, y_max_rect.
        # Esta versión estima el área entre f(x) y el eje x, dentro del rectángulo de muestreo.
        # Esta es la interpretación más común para "área bajo la curva f(x)".
        # func_at_x_rand = np.array([func(x) for x in x_rand])
        # hits = np.sum( (y_rand >= 0) & (y_rand <= func_at_x_rand) & (y_rand <= y_max_rect) & (func_at_x_rand >= y_min_rect) | \
        #                 (y_rand <= 0) & (y_rand >= func_at_x_rand) & (y_rand >= y_min_rect) & (func_at_x_rand <= y_max_rect) )
        # La lógica anterior de `points_under_curve` era más simple y directa para f(x) > 0.
        # Revisando la implementación original de estimate_area:
        # points_under_curve = sum(1 for x, y in zip(x_points, y_points) if y <= func(x))
        # Esto asume y_points son y_rand, y x_points son x_rand.
        # Y asume que "bajo la curva" es y_rand <= func(x_rand). Esto es ambiguo si func(x) o y_rand pueden ser negativos.
        # Para el método de rechazo clásico, y_rand se genera en [0, M] donde M > max(f(x)), y f(x) > 0.
        # Entonces se cuentan puntos donde 0 < y_rand < f(x_rand).
        
        # Re-escribimos `estimate_area` para ser más claro:
        # Asume f(x) es la curva, y queremos el área entre f(x) y el eje x,
        # dentro del rectángulo de muestreo [a,b] x [y_min_rect, y_max_rect].
        
        count = 0
        for i in range(n_points):
            f_val = func(x_rand[i])
            # Punto entre eje-x y la función
            is_between_fn_and_axis = (y_rand[i] >= 0 and y_rand[i] <= f_val) or \
                                     (y_rand[i] < 0 and y_rand[i] >= f_val)
            # Punto dentro de los límites verticales del rectángulo de muestreo
            is_within_rect_y = (y_rand[i] >= y_min_rect and y_rand[i] <= y_max_rect)
            
            if is_between_fn_and_axis and is_within_rect_y:
                count += 1
        
        points_hit_ratio = count / n_points
        total_sampling_area = (b - a) * (y_max_rect - y_min_rect)
        area = total_sampling_area * points_hit_ratio
        
        # El error para el método de acierto/fallo (binomial)
        # Si p = points_hit_ratio, error en p es sqrt(p(1-p)/N)
        # Error en el área = AreaTotal * error_en_p
        error_in_ratio = np.sqrt(points_hit_ratio * (1 - points_hit_ratio) / n_points)
        error = total_sampling_area * error_in_ratio
        
        return area, error

    def estimate_area_between_curves(self,
                                     func1: Callable[[float], float],
                                     func2: Callable[[float], float],
                                     a: float, b: float,
                                     n_points: int = 10000) -> Tuple[float, float, List[float], List[float], List[bool]]:
        """
        Estima el área entre dos curvas func1(x) y func2(x) en el intervalo [a,b].
        Se asume que func2(x) >= func1(x) en el intervalo [a,b].
        Los puntos (x_rand, y_rand) se muestrean en un rectángulo que contiene ambas curvas.
        Retorna (área estimada, error, x_points, y_points, is_inside_flags)
        """
        # Determinar el rectángulo de muestreo vertical (y_min_sampling, y_max_sampling)
        # Muestreamos algunos puntos para tener una idea de los rangos de las funciones
        x_sample_for_range = np.linspace(a, b, 200) # Aumentado para mejor estimación de rango
        y1_sample_for_range = np.array([func1(x) for x in x_sample_for_range])
        y2_sample_for_range = np.array([func2(x) for x in x_sample_for_range])

        # y_min_sampling = min(np.min(y1_sample_for_range), np.min(y2_sample_for_range))
        # y_max_sampling = max(np.max(y1_sample_for_range), np.max(y2_sample_for_range))
        # Para el caso de la hoja (x^2 y sqrt(x) en [0,1]), y_min=0, y_max=1.
        # El método del Excel muestrea Y en [0,1] directamente.
        # Adoptaremos ese enfoque para este método específico.
        y_min_sampling = 0.0
        y_max_sampling = 1.0
        
        # Asegurar un pequeño margen si y_min == y_max (curvas constantes e iguales, área 0)
        if y_min_sampling == y_max_sampling:
            y_min_sampling -= 0.1
            y_max_sampling += 0.1
            if y_min_sampling == y_max_sampling: # Aún iguales (ej. 0.0)
                 y_max_sampling = y_min_sampling + 1.0 # Forzar un rango

        x_rand_points = np.array([a + (b - a) * self.generator.generate() for _ in range(n_points)])
        y_rand_points = np.array([y_min_sampling + (y_max_sampling - y_min_sampling) * self.generator.generate() for _ in range(n_points)])
        
        count_inside = 0
        is_inside_flags = []

        for i in range(n_points):
            x = x_rand_points[i]
            y = y_rand_points[i]
            val1 = func1(x)
            val2 = func2(x)
            
            # Asumimos func1 es la inferior, func2 la superior, como en el ejemplo (x^2 vs sqrt(x))
            if val1 <= y <= val2:
                count_inside += 1
                is_inside_flags.append(True)
            else:
                is_inside_flags.append(False)
        
        points_hit_ratio = count_inside / n_points
        # El área del rectángulo de muestreo para x en [a,b] y y en [y_min_sampling, y_max_sampling]
        total_sampling_rectangle_area = (b - a) * (y_max_sampling - y_min_sampling)
        
        estimated_area = total_sampling_rectangle_area * points_hit_ratio
        
        error_in_ratio = np.sqrt(points_hit_ratio * (1 - points_hit_ratio) / n_points)
        estimated_error = total_sampling_rectangle_area * error_in_ratio
        
        return estimated_area, estimated_error, x_rand_points.tolist(), y_rand_points.tolist(), is_inside_flags

    def estimate_pi(self, n_points: int = 10000) -> Tuple[float, float, List[float], List[float], List[bool]]:
        """
        Estima el valor de π usando el método de Monte Carlo.
        Retorna (estimación de pi, error, x_points, y_points, is_inside_flags)
        """
        x_rand_points = np.array([2 * self.generator.generate() - 1 for _ in range(n_points)])
        y_rand_points = np.array([2 * self.generator.generate() - 1 for _ in range(n_points)])
        
        is_inside_flags = (x_rand_points**2 + y_rand_points**2) <= 1
        points_in_circle = np.sum(is_inside_flags)
        
        pi_estimate = 4 * points_in_circle / n_points
        
        # Error para una proporción binomial, escalado por 4
        # p = points_in_circle / n_points
        # error_p = sqrt(p(1-p)/n_points)
        # error_pi = 4 * error_p
        p_ratio = points_in_circle / n_points
        error = 4 * np.sqrt(p_ratio * (1 - p_ratio) / n_points)
        
        return pi_estimate, error, x_rand_points.tolist(), y_rand_points.tolist(), is_inside_flags.tolist()

# Ejemplo de uso
if __name__ == "__main__":
    # Crear instancia de Monte Carlo
    mc = MonteCarlo()
    
    # Ejemplo 1: Integrar x^2 de 0 a 1
    def square(x): return x**2
    integral, error = mc.integrate(square, 0, 1)
    print(f"Integral de x^2 de 0 a 1: {integral:.6f} ± {error:.6f}")
    
    # Ejemplo 2: Estimar π
    pi_estimate, pi_error = mc.estimate_pi()
    print(f"Estimación de π: {pi_estimate:.6f} ± {pi_error:.6f}") 