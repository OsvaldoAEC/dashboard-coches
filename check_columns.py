import pandas as pd

# Cargar datos
df = pd.read_csv('vehicles_us.csv')

print("=" * 50)
print("COLUMNAS DISPONIBLES EN TU DATASET:")
print("=" * 50)

# Mostrar todas las columnas
for col in df.columns:
    print(f"- {col}")

print("\n" + "=" * 50)
print("VERIFICACIÓN DE COLUMNAS NECESARIAS:")
print("=" * 50)

# Columnas que necesitamos
columnas_necesarias = ['manufacturer', 'type', 'model_year', 'condition', 'price']

for col in columnas_necesarias:
    existe = col in df.columns
    estado = "✅ SÍ" if existe else "❌ NO"
    print(f"{estado} - {col}")

print("\n" + "=" * 50)