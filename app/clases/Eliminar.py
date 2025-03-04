from ..utils.AnalizadorSemantico import Instruccion

class Eliminar(Instruccion):
    def __init__(self, tabla, clausula= None, limite = None):
        self.tabla = tabla
        self.clausula = clausula
        self.limite = limite
    
    def analizar_semantica(self, base_datos):
        if self.tabla not in base_datos:
            raise Exception(f"Error: La tabla '{self.tabla}' no existe.")

            
    def ejecutar(self, base_datos):
        """Genera la consulta SQL en formato de texto."""
        # Llamamos la validación aquí
        self.analizar_semantica(base_datos) 
         
        sql = f"DELETE FROM {self.tabla}"
        if self.clausula:
            sql += f" WHERE {self.clausula}"
        if self.limite:
            sql += f" LIMIT {self.limite}"
        return sql 