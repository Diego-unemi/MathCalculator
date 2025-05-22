import numpy as np
from typing import List, Optional

class CongruentialGenerator:
    """
    Implementación del generador congruencial lineal para números pseudoaleatorios.
    X_{n+1} = (a * X_n + c) mod m
    donde:
    - a: multiplicador
    - c: incremento
    - m: módulo
    - X_0: semilla inicial
    """
    
    DEFAULT_SEED = 12345

    def __init__(self, seed: Optional[int] = None, a: int = 1664525, c: int = 1013904223, m: int = 2**32):
        """
        Inicializa el generador con los parámetros dados.
        
        Args:
            seed: Semilla inicial (X_0). Si es None, se usa DEFAULT_SEED.
            a: Multiplicador
            c: Incremento
            m: Módulo
        """
        self.seed = seed if seed is not None else self.DEFAULT_SEED
        self.a = a
        self.c = c
        self.m = m
        self.current = self.seed
        
    def generate(self) -> float:
        """
        Genera el siguiente número pseudoaleatorio en el rango [0,1).
        
        Returns:
            float: Número pseudoaleatorio entre 0 y 1
        """
        self.current = (self.a * self.current + self.c) % self.m
        return self.current / self.m
    
    def generate_sequence(self, n: int) -> List[float]:
        """
        Genera una secuencia de n números pseudoaleatorios.
        
        Args:
            n: Cantidad de números a generar
            
        Returns:
            List[float]: Lista de n números pseudoaleatorios
        """
        return [self.generate() for _ in range(n)]
    
    def reset(self, seed: Optional[int] = None) -> None:
        """
        Reinicia el generador con una nueva semilla o la semilla original.
        
        Args:
            seed: Nueva semilla (opcional)
        """
        if seed is not None:
            self.seed = seed
        self.current = self.seed

# Ejemplo de uso
if __name__ == "__main__":
    # Crear un generador con parámetros por defecto
    generator = CongruentialGenerator()
    
    # Generar 5 números aleatorios
    random_numbers = generator.generate_sequence(5)
    print("Números aleatorios generados:", random_numbers)
    
    # Reiniciar el generador con una nueva semilla
    generator.reset(42)
    print("\nNúmeros aleatorios con nueva semilla:", generator.generate_sequence(5)) 