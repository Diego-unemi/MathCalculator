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
                     y_min_rect: float,
                     y_max_rect: float,
                     n_points: int = 10000) -> Tuple[float, float]:
        """Estima el área bajo una curva usando el método de Monte Carlo (acierto/fallo)."""
        x_rand = np.array([a + (b - a) * self.generator.generate() for _ in range(n_points)])
        y_rand = np.array([y_min_rect + (y_max_rect - y_min_rect) * self.generator.generate() for _ in range(n_points)])
        
        func_values = np.array([func(x) for x in x_rand])
        
        count = 0
        for i in range(n_points):
            f_val = func(x_rand[i])
            is_between_fn_and_axis = (y_rand[i] >= 0 and y_rand[i] <= f_val) or \
                                     (y_rand[i] < 0 and y_rand[i] >= f_val)
            is_within_rect_y = (y_rand[i] >= y_min_rect and y_rand[i] <= y_max_rect)
            
            if is_between_fn_and_axis and is_within_rect_y:
                count += 1
        
        points_hit_ratio = count / n_points
        total_sampling_area = (b - a) * (y_max_rect - y_min_rect)
        area = total_sampling_area * points_hit_ratio
        
        error_in_ratio = np.sqrt(points_hit_ratio * (1 - points_hit_ratio) / n_points)
        error = total_sampling_area * error_in_ratio
        
        return area, error

    def estimate_area_between_curves(self,
                                     func1: Callable[[float], float],
                                     func2: Callable[[float], float],
                                     a: float, b: float,
                                     n_points: int = 10000) -> Tuple[float, float, List[float], List[float], List[bool]]:
        """Estima el área entre dos curvas func1(x) y func2(x) en el intervalo [a,b]."""
        x_sample_for_range = np.linspace(a, b, 200)
        y1_sample_for_range = np.array([func1(x) for x in x_sample_for_range])
        y2_sample_for_range = np.array([func2(x) for x in x_sample_for_range])

        y_min_sampling = 0.0
        y_max_sampling = 1.0
        
        if y_min_sampling == y_max_sampling:
            y_min_sampling -= 0.1
            y_max_sampling += 0.1
            if y_min_sampling == y_max_sampling:
                 y_max_sampling = y_min_sampling + 1.0

        x_rand_points = np.array([a + (b - a) * self.generator.generate() for _ in range(n_points)])
        y_rand_points = np.array([y_min_sampling + (y_max_sampling - y_min_sampling) * self.generator.generate() for _ in range(n_points)])
        
        count_inside = 0
        is_inside_flags = []

        for i in range(n_points):
            x = x_rand_points[i]
            y = y_rand_points[i]
            val1 = func1(x)
            val2 = func2(x)
            
            if val1 <= y <= val2:
                count_inside += 1
                is_inside_flags.append(True)
            else:
                is_inside_flags.append(False)
        
        points_hit_ratio = count_inside / n_points
        total_sampling_rectangle_area = (b - a) * (y_max_sampling - y_min_sampling)
        
        estimated_area = total_sampling_rectangle_area * points_hit_ratio
        
        error_in_ratio = np.sqrt(points_hit_ratio * (1 - points_hit_ratio) / n_points)
        estimated_error = total_sampling_rectangle_area * error_in_ratio
        
        return estimated_area, estimated_error, x_rand_points.tolist(), y_rand_points.tolist(), is_inside_flags

    def estimate_pi(self, n_points: int = 10000) -> Tuple[float, float, List[float], List[float], List[bool]]:
        """Estima el valor de π usando el método de Monte Carlo."""
        x_rand_points = np.array([2 * self.generator.generate() - 1 for _ in range(n_points)])
        y_rand_points = np.array([2 * self.generator.generate() - 1 for _ in range(n_points)])
        
        is_inside_flags = (x_rand_points**2 + y_rand_points**2) <= 1
        points_in_circle = np.sum(is_inside_flags)
        
        pi_estimate = 4 * points_in_circle / n_points
        
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