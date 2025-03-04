from ..clases.Actualizar import *

def p_actualizar(t):
    """actualizar : ACTUALIZAR IDENTIFICADOR COLOCAR lista_asignaciones opt_condiciones
                  | ACTUALIZAR IDENTIFICADOR COLOCAR lista_asignaciones
    """
    if len(t) == 6:
        t[0] = Actualizar(nombre_tabla=t[2], asignacion=t[4], condicionales=t[5])  
    else:
        t[0] = Actualizar(nombre_tabla=t[2], asignacion=t[4])


def p_lista_asignaciones(t):
    """lista_asignaciones : asignacion
                          | lista_asignaciones COMA asignacion"""
    if len(t) == 2:  # Caso base: una sola asignación
        t[0] = f"{t[1]}"
    else:  # Caso recursivo: varias asignaciones
        t[0] = f"{t[1]}, {t[3]}"
        
def p_asignacion(t):
    """asignacion : IDENTIFICADOR IGUALDAD valor"""
    t[0] = f"{t[1]} {t[2]} {t[3]}"
    
