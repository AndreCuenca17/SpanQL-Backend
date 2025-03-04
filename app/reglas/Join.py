# Regla principal para JOIN
# UNIR tipo_join nombreTabla CON condicion
def p_unir(t):
    """unir : UNIR tipo_unir IDENTIFICADOR CON condicion"""
    # t[3]: nombre de la tabla que se une
    # t[5]: condición del JOIN
    t[0] = ("join", t[2], t[3], t[5])

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