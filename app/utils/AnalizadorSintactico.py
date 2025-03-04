import ply.yacc as yacc
from .AnalizadorLexico import tokens  # Importar los tokens de tu analizador léxico

from ..reglas import ReglasComunes, Select, Insert, Create, Alter, Update, Delete, DropTable, Transaction, Join

modulos = [ReglasComunes, Select, Insert, Create, Alter, Update, Delete, DropTable, Transaction, Join]

for mod in modulos:
    for nombre in dir(mod):
        if nombre.startswith("p_"):  # Si la función comienza con "p_", es una regla
            globals()[nombre] = getattr(mod, nombre)

# Definir la precedencia de los operadores
precedence = (
    ("left", "Y", "O"),  # Operadores lógicos
    (
        "left",
        "MENOR",
        "MAYOR",
        "MENOR_IGUAL",
        "MAYOR_IGUAL",
        "IGUALDAD",
        "DIFERENTE",
    ),  # Comparadores
    ("left", "MAS", "MENOS"),  # Operadores aritméticos
    ("left", "MULTIPLICACION", "DIVISION", "MODULO"),  # Operadores aritméticos
)

# Definición de la gramática del analizador sintáctico
def p_instruccion(t):
    """instruccion : seleccion
    | insertar
    | alterar
    | actualizar
    | eliminar
    | soltar
    | crear
    | transaccion
    | unir
    | valor"""
    t[0] = t[1]

# Manejo de errores sintácticos
def p_error(t):
    if t:
        print(f"Error de sintaxis en '{t.value}'")
        raise Exception(f"Error de sintaxis en '{t.value}'")
    else:
        print("Error de sintaxis en la entrada")
        raise Exception("Error de sintaxis en la entrada")


# Construcción del analizador
parser = yacc.yacc(start='instruccion')

# Función para analizar una consulta SQL en español
def analizar_sintaxis(consulta):
    return parser.parse(consulta)

# resultado = analizar_sintaxis(
#     """SELECCIONAR nombre DESDE empleados DONDE salario > 5000"""
# )

# print("Resultado de la consulta:")
# print(resultado)


