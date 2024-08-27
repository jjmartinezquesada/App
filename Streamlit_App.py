# IMPORTAMOS LIBRERIAS 
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

# CREAMOS LA CONEXION
engine = create_engine('postgresql://srv_calculadora:iRSoTq69l7z9ZKWx58@23.102.25.186:5432/quotationtool')


                # FUNCIONES DE LLAMADA A LA BBDD
#------------------------------------------------------------------

# Función para obtener opciones desplegables desde la base de datos
def get_distinct_values(table, column):
    query = text(f"SELECT DISTINCT {column} FROM {table}")
    with engine.connect() as connection:
        result = connection.execute(query)
        values = [row[0] for row in result]
    return values

# Función para insertar un registro
def insert_record(table, data):
    placeholders = ", ".join([f":{key}" for key in data.keys()])
    query = text(f"INSERT INTO {table} ({', '.join(data.keys())}) VALUES ({placeholders})")
    with engine.connect() as connection:
        connection.execute(query, **data)

# Función para actualizar un registro
def update_record(table, data, condition_column, condition_value):
    set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
    query = text(f"UPDATE {table} SET {set_clause} WHERE {condition_column} = :condition_value")
    with engine.connect() as connection:
        connection.execute(query, **data, condition_value=condition_value)

# Función para borrar un registro
def delete_record(table, condition_column, condition_value):
    query = text(f"DELETE FROM {table} WHERE {condition_column} = :condition_value")
    with engine.connect() as connection:
        connection.execute(query, condition_value=condition_value)

#------------------------------------------------------------------

                        # APLICACIÓN
#------------------------------------------------------------------

# Interfaz de Streamlit
st.title("Gestión de Registros")

# Desplegables obtenidos de la base de datos
empleados = get_distinct_values("reports.th_current_jira_worklogs","author_name")
proyectos = get_distinct_values("sa_bc.sa_bc_projects",'"No"')

# Seleccionar acción
accion = st.selectbox("Selecciona una acción", ["Insertar", "Actualizar", "Borrar"])


# Formulario para insertar o actualizar
if accion in ["Actualizar"]:
    empleado = st.selectbox("Selecciona un empleado", empleados)
    proyecto = st.selectbox("Selecciona un proyecto", proyectos)
    horas_trabajadas = st.number_input("Horas trabajadas", min_value=0, max_value=100)

    print("")