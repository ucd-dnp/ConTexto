import setuptools
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


INSTALL_REQUIRES = [
    "click==8.1.3",
    "docx2txt==0.8",
    "gensim==4.3.1",
    "googletrans==3.0.0",
    "jellyfish==0.9.0",
    "langid==1.1.6",
    "matplotlib==3.7.1",
    "networkx==3.0",
    "nltk==3.8.1",
    "pandas==1.5.3",
    "pdf2image==1.16.3",
    "PyPDF2==3.0.1",
    "pyspellchecker==0.7.1",
    "pytesseract==0.3.10",
    "python-docx==0.8.11",
    "opencv-python==4.7.0.72",
    "reportlab==3.6.12",
    "scikit-learn==1.2.2",
    "slate3k==0.5.3",
    "spacy==3.5.1",
    "stanza==1.5.0",
    "wordcloud==1.8.2.2",
]

PACKAGE_NAME = "ConTexto"

setuptools.setup(
    name=PACKAGE_NAME,
    version="0.2.0",
    author="Departamento Nacional de Planeación - DNP",
    author_email="ucd@dnp.gov.co",
    maintainer="Unidad de Científicos de Datos - UCD",
    maintainer_email="ucd@dnp.gov.co",
    description=("Librería para el procesamiento y análisis de texto con Python"),
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
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.6.2",
)
