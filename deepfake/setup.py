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
        'numpy==1.24.3',
        'Pillow',
        'reportlab',
        'fpdf2',
        'gdown==4.7.1',
        'exifread==3.0.0',
        'imagehash==4.3.1',
        'matplotlib'
    ]
)
