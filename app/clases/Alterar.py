from ..utils.AnalizadorSemantico import Instruccion


class Columna:
    def __init__(self, nombre, tipo_dato, restricciones):
        self.nombre = nombre
        self.tipo_dato = tipo_dato
        self.restricciones = restricciones


class AlterarTabla(Instruccion):
    def __init__(self, nombre_tabla, alteraciones):
        self.nombre_tabla = nombre_tabla
        self.alteraciones = alteraciones

    def __repr__(self):
        return f"AlterarTabla(tabla='{self.nombre_tabla}', alteraciones={self.alteraciones})"

    def analizar_semantica(self, base_datos):
        # Verificar que la tabla exista en base_datos
        if self.nombre_tabla not in base_datos:
            raise Exception(f"La tabla '{self.nombre_tabla}' no existe.")

        # Validar cada alteración
        for alteracion in self.alteraciones:
            alteracion.analizar_semantica(base_datos, self.nombre_tabla)
            print(type(alteracion))

    def ejecutar(self, base_datos):

        # Traducir a MySQL
        sql_statements = f""
        for alteracion in self.alteraciones:
            sql_statements += f" {alteracion.ejecutar(base_datos, self.nombre_tabla)}"
        return sql_statements


class AgregarColumna(Instruccion):
    def __init__(self, lista_columnas):
        self.lista_columnas = lista_columnas

    def __repr__(self):
        return f"AgregarColumna(columnas={self.lista_columnas})"

    def analizar_semantica(self, base_datos, nombre_tabla):
        # Validar si la tabla tiene la columna
        if nombre_tabla not in base_datos:
            raise Exception(f"La tabla '{nombre_tabla}' no existe.")

        diccionario = {
            "TEXTO": "text(255)",
            "ENTERO": "int",
            "CADENA": "varchar(255)",
            "DECIMAL": "decimal(10,2)",
            "BOOLEANO": "boolean",
        }

        for col_def in self.lista_columnas:
            nombre_columna = col_def.nombre
            if nombre_columna in base_datos[nombre_tabla]["columnas"]:
                raise Exception(
                    f"La columna '{nombre_columna}' ya existe en la tabla '{nombre_tabla}'."
                )
            if col_def.tipo_dato not in [
                "ENTERO",
                "TEXTO",
                "FECHA",
                "DECIMAL",
                "BOOLEANO",
                "CADENA",
            ]:
                raise Exception(
                    f"El tipo de dato '{col_def.tipo_dato}' no es válido para la columna '{nombre_columna}'."
                )
            if not all(
                restriccion
                in [
                    "NO NULO",
                    "UNICO",
                    "CLAVE PRIMARIA",
                    "CLAVE FORANEA",
                    "AUTOINCREMENTAl",
                ]
                for restriccion in col_def.restricciones
            ):
                raise Exception(
                    f"Las restricciones para '{nombre_columna}' no son válidas."
                )
            col_def.tipo_dato = diccionario.get(col_def.tipo_dato)

    def ejecutar(self, base_datos, nombre_tabla):
        # Generar la sentencia MySQL para agregar columnas
        self.analizar_semantica(base_datos, nombre_tabla)
        sql_statements = f""
        for col_def in self.lista_columnas:
            sql = f"ALTER TABLE {nombre_tabla} ADD COLUMN {col_def.nombre} {col_def.tipo_dato}"
            if "NO NULO" in col_def.restricciones:
                sql += " NOT NULL"
            if "UNICO" in col_def.restricciones:
                sql += " UNIQUE"
            if "CLAVE PRIMARIA" in col_def.restricciones:
                sql += " PRIMARY KEY"
            if "CLAVE FORANEA" in col_def.restricciones:
                # Aquí agregarías la lógica para claves foráneas si es necesario
                pass
            sql_statements += f"{sql}"
        return sql_statements


class SoltarColumna(Instruccion):
    def __init__(self, nombre_columna):
        self.nombre_columna = nombre_columna

    def __repr__(self):
        return f"SoltarColumna(columna='{self.nombre_columna}')"

    def analizar_semantica(self, base_datos, nombre_tabla):
        if nombre_tabla not in base_datos:
            raise Exception(f"La tabla '{nombre_tabla}' no existe.")
        if self.nombre_columna not in base_datos[nombre_tabla]["columnas"]:
            raise Exception(
                f"La columna '{self.nombre_columna}' no existe en la tabla '{nombre_tabla}'."
            )

    def ejecutar(self, base_datos, nombre_tabla):
        # Generar la sentencia MySQL para soltar columna
        self.analizar_semantica(base_datos, nombre_tabla)
        return f"ALTER TABLE {nombre_tabla} DROP COLUMN {self.nombre_columna}"


