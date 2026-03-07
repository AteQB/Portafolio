import openpyxl
import os

class DataReader:
    """
    Clase para leer datos de prueba desde un archivo Excel.
    Objetivo: Proporcionar una forma reutilizable de cargar datos de prueba para las cotizaciones de SOAT.
    """

    def __init__(self, file_path: str):
        """
        Inicializa el lector de datos.
        :param file_path: Ruta al archivo Excel.
        """
        self.file_path = file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no existe.")

    def read_soat_data(self) -> list:
        """
        Lee los datos de cotización de SOAT desde la hoja 'SOAT'.
        Objetivo: Extraer filas de datos para parametrizar pruebas.
        Cada fila debe tener columnas: placa (string, ej. "ABC-123"), tipo_vehiculo (string, "auto" o "moto"), expected_result (string opcional).
        :return: Lista de diccionarios con los datos.
        """
        workbook = openpyxl.load_workbook(self.file_path)
        sheet = workbook['SOAT']  # Asume hoja llamada 'SOAT'
        data = []
        headers = [cell.value for cell in sheet[1]]  # Primera fila como headers
        for row in sheet.iter_rows(min_row=2, values_only=True):
            data.append(dict(zip(headers, row)))
        return data