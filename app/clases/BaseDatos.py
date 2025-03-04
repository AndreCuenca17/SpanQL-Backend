class BaseDatos:
    def __init__(self):
        # Ejemplo de cómo podrían almacenarse las tablas y las columnas dentro de ellas.
        self.tablas = {
            "clientes": {
                "columnas": {
                    "id_cliente": {"tipo": "entero", "restricciones": ["no_nulo", "clave_primaria"]},
                    "nombre": {"tipo": "texto", "restricciones": ["no_nulo"]},
                    "email": {"tipo": "texto", "restricciones": ["no_nulo", "unico"]}
                }
            },
            "productos": {
                "columnas": {
                    "id_producto": {"tipo": "entero", "restricciones": ["no_nulo", "clave_primaria"]},
                    "descripcion": {"tipo": "texto", "restricciones": ["no_nulo"]}
                }
            }
        }

    def existe_tabla(self, nombre_tabla):
        """
        Verifica si la tabla existe en la base de datos.
        """
        return nombre_tabla in self.tablas

    def tabla_tiene_columna(self, nombre_tabla, nombre_columna):
        """
        Verifica si una tabla tiene una columna específica.
        """
        if not self.existe_tabla(nombre_tabla):
            raise Exception(f"La tabla '{nombre_tabla}' no existe.")
        return nombre_columna in self.tablas[nombre_tabla]["columnas"]

    def tipo_dato_valido(self, tipo_dato):
        """
        Verifica si el tipo de dato es válido.
        """
        tipos_validos = ["entero", "texto", "fecha", "decimal", "booleano"]  # Ejemplo de tipos válidos
        return tipo_dato in tipos_validos

    def restricciones_validas(self, restricciones):
        """
        Verifica si las restricciones de una columna son válidas.
        """
        restricciones_validas = ["no_nulo", "unico", "clave_primaria", "clave_foranea", "predeterminado"]
        # Verifica que todas las restricciones sean válidas
        return all(restriccion in restricciones_validas for restriccion in restricciones)

    def columna_tiene_restricciones(self, nombre_tabla, nombre_columna):
        """
        Verifica si una columna en una tabla tiene restricciones.
        """
        if not self.tabla_tiene_columna(nombre_tabla, nombre_columna):
            raise Exception(f"La columna '{nombre_columna}' no existe en la tabla '{nombre_tabla}'.")
        restricciones = self.tablas[nombre_tabla]["columnas"][nombre_columna]["restricciones"]
        return len(restricciones) > 0
