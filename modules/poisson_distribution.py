import numpy as np
import math
from modules.linear_congruential import LinearCongruentialGenerator

class PoissonDistribution:
    def __init__(self, lambda_param):
        """
        Inicializa la distribución de Poisson.
        
        Args:
            lambda_param (float): Parámetro lambda (tasa media de ocurrencia)
        """
        if lambda_param <= 0:
            raise ValueError("El parámetro lambda debe ser positivo")
        self.lambda_param = lambda_param
        self.generator = LinearCongruentialGenerator()
    
    def generate_poisson(self, n_samples):
        """
        Genera números aleatorios que siguen una distribución de Poisson usando el método
        de transformación inversa con números uniformes del generador congruencial lineal.
        
        El método funciona de la siguiente manera:
        1. Genera números uniformes U(0,1) usando el generador congruencial
        2. Aplica la transformación inversa de la distribución de Poisson
        3. El resultado es un número aleatorio que sigue la distribución de Poisson
        
        Args:
            n_samples (int): Número de muestras a generar
            
        Returns:
            list: Lista de números que siguen una distribución de Poisson
        """
        if n_samples <= 0:
            raise ValueError("El número de muestras debe ser positivo")
            
        poisson_numbers = []
        exp_neg_lambda = np.exp(-self.lambda_param)
        
        for _ in range(n_samples):
            p = 1.0
            k = 0
            
            # Método de transformación inversa para Poisson
            while p > exp_neg_lambda:
                u = self.generator.generate()  # Número uniforme del generador congruencial
                p *= u
                k += 1
            
            poisson_numbers.append(k - 1)
        
        return poisson_numbers
    
    def get_theoretical_probabilities(self, max_k):
        """
        Calcula las probabilidades teóricas de la distribución de Poisson.
        
        La probabilidad P(X=k) para una distribución de Poisson es:
        P(X=k) = (λ^k * e^(-λ)) / k!
        
        Args:
            max_k (int): Valor máximo de k para calcular probabilidades
            
        Returns:
            tuple: (valores de k, probabilidades teóricas)
        """
        if max_k < 0:
            raise ValueError("El valor máximo de k debe ser no negativo")
            
        k_values = np.arange(max_k + 1)
        probabilities = np.exp(-self.lambda_param) * (self.lambda_param ** k_values) / np.array([math.factorial(k) for k in k_values])
        return k_values, probabilities 