class ModificarColumna(Instruccion):
    def __init__(self, lista_columnas):
        self.lista_columnas = lista_columnas

    def __repr__(self):
        return f"ModificarColumna(columnas={self.lista_columnas})"

    def analizar_semantica(self, base_datos, nombre_tabla):
        diccionario = {
            "TEXTO": "text(255)",
            "ENTERO": "int",
            "CADENA": "varchar(255)",
            "DECIMAL": "decimal(10,2)",
            "BOOLEANO": "boolean",
        }
        if nombre_tabla not in base_datos:
            raise Exception(f"La tabla '{nombre_tabla}' no existe.")
        for col_def in self.lista_columnas:
            if col_def.nombre not in base_datos[nombre_tabla]["columnas"]:
                raise Exception(
                    f"La columna '{col_def.nombre}' no existe en la tabla '{nombre_tabla}'."
                )
            if col_def.tipo_dato not in [
                "ENTERO",
                "TEXTO",
                "FECHA",
                "DECIMAL",
                "BOOLEANO",
                "CADENA",
            ]:
                raise Exception(f"El tipo de dato '{col_def.tipo_dato}' no es válido.")
            if not all(
                restriccion in ["NO NULO", "UNICO", "CLAVE PRIMARIA", "CLAVE FORANEA"]
                for restriccion in col_def.restricciones
            ):
                raise Exception(
                    f"Las restricciones para la columna '{col_def.nombre}' no son válidas."
                )
            col_def.tipo_dato = diccionario.get(col_def.tipo_dato)

    def ejecutar(self, base_datos, nombre_tabla):
        self.analizar_semantica(base_datos, nombre_tabla)
        sql_statements = f""
        for col_def in self.lista_columnas:
            sql = f"ALTER TABLE {nombre_tabla} MODIFY COLUMN {col_def.nombre} {col_def.tipo_dato}"
            if "NO NULO" in col_def.restricciones:
                sql += " NOT NULL"
            if "UNICO" in col_def.restricciones:
                sql += " UNIQUE"
            if "CLAVE PRIMARIA" in col_def.restricciones:
                sql += " PRIMARY KEY"
            if "CLAVE FORANEA" in col_def.restricciones:
                # Aquí agregarías la lógica para claves foráneas si es necesario
                pass
            sql_statements += sql
        return sql_statements


class RenombrarColumna(Instruccion):
    def __init__(self, nombre_viejo, nombre_nuevo):
        self.nombre_viejo = nombre_viejo
        self.nombre_nuevo = nombre_nuevo

    def __repr__(self):
        return f"RenombrarColumna(viejo='{self.nombre_viejo}', nuevo='{self.nombre_nuevo}')"

    def analizar_semantica(self, base_datos, nombre_tabla):
        if nombre_tabla not in base_datos:
            raise Exception(f"La tabla '{nombre_tabla}' no existe.")
        if self.nombre_viejo not in base_datos[nombre_tabla]["columnas"]:
            raise Exception(
                f"La columna '{self.nombre_viejo}' no existe en la tabla '{nombre_tabla}'."
            )
        if self.nombre_nuevo in base_datos[nombre_tabla]["columnas"]:
            raise Exception(
                f"La columna '{self.nombre_nuevo}' ya existe en la tabla '{nombre_tabla}'."
            )

    def ejecutar(self, base_datos, nombre_tabla):
        self.analizar_semantica(base_datos, nombre_tabla)
        return f"ALTER TABLE {nombre_tabla} RENAME COLUMN {self.nombre_viejo} TO {self.nombre_nuevo}"


class CambiarColumna(Instruccion):
    def __init__(self, nombre_viejo, nueva_definicion):
        self.nombre_viejo = nombre_viejo
        if isinstance(nueva_definicion, list) and len(nueva_definicion) > 0:
            # Extraer la primera tupla de la lista
            columna_info = nueva_definicion[0]
            self.nueva_definicion = {
                "nombre": columna_info[0],
                "tipo_dato": columna_info[1],
                "restricciones": columna_info[2],
            }
        else:
            # Caso de error, inicializar con valores por defecto
            self.nueva_definicion = {"nombre": "", "tipo_dato": "", "restricciones": []}

    def __repr__(self):
        return f"CambiarColumna(viejo='{self.nombre_viejo}', nueva_def='{self.nueva_definicion}')"

    def analizar_semantica(self, base_datos, nombre_tabla):
        diccionario = {
            "TEXTO": "text(255)",
            "ENTERO": "int",
            "CADENA": "varchar(255)",
            "DECIMAL": "decimal(10,2)",
            "BOOLEANO": "boolean",
        }
        if nombre_tabla not in base_datos:
            raise Exception(f"La tabla '{nombre_tabla}' no existe.")
        if self.nombre_viejo not in base_datos[nombre_tabla]["columnas"]:
            raise Exception(
                f"La columna '{self.nombre_viejo}' no existe en la tabla '{nombre_tabla}'."
            )
        if self.nueva_definicion["nombre"] in base_datos[nombre_tabla]["columnas"]:
            raise Exception(
                f"La columna '{self.nueva_definicion['nombre']}' ya existe en la tabla '{nombre_tabla}'."
            )
        if self.nueva_definicion["tipo_dato"] not in [
            "ENTERO",
            "TEXTO",
            "FECHA",
            "DECIMAL",
            "BOOLEANO",
        ]:
            raise Exception(
                f"El tipo de dato '{self.nueva_definicion['tipo_dato']}' no es válido."
            )
        if not all(
            restriccion in ["NO NULO", "UNICO", "CLAVE PRIMARIA", "CLAVE FORANEA"]
            for restriccion in self.nueva_definicion["restricciones"]
        ):
            raise Exception(f"Las restricciones para la nueva columna no son válidas.")
        self.nueva_definicion["tipo_dato"] = diccionario.get(
            self.nueva_definicion["tipo_dato"]
        )

    def ejecutar(self, base_datos, nombre_tabla):
        self.analizar_semantica(base_datos, nombre_tabla)
        sql = f"ALTER TABLE {nombre_tabla} CHANGE COLUMN {self.nombre_viejo} {self.nueva_definicion['nombre']} {self.nueva_definicion['tipo_dato']}"

        if "NO NULO" in self.nueva_definicion["restricciones"]:
            sql += " NOT NULL"
        if "UNICO" in self.nueva_definicion["restricciones"]:
            sql += " UNIQUE"
        if "CLAVE PRIMARIA" in self.nueva_definicion["restricciones"]:
            sql += " PRIMARY KEY"
        if "CLAVE FORANEA" in self.nueva_definicion["restricciones"]:
            # Aquí agregarías la lógica para claves foráneas si es necesario
            pass
        return sql
