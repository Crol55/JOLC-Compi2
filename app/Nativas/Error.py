from datetime import datetime

class Error(): 
    def __init__(self,descripcion, linea,columna) -> None:
        self.descripcion = descripcion 
        self.linea = linea 
        self.columna = columna 
        self.time = self.cast_time_to_string( datetime.now())

    def cast_time_to_string (self, fechaYhora):
        dt_string = fechaYhora.strftime("%d/%m/%Y %H:%M:%S")
        return dt_string


