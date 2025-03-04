import ply.lex as lex

tokens = [
    # Definición de Datos
    "CREAR",  # CREATE
    "ALTERAR",  # ALTER
    "SOLTAR",  # DROP
    "RENOMBRAR",  # RENAME
    # Manipulación de Datos
    "SELECCIONAR",  # SELECT
    "INSERTAR_EN",  # INSERT INTO
    "ELIMINAR",  # DELETE
    "REEMPLAZAR",  # REPLACE
    "VALORES",  # VALUES
    "ACTUALIZAR",  # UPDATE
    "MEZCLAR",  # MERGE
    "AGREGAR",  # ADD
    "MODIFICAR",  # MODIFY
    "CAMBIAR",  # CHANGE
    "RESTRICCION",  # CONSTRAINT
    # Consulta y Filtrado de Datos
    "DESDE",  # FROM
    "DONDE",  # WHERE
    "AGRUPAR_POR",  # GROUP BY
    "ORDENAR_POR",  # ORDER BY
    "TENIENDO",  # HAVING
    "TABLA",  # TABLE
    "LIMITAR",  # LIMIT
    "PRIMEROS",  # TOP
    # Control de Transacciones
    "CONFIRMAR",  # COMMIT
    "REVERTIR",  # ROLLBACK
    "PUNTO_GUARDADO",  # SAVEPOINT
    "INICIAR_TRANSACCION",  # BEGIN TRANSACTION
    "ESTABLECER_TRANSACCION",  # SET TRANSACTION
    # Operadores Logicos y de Comparación
    "Y",  # AND
    "O",  # OR
    "NO",  # NOT
    "MAYOR",  # >
    "MENOR",  # <
    "MAYOR_IGUAL",  # >=
    "MENOR_IGUAL",  # <=
    "IGUALDAD",  # '='
    "DIFERENTE",  #!=
    "ENTRE",  # BETWEEN
    "SIMILAR_A",  # LIKE
    "ES_NULO",  # IS NULL
    "NO_ES_NULO",  # IS NOT NULL
    "A",  # TO
    # Unión de Tablas
    "UNIR",  # JOIN
    "NORMAL",  # INNER
    "IZQUIERDO",  # LEFT JOIN
    "DERECHO",  # RIGHT JOIN
    "COMPLETO",  # FULL
    "CON",  # ON (para condiciones de JOIN)
    # Operadores aritmeticos
    "MAS",  # +
    "MENOS",  # -
    "MULTIPLICACION",  # *
    "DIVISION",  # /
    "MODULO",  # %
    # Palabras clave de subconsulta
    "EXISTE",  # EXISTS
    "TODOS",  # ALL
    "ALGUNO",  # ANY
    "ALGUNOS",  # SOME
    "CUALQUIERA",  # ANY
    "RANGO",  # RANGE
    # Palabras clave de funciones de agregación
    "CONTAR",  # COUNT
    "SUMA",  # SUM
    "PROMEDIO",  # AVG
    "MAXIMO",  # MAX
    "MINIMO",  # MIN
    # Tipos de datos
    "FECHA",  # DATE
    "BOOLEANO",  # BOOLEAN
    "DECIMAL",  # DECIMAL
    "NULO",  # NULL
    "ENTERO",  # INTEGER
    "TEXTO",  # TEXT
    "CARACTER",  # CHAR
    "NO_NULO",  # NOT NULL
    "CLAVE_PRIMARIA",  # PRIMARY KEY
    "CLAVE_FORANEA",  # FOREIGN KEY
    "REFERENCIA",  # REFERENCES
    "VALOR_CADENA",  # CADENA entre comillas simples
    "VALOR_FLOTANTE",  # FLOTANTE
    "VALOR_BOOLEANO",  # BOOLEANO
    # Identificadores / Claves
    "IDENTIFICADOR",  # IDENTIFICADOR
    "IDENTIFICADOR_INVALIDO",
    "CADENA",  # VARCHAR
    "VALOR_NUMERO",  # NÚMERO
    "FLOTANTE",  # FLOAT
    # Palabras clave de manejo de procedimientos almacenados
    "INICIO",  # BEGIN
    "FIN",  # END
    "SI",  # IF
    "SINO",  # ELSE
    "CASO",  # CASE
    "MIENTRAS",  # WHILE
    "PARA",  # FOR
    "ENTONCES",  # THEN
    # Caracteres especiales
    "COMA",  # ','
    "TODO",  # '*'
    "PUNTO",  # .
    "COMENTARIO",  # --
    "PARENTESIS_DER",  # (
    "PARENTESIS_IZQ",  # )
    "SALTO_DE_LINEA",  # \n
    "PYC",  # ;
    "COMILLAS_SIMPLES",  #'
    # Otros
    "CONVERTIR",  # CAST
    "ES",  # IS
    "ASCENDENTE",  # ASC
    "DESCENDENTE",  # DESC
    "COMO",  # AS
    "DISTINTO",  # DISTINCT
    "OBTENER",  # GET
    "COLOCAR",  # SET
    "AUTOINCREMENTAL",  # AUTO_INCREMENT
    "COLUMNA",  # COLUMN
]

