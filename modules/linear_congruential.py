class LinearCongruentialGenerator:
    def __init__(self, seed=None):
        """
        Inicializa el generador congruencial lineal.
        
        Args:
            seed (int, optional): Semilla inicial. Si no se proporciona, se usa un valor por defecto.
        """
        # Parámetros del generador (usando parámetros de MINSTD)
        self.m = 2147483647  # 2^31 - 1
        self.a = 16807       # Multiplicador
        self.c = 0           # Incremento
        
        # Inicializar la semilla
        self.seed = seed if seed is not None else 12345
        self.current = self.seed
    
    def generate(self):
        """
        Genera un número pseudoaleatorio en el intervalo [0,1).
        
        Returns:
            float: Número pseudoaleatorio entre 0 y 1
        """
        # Fórmula del generador congruencial lineal
        self.current = (self.a * self.current + self.c) % self.m
        
        # Normalizar al intervalo [0,1)
        return self.current / self.m
    
    def generate_sequence(self, n):
        """
        Genera una secuencia de n números pseudoaleatorios.
        
        Args:
            n (int): Número de elementos a generar
            
        Returns:
            list: Lista de n números pseudoaleatorios
        """
        return [self.generate() for _ in range(n)] 