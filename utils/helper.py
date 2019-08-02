import os

# leer archivo '.RData' como una dataframe pandas
def load_rdata_file(filename):
    r_data = robjects.r['get'](robjects.r['load'](filename))
    df = pandas2ri.ri2py(r_data)
    return df

# Escribir pandas dataframe en un archivo '.RData'
def save_rdata_file(df, filename):
    r_data = pandas2ri.py2ri(df)
    robjects.r.assign("datos", r_data)
    robjects.r("save(datos, file='{}')".format(filename))
    

######### Definición de funciones para buscar en el texto  #########
def buscar_en_texto(texto, lista=[]):
    return any(i in texto for i in lista)

def is_in_text(text, lista=[], lista_2 = []):
    isin = False
    count = 0
    for string in lista:
        if all(i in text for i in string.split('|')):
            if string not in lista_2:
                return True
            else:
                count+=1
                if count > 1:
                    return True
    return isin


def verify_create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)