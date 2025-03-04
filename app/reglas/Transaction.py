def p_transaccion_iniciar(t):
    "transaccion : INICIAR_TRANSACCION"
    t[0] = ("transaccion", t[1])

def p_transaccion_confirmar(t):
    "transaccion : CONFIRMAR"
    t[0] = ("transaccion", t[1])

def p_transaccion_revertir(t):
    "transaccion : REVERTIR"
    t[0] = ("transaccion", t[1])
