import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de la página web
st.set_page_config(page_title="Análisis TMDB - FCE UBA", layout="wide")

st.title("🎬 Factores Asociados al Éxito Económico de las Películas")
st.markdown("### Análisis interactivo de datos basado en TMDB 5000 - Cátedra de Métodos Cuantitativos (FCE-UBA)")

# Carga de datos local o remota
@st.cache_data
def cargar_datos():
    # Podés subir tu archivo limpio a un repositorio de GitHub y poner el link raw acá
    df = pd.read_csv("tmdb_5000_movies.csv")
    df = df[(df['budget'] > 0) & (df['revenue'] > 0)]
    df['profit'] = df['revenue'] - df['budget']
    df['roi'] = df['profit'] / df['budget']
    corte = df['budget'].quantile(0.05)
    df = df[df['budget'] >= corte]
    return df

try:
    movies = cargar_datos()
    
    # Sidebar con métricas generales
    st.sidebar.header("Métricas Globales del Dataset")
    st.sidebar.metric("Películas Analizadas", len(movies))
    st.sidebar.metric("ROI Promedio Global", f"{movies['roi'].mean():.2f}x")

    # Pestañas para cada hipótesis
    tab1, tab2, tab3, tab4 = st.tabs(["📌 Introducción", "📈 Hipótesis 1", "⭐ Hipótesis 2", "🎭 Hipótesis 3"])

    with tab1:
        st.subheader("Pregunta Principal: ¿Qué factores explican la rentabilidad de una película?")
        st.markdown("""
        Este proyecto analiza los determinantes financieros del éxito en la industria del cine utilizando técnicas analíticas avanzadas.
        A continuación, podés navegar por las pestañas para auditar la validación de cada hipótesis planteada por el equipo.
        """)
        st.dataframe(movies[['title', 'budget', 'revenue', 'roi', 'vote_average']].head(10))

    with tab2:
        st.header("H1: Presupuesto vs Recaudación")
        col1, col2 = st.columns([2, 1])
        with col1:
            fig, ax = plt.subplots()
            sns.regplot(data=movies, x='budget', y='revenue', scatter_kws={'alpha':0.3, 'color':'#2ca02c'}, line_kws={'color':'red'}, ax=ax)
            st.pyplot(fig)
        with col2:
            st.metric("Correlación de Pearson", "0.71")
            st.success("Hipótesis ACEPTADA. Invertir más capital tracciona de forma directa una mayor recaudación bruta en taquilla.")

    with tab3:
        st.header("H2: Valoraciones vs Ingresos")
        col1, col2 = st.columns([2, 1])
        with col1:
            fig, ax = plt.subplots()
            sns.scatterplot(data=movies, x='vote_average', y='revenue', alpha=0.4, color='#1f77b4', ax=ax)
            st.pyplot(fig)
        with col2:
            st.metric("Correlación de Pearson", "0.20")
            st.error("Hipótesis RECHAZADA. El puntaje de los usuarios no influye significativamente en la recaudación comercial de la película.")

    with tab4:
        st.header("H3: Rentabilidad por Género Cinematográfico")
        st.markdown("Análisis del Retorno de Inversión (ROI) segmentado por categorías principales.")
        
        # Simulación del top_roi obtenido de tu notebook
        st.markdown("**Top Géneros con mayor eficiencia financiera (ROI promedio):**")
        st.markdown("- **Horror:** 9.86x de retorno promedio")
        st.markdown("- **Mystery:** 6.06x de retorno promedio")
        st.markdown("- **Documentary:** 4.19x de retorno promedio")
        
        st.info("El género de Terror optimiza los costos de producción y genera márgenes de ganancias relativos masivos frente a los blockbusters tradicionales.")

except Exception as e:
    st.error(f"Por favor, asegurate de tener el archivo 'tmdb_5000_movies.csv' en la misma carpeta. Error: {e}")