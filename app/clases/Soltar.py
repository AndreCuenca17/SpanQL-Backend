from ..utils.AnalizadorSemantico import Instruccion

class Soltar(Instruccion):
    def __init__(self,tabla):
        self.tabla = tabla
    def analizar_semantica(self, base_datos):
        for t in self.tabla:
            if t not in base_datos:
                raise Exception(f"Error: La tabla '{t}' no existe.")
        
    def ejecutar(self, base_datos):
        self.analizar_semantica(base_datos)
        tablas_sql = ", ".join(self.tabla)
        sql = f"DROP TABLE {tablas_sql}"
        return sql
        
class soltar_condicional(Instruccion):
    def __init__(self, tabla):
        self.tabla = tabla
    def analizar_semantica(self, base_datos):
        for t in self.tabla:
            if t not in base_datos:
                raise Exception(f"Error: La tabla '{t}' no existe.")
        
    def ejecutar(self, base_datos):
        self.analizar_semantica(base_datos)
        tablas_sql = ", ".join(self.tabla)
        sql = f"DROP TABLE IF EXISTS {tablas_sql}"
        return sql