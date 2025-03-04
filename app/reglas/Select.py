from ..clases.Seleccion import Seleccion

def p_seleccion(t):
    """seleccion : SELECCIONAR lista_floro lista_columnas DESDE IDENTIFICADOR opt_condiciones
                 | SELECCIONAR lista_floro lista_columnas DESDE IDENTIFICADOR opt_condiciones unir"""
    # t[1] : SELECCIONAR
    # t[2] : lista_floro
    # t[3] : lista_columnas
    # t[4] : DESDE
    # t[5] : IDENTIFICADOR (nombre de la tabla)
    # t[6] : opt_condiciones (lista de cláusulas, o [] si no hay)
    # t[7] : unir (el JOIN)
    if len(t) == 7:  # Sin JOIN
        t[0] = Seleccion(columnas=t[3], tabla=t[5], condiciones=t[6])
    else:  # Con JOIN
        t[0] = Seleccion(columnas=t[3], tabla=t[5], condiciones=t[6], unir=t[7])


def p_lista_floro(t):
    """lista_floro : lista_floro floro
                   | floro"""
    if len(t) == 3:
        t[0] = (t[1], t[2])
    else:
        t[0] = t[1]


def p_floro(t):
    """floro : DISTINTO
             | empty"""
    if t[1] == "DISTINTO":  # Se encontró la palabra DISTINCT
        t[0] = "DISTINTO"
    else:
        t[0] = None


def p_lista_columnas(t):
    """lista_columnas : IDENTIFICADOR
                      | lista_columnas COMA IDENTIFICADOR
                      | TODO"""
    if len(t) == 2:
        if t[1] == "TODO":
            t[0] = ["*"]  # Reemplaza "TODO" por "*"
        else:
            t[0] = [t[1]]
    elif len(t) == 4:
        t[0] = t[1] + [t[3]]  # Concatena las columnas correctamente
        
# Regla principal para JOIN
# UNIR tipo_join nombreTabla CON condicion
def p_unir(t):
    """unir : UNIR tipo_unir IDENTIFICADOR CON condicion"""
    # t[3]: nombre de la tabla que se une
    # t[5]: condición del JOIN
    t[0] = (t[2], t[3], t[5])

# Tipos de JOIN (NORMAL, IZQUIERDO, DERECHO, COMPLETO)
def p_tipo_unir(t):
    """tipo_unir : NORMAL
                 | IZQUIERDO
                 | DERECHO
                 | COMPLETO
                 | empty"""
    t[0] = t[1] if t[1] is not None else "NORMAL"  # Si no se especifica, asumimos NORMAL (INNER JOIN)

# Regla para la condición del JOIN
# Ejemplo: tabla1.id = tabla2.id
def p_condicion(t):
    """condicion : especificacion IGUALDAD especificacion"""
    t[0] = (t[1], "=", t[3])

# Regla para manejar `empty`, que representa un valor opcional
def p_empty(t):
    """empty :"""
    t[0] = None

def p_especificacion(t):
    """especificacion : IDENTIFICADOR PARENTESIS_IZQ IDENTIFICADOR PARENTESIS_DER"""
    t[0] = (t[3], "from", t[1])