# Definición de Datos
t_CREAR = r"CREAR"
t_ALTERAR = r"ALTERAR"
t_SOLTAR = r"SOLTAR"
t_RENOMBRAR = r"RENOMBRAR"

# Manipulación de Datos
t_SELECCIONAR = r"SELECCIONAR"
t_ELIMINAR = r"ELIMINAR"
t_REEMPLAZAR = r"REEMPLAZAR"
t_VALORES = r"VALORES"
t_ACTUALIZAR = r"ACTUALIZAR"
t_MEZCLAR = r"MEZCLAR"
t_AGREGAR = r"AGREGAR"
t_MODIFICAR = r"MODIFICAR"
t_CAMBIAR = r"CAMBIAR"

# Consulta y Filtrado de Datos
t_DESDE = r"DESDE"
t_DONDE = r"DONDE"
t_TENIENDO = r"TENIENDO"
t_TABLA = r"TABLA"
t_LIMITAR = r"LIMITAR"
t_PRIMEROS = r"PRIMEROS"

# Control de Transacciones
t_CONFIRMAR = r"CONFIRMAR"
t_REVERTIR = r"REVERTIR"

# Operadores Logicos y de Comparación
t_Y = r"Y"
t_O = r"O"
t_NO = r"NO"
t_MAYOR = r">"
t_MENOR = r"<"
t_MAYOR_IGUAL = r">="
t_MENOR_IGUAL = r"<="
t_IGUALDAD = r"\="
t_DIFERENTE = r"!="
t_ENTRE = r"ENTRE"
t_A = r"A"

# Unión de Tablas
t_UNIR = r"UNIR"
t_NORMAL = r"NORMAL"
t_IZQUIERDO = r"IZQUIERDO"
t_DERECHO = r"DERECHO"
t_COMPLETO = r"COMPLETO"
t_CON = r"CON"

# Operadores aritmeticos
t_MAS = r"\+"
t_MENOS = r"-"
t_MULTIPLICACION = r"\*"
t_DIVISION = r"/"
t_MODULO = r"%"

# Palabras clave de subconsulta
t_EXISTE = r"EXISTE"
t_TODOS = r"TODOS"
t_ALGUNO = r"ALGUNO"
t_ALGUNOS = r"ALGUNOS"
t_CUALQUIERA = r"CUALQUIERA"
t_RANGO = r"RANGO"
t_RESTRICCION = r"RESTRICCION"

# Palabras clave de funciones de agregación
t_CONTAR = r"CONTAR"
t_SUMA = r"SUMA"
t_PROMEDIO = r"PROMEDIO"
t_MAXIMO = r"MAXIMO"
t_MINIMO = r"MINIMO"

# Tipos de datos
t_FECHA = r"FECHA"
t_BOOLEANO = r"BOOLEANO"
t_DECIMAL = r"DECIMAL"
t_NULO = r"NULO"
t_ENTERO = r"ENTERO"
t_TEXTO = r"TEXTO"
t_CARACTER = r"CARACTER"
t_REFERENCIA = r"REFERENCIA"

