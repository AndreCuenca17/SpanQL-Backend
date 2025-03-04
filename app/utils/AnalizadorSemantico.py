class Instruccion:
    def __init__(self):
        pass
    def analizar_semantica(self, base_datos):
        raise NotImplementedError()
    
    def ejecutar(self, base_datos):
        raise NotImplementedError()



