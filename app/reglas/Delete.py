from ..clases.Eliminar import Eliminar

# DELETE FROM 'nombreTabla'
def p_eliminar(t):
    """eliminar : eliminar_todo
                | eliminar_donde
                | eliminar_hasta_todo
                | eliminar_hasta_donde"""
    t[0] = t[1] # t[3] es el nombre de la tabla

# 1️⃣ Eliminar todos los registros de la tabla
def p_eliminar_todo(t):
    """eliminar_todo : ELIMINAR DESDE IDENTIFICADOR"""
    t[0] = Eliminar(tabla = t[3])

def p_eliminar_donde(t):
    """eliminar_donde : ELIMINAR DESDE IDENTIFICADOR clausula"""
    t[0] = Eliminar(tabla= t[3], clausula = t[4])

# 3️⃣ Eliminar los primeros `N` registros sin condición
def p_eliminar_hasta_todo(t):
    """eliminar_hasta_todo : ELIMINAR PRIMEROS VALOR_NUMERO DESDE IDENTIFICADOR"""
    t[0] = Eliminar(tabla=t[5], limite=t[3])  # `t[3]` es `N`, `t[5]` es la tabla

# 4️⃣ Eliminar los primeros `N` registros con una condición
def p_eliminar_hasta_donde(t):
    """eliminar_hasta_donde : ELIMINAR PRIMEROS VALOR_NUMERO DESDE IDENTIFICADOR clausula"""
    # `t[3]` es `N`, `t[5]` es la tabla, `t[6]` la condición
    t[0] = Eliminar(tabla=t[5], clausula=t[6], limite=t[3])  

def p_clausula(t):
    """clausula : DONDE condicioncita"""
    t[0] = t[2]
def p_condicioncita(t):
    """condicioncita : IDENTIFICADOR comparador valor
                    | condicioncita Y condicioncita
                    | condicioncita O condicioncita"""
    if len(t) == 4:
        if t[2].upper() == "Y":
            t[2] = "AND"
        elif t[2].upper() == "O":
            t[2] = "OR"
        t[0] = f"{t[1]} {t[2]} {t[3]}"
    else:
        t[0] = f"{t[1]} {t[2]} {t[3]}" 
    
def p_comparador(t):
    """comparador : IGUALDAD
                  | MAYOR
                  | MENOR
                  | MAYOR_IGUAL
                  | MENOR_IGUAL
                  | DIFERENTE"""
    t[0] = t[1]

def p_valor(t):
    """valor : VALOR_NUMERO
             | VALOR_CADENA
             | VALOR_BOOLEANO
             | VALOR_FLOTANTE"""
    t[0] = t[1]