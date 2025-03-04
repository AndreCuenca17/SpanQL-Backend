from datetime import datetime
from ..utils.AnalizadorSemantico import Instruccion

class Insertar(Instruccion):
    def __init__(self, nombre_tabla, columnas, valores):
        self.nombre_tabla = nombre_tabla
        self.columnas = columnas
        self.valores = valores

    def __str__(self):
        return f"Insertar({self.nombre_tabla}, {self.columnas}, {self.valores})"

    def analizar_semantica(self, base_datos):
        # Se verifica si la tabla existe
        if self.nombre_tabla not in base_datos:
            raise Exception(
                f"Error semántico: la tabla '{self.nombre_tabla}' no existe."
            )
        # Se verifica que las columnas existan en la tabla

        tabla = base_datos[self.nombre_tabla]

        # Se obtiene la clave primaria de la tabla
        clave_primaria = tabla.get("llave_primaria", None)
        # print("la clave primaria ", clave_primaria )

        for columna in self.columnas:
            if columna not in base_datos[self.nombre_tabla]["columnas"]:
                raise Exception(
                    f"Error semántico: la columna '{columna}' no existe en la tabla '{self.nombre_tabla}'."
                )
        # Se verifica que el número de columnas sea igual al número de valores
        """
        Cuando es mas de una fila a insertar, se complica, sel columnas es una listaza
        """
        # if len(self.columnas) != len(self.valores):
        # raise Exception(f"Error semántico: el número de columnas y valores no coincide en la tabla '{self.nombre_tabla}'.")
        # Se verifica que no se inserten valores en columnas autoincrementales
        for col in self.columnas:
            if (
                "AUTOINCREMENTAL"
                in base_datos[self.nombre_tabla]["columnas"][col]["restricciones"]
            ):
                raise Exception(
                    f"Error semántico: no se pueden insertar valores en columnas autoincrementales."
                )

        # Se validan los tipos de datos
        for valor, col in zip(self.valores, self.columnas):
            restricciones = base_datos[self.nombre_tabla]["columnas"][col].get(
                "restricciones", []
            )
            base_datos_tipo = base_datos[self.nombre_tabla]["columnas"][col][
                "tipo"
            ].upper()

            es_nulo = isinstance(valor, str) and valor.upper() == "NULO"

            # Si la columna es NO NULO y nos pasan "NULO", error
            if "NO NULO" in restricciones and es_nulo:
                raise Exception(
                    f"Error semántico: la columna '{col}' no puede ser nula."
                )

            # Si es "NULO" y la columna es clave primaria => error (las PK no aceptan nulos)
            if es_nulo and clave_primaria == col:
                raise Exception(
                    f"Error semántico: no se puede insertar NULO en la clave primaria '{col}'."
                )

            if not es_nulo:

                if base_datos_tipo == "ENTERO":
                    try:
                        valor_convertido = int(valor)
                    except:
                        raise Exception(
                            f"Error semántico: el valor '{valor}' no es un entero."
                        )
                elif base_datos_tipo == "FLOTANTE":
                    try:
                        valor_convertido = float(valor)
                    except:
                        raise Exception(
                            f"Error semántico: el valor '{valor}' no es un flotante."
                        )
                elif base_datos_tipo == "BOOLEANO":
                    if valor.upper() not in ["TRUE", "FALSE"]:
                        raise Exception(
                            f"Error semántico: el valor '{valor}' no es un booleano."
                        )
                    valor_convertido = valor.upper()  # Normalizamos a mayúsculas
                elif base_datos_tipo == "FECHA":
                    if (
                        isinstance(valor, str)
                        and valor.startswith('"')
                        and valor.endswith('"')
                    ):
                        valor = valor[1:-1]  # Eliminar comillas externas
                    try:
                        datetime.strptime(valor, "%Y-%m-%d")
                    except:
                        raise Exception(
                            f"Error semántico: el valor '{valor}' no es una fecha válida (YYYY-MM-DD)."
                        )
                    valor_convertido = valor
                else:
                    # Si el tipo no requiere conversión, se usa el valor tal cual
                    valor_convertido = valor

                # Validación de clave primaria: evitar duplicados
                if clave_primaria and col == clave_primaria:
                    # Se compara el valor convertido (asegúrate que en la base de datos se almacenan del mismo tipo)
                    if valor_convertido in tabla["columnas"][col]["datos"]:
                        raise Exception(
                            f"Error semántico: El valor '{valor}' ya existe como clave primaria en '{col}'."
                        )

                # Validación de clave foránea:
                # Se asume que la columna es clave foránea si aparece en el diccionario "llaves_foraneas"
                if col in tabla.get("llaves_foraneas", {}):
                    # Obtener la referencia: formato "tabla_ref.columna_ref"
                    ref = tabla["llaves_foraneas"][col]
                    tabla_ref, col_ref = ref.split(".")
                    # Verificar que el valor convertido exista en la columna referenciada de la tabla foránea
                    if (
                        valor_convertido
                        not in base_datos[tabla_ref]["columnas"][col_ref]["datos"]
                    ):
                        raise Exception(
                            f"Error semántico: El valor '{valor_convertido}' en la columna '{col}' "
                            f"no existe en '{tabla_ref}.{col_ref}' (clave foránea)."
                        )
        # Se valida el no nulo en las columnas correspondientes
        # Se valida la no repetición de llaves primarias
        # Se valida la inserción de llaves foráneas

    def ejecutar(self, base_datos):
        print(type(self.valores))
        self.analizar_semantica(base_datos)
        sql = f"INSERT INTO {self.nombre_tabla} ({', '.join(self.columnas)}) VALUES ({', '.join(self.valores)})"
        return sql
