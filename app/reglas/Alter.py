from ..clases.Alterar import *
# Regla principal para ALTER TABLE
# ALTER TABLE nombreTabla ***************
def p_alterar(t):
    """alterar : ALTERAR TABLA IDENTIFICADOR alteraciones"""
    # t[3]: nombre de la tabla
    # t[4]: lista de alteraciones (cada una representa una modificación)
    # t[0] = ("alter_table", t[3], t[4])
    t[0] = AlterarTabla(nombre_tabla=t[3], alteraciones=t[4])

# Permitir una o más alteraciones separadas por coma
def p_alteraciones_single(t):
    """alteraciones : alteracion"""
    t[0] = [t[1]]


def p_alteraciones_multiple(t):
    """alteraciones : alteracion COMA alteraciones"""
    t[0] = [t[1]] + t[3]


# 1. Agregar una nueva columna (se puede permitir la palabra opcional COLUMN)
# ALTER TABLE ADD COLUMN 'nombreColumna' 'tipoDato' 'reestriccion'
def p_alteracion_add(t):
    """alteracion : AGREGAR opt_column lista_columna_crear"""
    #t[0] = ("add_column", t[3])
    columnas = [Columna(nombre=col[0], tipo_dato=col[1], restricciones=col[2]) for col in t[3]]
    t[0] = AgregarColumna(lista_columnas=columnas)

# Regla para la opción COLUMN (puede estar o no)
def p_opt_column(t):
    """opt_column : COLUMNA
                  | empty"""
    t[0] = f"{t[1]}" if f"{t[1]}" is not None else None


# 2. Eliminar una columna (con o sin la palabra COLUMN):
# ALTER TABLE DROP COLUMN 'nombreColumna'
def p_alteracion_drop(t):
    """alteracion : SOLTAR opt_column IDENTIFICADOR"""
    # t[0] = ("drop_column", t[3])
    t[0] = SoltarColumna(nombre_columna= t[3])

# 3. Modificar la definición de una columna:
# ALTER TABLE MODIFY COLUMN 'nombreColumna' 'tipoDato' 'restriccion'
def p_alteracion_modificar(t):
    """alteracion : MODIFICAR opt_column lista_columna_crear"""
    # t[3] es el nombre de la columna, t[4] la nueva definición (por ejemplo, nuevo tipo)
    # t[0] = ("modify_column", t[3])
    columnas = [Columna(nombre=col[0], tipo_dato=col[1], restricciones=col[2]) for col in t[3]]
    t[0] = ModificarColumna(lista_columnas= columnas)

# 4. Renombrar una columna:
#    ALTER TABLE [table_name] RENAME COLUMN [OldName] TO [NewName];
def p_alteracion_rename(t):
    """alteracion : RENOMBRAR opt_column IDENTIFICADOR A IDENTIFICADOR"""
    # t[0] = ("rename_column", t[3], t[5])
    t[0] = RenombrarColumna(nombre_viejo= t[3], nombre_nuevo= t[5])

# 5. Cambiar una columna:
#    ALTER TABLE [table_name] CHANGE [old_column_name] [new_column_name] [column definition]
def p_alteracion_change(t):
    """alteracion : CAMBIAR opt_column IDENTIFICADOR lista_columna_crear"""
    # t[0] = ("change_column", t[3], t[4])
    t[0] = CambiarColumna(nombre_viejo= t[3], nueva_definicion= t[4])
