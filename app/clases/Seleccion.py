from ..utils.AnalizadorSemantico import Instruccion


class Seleccion(Instruccion):
    def __init__(self, columnas, tabla, condiciones=None, unir=None):
        self.columnas = columnas  # Lista de columnas a seleccionar
        self.tabla = tabla  # Nombre de la tabla
        self.condiciones = condiciones  # Condiciones opcionales
        self.unir = unir  # datos del join

    def analizar_semantica(self, base_datos):
        """Verifica que la tabla y las columnas existan en la base de datos."""
        # Verificar la existencia de la tabla principal
        if self.tabla not in base_datos:
            raise Exception(f"Error: La tabla '{self.tabla}' no existe.")

        # Verificar las columnas en la tabla principal
        columnas_disponibles = list(base_datos[self.tabla]["columnas"].keys())

        if self.columnas == ["TODO"]:
            self.columnas = ["*"]

        for columna in self.columnas:
            if self.columnas != ["*"] and columna not in columnas_disponibles:
                raise Exception(
                    f"Error: La columna '{self.columnas}' no existe en '{self.tabla}'."
                )

        # Si hay JOIN, verificamos la tabla unida y su condición
        if self.unir:
            _, tipo, tabla_unida, condicion = self.unir

            # Verificar si la tabla del JOIN existe
            if tabla_unida not in base_datos:
                raise Exception(
                    f"Error: La tabla '{tabla_unida}' no existe para el JOIN."
                )

            # Regla semántica: No permitir JOIN con la misma tabla del SELECT
            if self.tabla == tabla_unida:
                raise Exception(
                    f"Error: No puedes hacer un JOIN con la misma tabla '{self.tabla}'."
                )

            # Verificar que las columnas de la condición existen
            (col1, _, tabla1), operador, (col2, _, tabla2) = condicion

            if set([tabla1, tabla2]) != set([self.tabla, tabla_unida]):
                raise Exception(
                    f"Error: La condición del JOIN debe involucrar solo '{self.tabla}' y '{tabla_unida}', pero usa '{tabla1}' y '{tabla2}'."
                )

            if col1 not in base_datos.get(tabla1, {}).get("columnas", {}):
                raise Exception(
                    f"Error: La columna '{col1}' no existe en la tabla '{tabla1}'."
                )
            if col2 not in base_datos.get(tabla2, {}).get("columnas", {}):
                raise Exception(
                    f"Error: La columna '{col2}' no existe en la tabla '{tabla2}'."
                )

    def ejecutar(self, base_datos):
        """Genera la consulta SQL en formato de texto."""
        self.analizar_semantica(base_datos)
        sql = f""
        # Construcción de la parte inicial del SELECT
        if self.columnas == ["*"]:
            sql += f"SELECT * FROM {self.tabla}"
        else:
            sql += f"SELECT {', '.join(self.columnas)} FROM {self.tabla}"

        # Procesar JOIN si existe
        if self.unir:
            print("Debug JOIN:", self.unir)  # Verificar la estructura real de self.unir

            # Desempaquetar la estructura de self.unir directamente
            _, tipo_join, tabla_join, condicion_join = self.unir
            (col1, _, tabla1), operador, (col2, _, tabla2) = condicion_join

            # Construcción de la condición del JOIN
            condicion_sql = f"{tabla1}.{col1} {operador} {tabla2}.{col2}"
            diccionario = {
                "NORMAL": "INNER",
                "IZQUIERDO": "LEFT",
                "DERECHO": "RIGHT",
                "COMPLETO": "TOTAL",
            }
            tipo_join = diccionario.get(tipo_join)
            sql += f" {tipo_join} JOIN {tabla_join} ON {condicion_sql}"

        # Agregar WHERE si hay condiciones
        if self.condiciones:
            sql += f" WHERE {self.condiciones}"

        return sql
