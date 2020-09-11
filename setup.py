import setuptools

with open("README.md", "r", encoding ='utf-8') as fh:
    long_description = fh.read()

INSTALL_REQUIRES = []
PACKAGE_NAME = 'ConTexto'

setuptools.setup(
    name=PACKAGE_NAME,
    version='0.0.1',
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
    keywords= 'python OCR texto'
    url='https://github.com/ucd-dnp/ConTexto',
    packages=setuptools.find_packages(),
    include_package_data = True,
    install_requires = ['numpy>=1.18.4',
                        'pandas==1.0.3',
                        'scipy==1.5.1',
                        'pytz==2020.1',
                        'xlrd==1.2.0',
                        'certifi==2020.4.5.1',
                        'chardet==3.0.4',
                        'idna==2.9',
                        'Jinja2==2.11.2',
                        'MarkupSafe==1.1.1',
                        'python-dateutil==2.8.1',
                        'requests==2.23.0',
                        'six==1.14.0',
                        'sodapy==2.1.0',
                        'urllib3==1.25.9',
                        'phik==0.10.0'],
    
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",        
    ],
    python_requires='>=3.6',
)