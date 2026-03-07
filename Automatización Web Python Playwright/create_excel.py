import openpyxl

# Crear un archivo Excel de ejemplo para datos de prueba de SOAT
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = 'SOAT'

# Headers
sheet['A1'] = 'placa'
sheet['B1'] = 'tipo_vehiculo'
sheet['C1'] = 'expected_result'

# Datos de ejemplo
sheet['A2'] = 'ABC-123'
sheet['B2'] = 'auto'
sheet['C2'] = 'Cotización exitosa'

sheet['A3'] = 'XYZ-456'
sheet['B3'] = 'camioneta'
sheet['C3'] = 'Cotización exitosa'

# Guardar el archivo
workbook.save('data/test_data.xlsx')
print("Archivo test_data.xlsx creado en data/")