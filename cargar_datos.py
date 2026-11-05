import os
import pandas as pd
from sqlalchemy import create_engine

carpeta = os.path.dirname(os.path.abspath(__file__))
ruta_excel = os.path.join(carpeta, "Data", "Prestamos_Data_Alumnos_v5.xlsx")

df = pd.read_excel(ruta_excel)
print("Columnas:", df.columns.tolist())
print("Filas:", len(df))

engine = create_engine("mysql+pymysql://clase:clase123@localhost:3307/creditos")
df.to_sql("clientes_credito", engine, if_exists="replace", index=False, chunksize=5000, method="multi")
print("Datos cargados en MySQL")