import streamlit as st
import pulp

st.set_page_config(page_title="Optimización Binaria con PuLP", layout="centered")

st.title("🎒 Optimizador de Mochila (Programación Binaria)")
st.write("""
Esta aplicación resuelve problemas de optimización lineal entera binaria.
Personaliza el número de elementos, sus valores en la función objetivo y sus pesos/impactos en la restricción.
""")

# 1. Configuración de parámetros
st.sidebar.header("Configuración General")
n_variables = st.sidebar.number_input("Número de Variables (Elementos)", min_value=1, max_value=10, value=4, step=1)

st.subheader("Parámetros del Problema")

# Ingreso de datos de forma dinámica
col1, col2 = st.columns(2)

valores = {}
pesos = {}

with col1:
    st.markdown("**Valores en la Función Objetivo (Maximizar)**")
    for i in range(1, n_variables + 1):
        valores[i] = st.number_input(f"Valor/Costo de x{i}", value=float(15 - i*2) if i <= 4 else 5.0, key=f"val_{i}")

with col2:
    st.markdown("**Pesos/Impacto en la Restricción**")
    for i in range(1, n_variables + 1):
        pesos[i] = st.number_input(f"Peso/Impacto de x{i}", value=float(10 - i*2) if i <= 4 else 3.0, key=f"peso_{i}")

st.markdown("---")
capacidad = st.number_input("Capacidad Máxima o Límite de la Restricción (≤)", value=9.0, step=1.0)

# Botón para resolver
if st.button("⚡ Resolver Modelo"):
    # Crear el problema de maximización
    prob = pulp.LpProblem("Problema_Mochila_Binaria", pulp.LpMaximize)
    
    # Crear las variables como binarias
    indices = list(range(1, n_variables + 1))
    x = pulp.LpVariable.dicts("x", indices, cat=pulp.LpBinary)
    
    # Definir Función Objetivo
    prob += pulp.lpSum([valores[i] * x[i] for i in indices]), "Funcion_Objetivo"
    
    # Definir Restricción de Capacidad
    prob += pulp.lpSum([pesos[i] * x[i] for i in indices]) <= capacidad, "Restriccion_Capacidad"
    
    # Resolver
    status = prob.solve()
    
    # Mostrar Resultados
    st.success(f"¡Modelo Resuelto! Estado de la solución: **{pulp.LpStatus[status]}**")
    
    st.subheader("Resultados de las Variables:")
    cols_res = st.columns(min(n_variables, 4))
    for idx, i in enumerate(indices):
        val_optimo = pulp.value(x[i])
        with cols_res[idx % len(cols_res)]:
            st.metric(
                label=f"Variable x{i}",
                value=f"{int(val_optimo)}",
                delta="Seleccionado" if val_optimo == 1 else "No Seleccionado",
                delta_color="normal" if val_optimo == 1 else "inverse"
            )
            
    st.markdown("---")
    st.subheader("Resumen General")
    peso_total_utilizado = sum(pesos[i] * pulp.value(x[i]) for i in indices)
    
    st.write(f"🏆 **Valor Óptimo de la Función Objetivo:** {pulp.value(prob.objective):.2f}")
    st.write(f"⚖️ **Capacidad Utilizada:** {peso_total_utilizado:.2f} de {capacidad:.2f}")
