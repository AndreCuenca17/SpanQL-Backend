from ..clases.Soltar import Soltar
from ..clases.Soltar import soltar_condicional

def p_soltar(t):
    """soltar : SOLTAR TABLA lista_identificadores
              | SOLTAR TABLA condicional_soltar lista_identificadores"""
    if len(t) == 4:
        t[0] = Soltar(tabla= t[3])
    else:
        t[0] = soltar_condicional(tabla= t[4])

def p_lista_identificadores(t):
    """lista_identificadores : IDENTIFICADOR
                             | lista_identificadores COMA IDENTIFICADOR"""
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[3]]

def p_condicional(t):
    """condicional_soltar : SI EXISTE """
    t[0] = t[1] + t[2]
