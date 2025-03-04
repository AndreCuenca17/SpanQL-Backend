from ..clases.Crear import Crear

def p_crear(t):
    """crear : CREAR TABLA IDENTIFICADOR PARENTESIS_IZQ lista_columnas_crear PARENTESIS_DER"""

    nombre_tabla = t[3]
    columnas_lista = []  
    llave_primaria = None
    llaves_foraneas = {}

    for sublista in t[5]:
        columna = sublista[0]
        nombre_columna, tipo_dato, restricciones  = columna
         
        columnas_lista.append((nombre_columna, tipo_dato, restricciones))  

        if "CLAVE PRIMARIA" in restricciones:
            llave_primaria = nombre_columna  

        for restriccion in restricciones:
            if isinstance(restriccion, tuple) and restriccion[0] == "CLAVE FORANEA":
                tabla_ref, columna_ref = restriccion[1]
                llaves_foraneas[nombre_columna] = f"{tabla_ref}.{columna_ref}"

    t[0] = Crear(nombre_tabla, columnas_lista, llave_primaria, llaves_foraneas)

def p_lista_columnas_crear(t):
    """lista_columnas_crear : lista_columnas_crear COMA lista_columna_crear
                      | lista_columna_crear"""
    if len(t) == 4:
        t[0] = t[1] + [t[3]]
    else:
        t[0] = [t[1]]