from setuptools import setup

setup(
    name="MathCalculator",
    version="1.0",
    packages=["views"],
    install_requires=[
        "flet>=0.10.0",
        "matplotlib>=3.7.0",
    ],
    entry_points={
        "console_scripts": [
            "mathcalculator=app:main",
        ],
    },
) 