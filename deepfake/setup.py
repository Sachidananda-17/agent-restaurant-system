from setuptools import setup, find_packages

setup(
    name="deepfake-detection",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'uagents',
        'torch',
        'torchvision',
        'opencv-python',
        'numpy',
        'Pillow',
        'reportlab',
        'fpdf2'
    ]
)
