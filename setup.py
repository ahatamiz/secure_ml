import os
from setuptools import setup


def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join('.', 'requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements


packages = [
    'secure_ml',
    "secure_ml.attack",
    "secure_ml.defense",
    "secure_ml.utils"
]

console_scripts = [
]

setup(
    name='secure_ml',
    version='0.0.0',
    description='package to implemet secure machine learning algorythm',
    author='Hideaki Takahashi',
    author_email='koukyosyumei@hotmail.com',
    license="MIT",
    install_requires=read_requirements(),
    url="https://github.com/Koukyosyumei/secure_ml",
    packages=packages,
    entry_points={'console_scripts': console_scripts},
)
