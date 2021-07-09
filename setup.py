import setuptools
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


INSTALL_REQUIRES = [
    "click<7.2.0,>=7.1.1",
    "comtypes>=1.1.10; platform_system=='Windows'",
    "docx2pdf",
    "docx2txt==0.8",
    "gensim==4.0.1",
    "googletrans==2.4.0",
    "jellyfish==0.8.2",
    "langid==1.1.6",
    "matplotlib>=3.3.4",
    "networkx==2.5.1",
    "nltk==3.6.2",
    "pandas>=0.25.3",
    "pdf2image==1.16.0",
    "PyPDF2==1.26.0",
    "pyspellchecker==0.6.2",
    "pytesseract==0.3.7; python_version<'3.8'",
    "pytesseract>=0.3.7; python_version>='3.8'",
    "opencv-python>=4.5.2.54",
    "reportlab==3.5.68",
    "scikit-learn>=0.24.2",
    "slate3k==0.5.3",
    "spacy>=3.0.6",
    "stanza>=1.2.1",
    "wordcloud>=1.8.1",
]

PACKAGE_NAME = "ConTexto"

setuptools.setup(
    name=PACKAGE_NAME,
    version="0.2.0",
    author="Departamento Nacional de Planeación - DNP",
    author_email="ucd@dnp.gov.co",
    maintainer="Unidad de Científicos de Datos - UCD",
    maintainer_email="ucd@dnp.gov.co",
    description=(
        "Librería para el procesamiento y análisis de texto con Python"
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    keywords=[
        "Python",
        "OCR",
        "NLP",
        "Español",
        "Text processing",
        "UCD",
        "DNP",
    ],
    url="https://github.com/ucd-dnp/ConTexto",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    project_urls={
        "Documentación": "https://ucd-dnp.github.io/contexto/",
        "Seguimiento de fallas": "https://github.com/ucd-dnp/ConTexto/issues",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6.1",
)
