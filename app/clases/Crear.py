from ..utils.AnalizadorSemantico import Instruccion

class Crear(Instruccion):
    def __init__(self, nombre_tabla, columnas, llave_primaria=None, llaves_foraneas=None):
        self.nombre_tabla = nombre_tabla
        self.columnas = columnas  
        self.llave_primaria = llave_primaria
        self.llaves_foraneas = llaves_foraneas if llaves_foraneas else {}
        
    def __str__(self):
        return f"Crear({self.nombre_tabla}, {self.columnas}, CPrincipal={self.llave_primaria}, CForanea={self.llaves_foraneas})"
                
    def analizar_semantica(self, base_datos):
     # Se convierte la lista en un diccionario temporal para validar duplicados
     columnas_dict = {}
    
     for nombre_columna, tipo_dato, restricciones in self.columnas:
        if nombre_columna in columnas_dict:
            raise Exception(f"Error semántico: la columna '{nombre_columna}' está duplicada en la tabla '{self.nombre_tabla}'.")
        
        columnas_dict[nombre_columna] = {
            "tipo": tipo_dato,
            "restricciones": restricciones
        }

     # Se verifica si la tabla ya existe
     if self.nombre_tabla in base_datos:
        raise Exception(f"Error semántico: la tabla '{self.nombre_tabla}' ya existe.")
    
     # Se verifica que se estén definiendo columnas
     if not columnas_dict:
        raise Exception(f"Error semántico: la tabla '{self.nombre_tabla}' debe tener al menos una columna.")
    
     # self.columnas como un diccionario generado desde la lista 
     self.columnas = columnas_dict  

     # Se verifica que solo exista una llave primaria
     if sum(1 for col in self.columnas if "CLAVE PRIMARIA" in self.columnas[col]["restricciones"]) > 1:
        raise Exception(f"Error semántico: la tabla '{self.nombre_tabla}' tiene más de una llave primaria.")
    
     # Se verifica que la llave primaria (si hay) exista en las columnas
     if self.llave_primaria and self.llave_primaria not in self.columnas:
        raise Exception(f"Error semántico: la llave primaria '{self.llave_primaria}' no está en las columnas de la tabla '{self.nombre_tabla}'.")
    
     # Se valida que si un dato es una llave foránea, no puede ser autoincremental
     for col, ref in self.llaves_foraneas.items():
        if "AUTOINCREMENTAL" in self.columnas[col]["restricciones"]:
            raise Exception(f"Error semántico: la columna '{col}' no puede ser autoincremental y llave foránea al mismo tiempo.")
    
     # Se validan las llaves foráneas
     for col, ref in self.llaves_foraneas.items():
        if col not in self.columnas:
            raise Exception(f"Error semántico: la columna '{col}' definida como llave foránea no existe en la tabla {self.nombre_tabla}.")
        
        ref_tabla, ref_columna = ref.split(".")
        
        if ref_tabla not in base_datos:
            raise Exception(f"Error semántico: la tabla referenciada '{ref_tabla}' no existe.")
        
        if ref_columna not in base_datos[ref_tabla]["columnas"]:
            raise Exception(f"Error semántico: la columna referenciada '{ref_columna}' no existe en la tabla '{ref_tabla}'.")
        
        # Se valida que la llave foránea apunte a una llave primaria en la tabla referenciada
        if "CLAVE PRIMARIA" not in base_datos[ref_tabla]["columnas"][ref_columna]["restricciones"]:
            raise Exception(f"Error semántico: la columna referenciada '{ref_columna}' en la tabla '{ref_tabla}' no es llave primaria.")
        
    def ejecutar(self, base_datos):
     # Se ejecuta el análisis semántico
     self.analizar_semantica(base_datos)

     # Se construye la consulta SQL en formato de texto
     columnas_sql = []

     for nombre_col, atributos in self.columnas.items():
        if atributos["tipo"] == "ENTERO":
            tipo_dato = "INT"
        elif atributos["tipo"] == "TEXTO":
            tipo_dato = "TEXT"
        elif atributos["tipo"] == "CADENA":
            tipo_dato = "VARCHAR(255)"
        elif atributos["tipo"] == "FECHA":
            tipo_dato = "DATE"
        elif atributos["tipo"] == "DECIMAL":
            tipo_dato = "DECIMAL"
        elif atributos["tipo"] == "BOOLEANO":
            tipo_dato = "BOOLEAN"
        elif atributos["tipo"] == "CARACTER":
            tipo_dato = "CHAR"
        elif atributos["tipo"] == "FLOTANTE":
            tipo_dato = "FLOAT"
        else:
            raise Exception(f"Error semántico: tipo de dato '{atributos['tipo']}' no válido.")
        
        restricciones = []
        
        for restriccion in atributos["restricciones"]:
         if "AUTOINCREMENTAL" == restriccion:
            restricciones.append("AUTO_INCREMENT")
         elif "NO NULO" == restriccion:
            restricciones.append("NOT NULL")
         elif "CLAVE PRIMARIA" == restriccion:
             pass
         elif "CLAVE FORANEA" == restriccion:
            restricciones.append("FOREIGN KEY")

        restriccion_sql = " ".join(restricciones) if restricciones else ""
        columnas_sql.append(f"{nombre_col} {tipo_dato} {restriccion_sql}".strip())

     if self.llave_primaria:
        columnas_sql.append(f"PRIMARY KEY ({self.llave_primaria})")

     for col, ref in self.llaves_foraneas.items():
        ref_tabla, ref_columna = ref.split(".")
        columnas_sql.append(f"FOREIGN KEY ({col}) REFERENCES {ref_tabla}({ref_columna})")

     sql = f"CREATE TABLE {self.nombre_tabla} (\n    " + ",\n    ".join(columnas_sql) + "\n);"
     return sql
    
    