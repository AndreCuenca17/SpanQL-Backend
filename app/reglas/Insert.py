from ..clases.Insertar import Insertar

# INSERT INTO nombreTabla (columna1,columna2) VALORES ('Mantari',9.9)
def p_insertar(t):
    """insertar : INSERTAR_EN IDENTIFICADOR PARENTESIS_IZQ lista_columnas_creadas PARENTESIS_DER VALORES lista_filas"""
    # t[2] -> nombre de la tabla
    # t[4] -> columnas
    # t[7] -> valores
    # ("insertar_en", t[2], t[4], t[7])
    t[0] = Insertar(t[2], t[4], t[7])


def p_lista_columnas_creadas(t):
    """lista_columnas_creadas : IDENTIFICADOR
    | lista_columnas_creadas COMA IDENTIFICADOR"""
    if len(t) == 4:
        t[0] = t[1] + [t[3]]
    else:
        t[0] = [t[1]]


def p_lista_filas(t):
    """lista_filas : fila
    | lista_filas COMA fila"""
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = [t[1]] + [t[3]]


def p_fila(t):
    """fila : PARENTESIS_IZQ lista_valores PARENTESIS_DER"""
    t[0] = t[2]


def p_lista_valores(t):
    """lista_valores : valor
    | lista_valores COMA valor
    | lista_valores COMA NULO
    |"""
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[3]]