# Identificadores / Claves
# t_CLAVE = r'CLAVE (PRIMARIA|FORANEA)'
# t_CLAVE_FORANEA = r'CLAVE FORANEA'

# Palabras clave de manejo de procedimientos almacenados
t_INICIO = r"INICIO"
t_FIN = r"FIN"
t_SI = r"SI"
t_SINO = r"SINO"
t_CASO = r"CASO"
t_MIENTRAS = r"MIENTRAS"
t_PARA = r"PARA"
t_ENTONCES = r"ENTONCES"

# Caracteres especiales
t_COMA = r","
t_PUNTO = r"\."
t_TODO = r"\*"
t_ignore = " \t"  # Ignorar espacios y tabs
t_PARENTESIS_DER = r"\)"
t_PARENTESIS_IZQ = r"\("
t_PYC = r"\;"
t_COMILLAS_SIMPLES = r"\'"

# Otros
t_CONVERTIR = r"CONVERTIR"
t_ES = r"ES"

t_ASCENDENTE = r"ASCENDENTE"
t_DESCENDENTE = r"DESCENDENTE"
t_COMO = r"COMO"
t_DISTINTO = r"DISTINTO"
t_OBTENER = r"OBTENER"
t_COLOCAR = r"COLOCAR"
t_AUTOINCREMENTAL = r"AUTOINCREMENTAL"
t_COLUMNA = r"COLUMNA"


def t_INSERTAR_EN(t):
    r"INSERTAR\s+EN"
    return t


# Consulta y Filtrado de Datos
def t_AGRUPAR_POR(t):
    r"AGRUPAR\s+POR"
    return t


def t_ORDENAR_POR(t):
    r"ORDENAR\s+POR"
    return t


def t_SIMILAR_A(t):
    r"SIMILAR\s+A"
    return t


# Control de Transacciones
def t_PUNTO_GUARDADO(t):
    r"PUNTO\s+GUARDADO"
    return t


def t_INICIAR_TRANSACCION(t):
    r"INICIAR\s+TRANSACCION"
    return t


def t_ESTABLECER_TRANSACCION(t):
    r"ESTABLECER\s+TRANSACCION"
    return t


# Control de Transacciones
def t_CLAVE_PRIMARIA(t):
    r"CLAVE\s+PRIMARIA"
    return t


def t_CLAVE_FORANEA(t):
    r"CLAVE\s+FORANEA"
    return t


# Operadores Logicos y de Comparación
def t_ES_NULO(t):
    r"ES\s+NULO"
    return t


def t_NO_ES_NULO(t):
    r"NO\s+ES\s+NULO"
    return t


# Unión de Tablas
def t_UNIR_INTERIOR(t):
    r"UNIR\s+INTERIOR"
    return t


def t_UNIR_IZQUIERDA(t):
    r"UNIR\s+IZQUIERDA"
    return t


def t_UNIR_DERECHA(t):
    r"UNIR\s+DERECHA"
    return t


# Tipos de datos
def t_NO_NULO(t):
    r"NO\s+NULO"
    return t


