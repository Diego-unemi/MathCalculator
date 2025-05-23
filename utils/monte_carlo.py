import numpy as np
from typing import Callable, Tuple, List, Optional
from utils.random_generator import CongruentialGenerator

class MonteCarlo:
    
    def __init__(self, seed: Optional[int] = None):
        self.generator = CongruentialGenerator(seed=seed)
    
    def integrate(self, 
                 func: Callable[[float], float], 
                 a: float, 
                 b: float, 
                 n_points: int = 10000) -> Tuple[float, float]:
       
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
       
        x_rand = np.array([a + (b - a) * self.generator.generate() for _ in range(n_points)])
        y_rand = np.array([y_min_rect + (y_max_rect - y_min_rect) * self.generator.generate() for _ in range(n_points)])
        
        
        func_values = np.array([func(x) for x in x_rand])
        
        
        # Area entre la curva"
        points_hit = np.sum( (y_rand >= np.minimum(func_values, y_max_rect)) & (y_rand <= np.maximum(func_values, y_min_rect)) & (y_rand >= y_min_rect) & (y_rand <= y_max_rect) | (y_rand <= np.minimum(func_values, y_max_rect)) & (y_rand >= np.maximum(func_values, y_min_rect)) & (y_rand >= y_min_rect) & (y_rand <= y_max_rect) )
        
        
        
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
        
        
        error_in_ratio = np.sqrt(points_hit_ratio * (1 - points_hit_ratio) / n_points)
        error = total_sampling_area * error_in_ratio
        
        return area, error

    def estimate_area_between_curves(self,
                                     func1: Callable[[float], float],
                                     func2: Callable[[float], float],
                                     a: float, b: float,
                                     n_points: int = 10000) -> Tuple[float, float, List[float], List[float], List[bool]]:
        
        
        x_sample_for_range = np.linspace(a, b, 200) 
        y1_sample_for_range = np.array([func1(x) for x in x_sample_for_range])
        y2_sample_for_range = np.array([func2(x) for x in x_sample_for_range])

        
        y_min_sampling = 0.0
        y_max_sampling = 1.0
        
        # Asegurar un pequeño margen si y_min == y_max (curvas constantes e iguales, área 0)
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