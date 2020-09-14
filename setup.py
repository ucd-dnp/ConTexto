import setuptools
import sys

with open("README.md", "r", encoding ='utf-8') as fh:
    long_description = fh.read()


TORCH36 = 'torch @ https://download.pytorch.org/whl/cpu/torch-1.6.0%2Bcpu-cp36-cp36m-win_amd64.whl'
TORCH_VISION36 = 'torchvision @ https://download.pytorch.org/whl/cpu/torchvision-0.7.0%2Bcpu-cp36-cp36m-win_amd64.whl'

TORCH37 = 'torch @ https://download.pytorch.org/whl/cpu/torch-1.6.0%2Bcpu-cp37-cp37m-win_amd64.whl'
TORCH_VISION37 = 'torchvision @ https://download.pytorch.org/whl/cpu/torchvision-0.7.0%2Bcpu-cp37-cp37m-win_amd64.whl'

TORCH38 = 'torch @ https://download.pytorch.org/whl/cpu/torch-1.6.0%2Bcpu-cp38-cp38-win_amd64.whl'
TORCH_VISION38 = 'torchvision @ https://download.pytorch.org/whl/cpu/torchvision-0.7.0%2Bcpu-cp38-cp38-win_amd64.whl'


INSTALL_REQUIRES = ['gensim==3.8.3',
                    'googletrans==3.0.0',
                    'jellyfish==0.8.2',
                    'langid==1.1.6',
                    'matplotlib==3.3.1',
                    'networkx==2.5',
                    'nltk==3.5',
                    'numpy==1.19.1',
                    'pandas==1.1.1',
                    'pdf2image==1.14.0',
                    'pyspellchecker==0.5.5',
                    'PyPDF2==1.26.0',
                    'python-docx==0.8.10',
                    'pywin32==228',
                    'opencv-python==4.4.0.42',
                    'pytesseract==0.3.5',
                    'reportlab==3.5.48',
                    'scikit-learn==0.23.2',
                    'spacy==2.3.2',
                    'stanza==1.1.1',
                    TORCH36,
                    TORCH_VISION36,
                    'wordcloud==1.8.0']

PACKAGE_NAME = 'ConTexto'

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.1.0',
    author="Departamento Nacional de Planeación - DNP",
    author_email='ucd@dnp.gov.co',
    maintainer='Unidad de Científicos de Datos - UCD',
    maintainer_email='ucd@dnp.gov.co',
    description=(
        "Librería para el procesamiento y análisis de texto con Python"
        ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license = 'MIT',
    keywords= 'python OCR texto',
    url='https://github.com/ucd-dnp/ConTexto',
    packages=setuptools.find_packages(),
    include_package_data = True,
    install_requires = INSTALL_REQUIRES,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",        
    ],
    python_requires=">=3.6.*"
)