def t_IDENTIFICADOR(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    keywords = {
        # Definición de Datos
        "CREAR": "CREAR",
        "ALTERAR": "ALTERAR",
        "SOLTAR": "SOLTAR",
        "RENOMBRAR": "RENOMBRAR",
        # Manipulación de Datos
        "SELECCIONAR": "SELECCIONAR",
        "ELIMINAR": "ELIMINAR",
        "REEMPLAZAR": "REEMPLAZAR",
        "VALORES": "VALORES",
        "ACTUALIZAR": "ACTUALIZAR",
        "MEZCLAR": "MEZCLAR",
        "AGREGAR": "AGREGAR",
        "MODIFICAR": "MODIFICAR",
        "CAMBIAR": "CAMBIAR",
        "RESTRICCION": "RESTRICCION",
        # Consulta y Filtrado de Datos
        "DESDE": "DESDE",
        "DONDE": "DONDE",
        "TENIENDO": "TENIENDO",
        "TABLA": "TABLA",
        "LIMITAR": "LIMITAR",
        "PRIMEROS": "PRIMEROS",
        # Control de Transacciones
        "CONFIRMAR": "CONFIRMAR",
        "REVERTIR": "REVERTIR",
        # Operadores Lógicos y de Comparación
        "Y": "Y",
        "O": "O",
        "NO": "NO",
        "ENTRE": "ENTRE",
        "ES_NULO": "ES_NULO",
        "NO_ES_NULO": "NO_ES_NULO",
        "A": "A",
        # Unión de Tablas
        "UNIR": "UNIR",
        "NORMAL": "NORMAL",  # INNER JOIN
        "IZQUIERDO": "IZQUIERDO",  # LEFT JOIN
        "DERECHO": "DERECHO",  # RIGHT JOIN
        "COMPLETO": "COMPLETO",  # FULL JOIN
        "CON": "CON",  # ON (condición de JOIN)
        # Palabras clave de Subconsulta
        "EXISTE": "EXISTE",
        "TODOS": "TODOS",
        "ALGUNO": "ALGUNO",
        "ALGUNOS": "ALGUNOS",
        "CUALQUIERA": "CUALQUIERA",
        "RANGO": "RANGO",
        # Palabras clave de Funciones de Agregación
        "CONTAR": "CONTAR",
        "SUMA": "SUMA",
        "PROMEDIO": "PROMEDIO",
        "MAXIMO": "MAXIMO",
        "MINIMO": "MINIMO",
        # Tipos de Datos
        "FECHA": "FECHA",
        "BOOLEANO": "BOOLEANO",
        "DECIMAL": "DECIMAL",
        "NULO": "NULO",
        "ENTERO": "ENTERO",
        "TEXTO": "TEXTO",
        "CARACTER": "CARACTER",
        "NO_NULO": "NO_NULO",
        "CADENA": "CADENA",
        "FLOTANTE": "FLOTANTE",
        # Identificadores / Claves
        "CLAVE_PRIMARIA": "CLAVE_PRIMARIA",
        "CLAVE_FORANEA": "CLAVE_FORANEA",
        "REFERENCIA": "REFERENCIA",
        # Palabras clave de Manejo de Procedimientos Almacenados
        "INICIO": "INICIO",
        "FIN": "FIN",
        "SI": "SI",
        "SINO": "SINO",
        "CASO": "CASO",
        "MIENTRAS": "MIENTRAS",
        "PARA": "PARA",
        "ENTONCES": "ENTONCES",
        # Otros
        "CONVERTIR": "CONVERTIR",
        "ES": "ES",
        "ASCENDENTE": "ASCENDENTE",
        "DESCENDENTE": "DESCENDENTE",
        "COMO": "COMO",
        "DISTINTO": "DISTINTO",
        "OBTENER": "OBTENER",
        "COLOCAR": "COLOCAR",
        "AUTOINCREMENTAL": "AUTOINCREMENTAL",
        "COLUMNA": "COLUMNA",
    }
    t.type = keywords.get(t.value.upper(), "IDENTIFICADOR")
    return t


def t_VALOR_CADENA(t):
    r"(\"[^\"\\]*(?:\\.[^\"\\]*)*\"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')"
    return t


def t_VALOR_FLOTANTE(t):
    r"\d+\.\d+"
    return t


def t_VALOR_NUMERO(t):
    r"\d+"

    return t


def t_COMENTARIO(t):
    r"--.*"
    pass


def t_error(t):
    line = t.lineno
    column = t.lexpos - t.lexer.lexdata.rfind(
        "\n", 0, t.lexpos
    )  # Calcula la columna correctamente
    print(f"Error léxico: {t.value}")
    t.lexer.skip(1)
    raise Exception(f"Error léxico: {t.value} en la línea {line}, columna {column}.")


def t_SALTO_DE_LINEA(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_IDENTIFICADOR_INVALIDO(t):
    r"[^=a-zA-Z_\s\(-]+[a-zA-Z0-9_]*[a-zA-Z]+"
    print(f"Identificador inválido: {t.value}")
    t.lexer.skip(1)
    raise Exception(f"Identificador inválido: {t.value}")


lexer = lex.lex()


def analizar_lexico(query):
    lexer.input(query)
    lexer.lineno = 1
    tokens = []
    for token in lexer:
        tokens.append(token)
    return tokens
