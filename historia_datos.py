import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# Configuración de la página con Streamlit
st.set_page_config(page_title="Historia de Datos", layout="wide")

# --- SECCIÓN 1: INTRODUCCIÓN ---
# Aqui se inicia con el storytelling usando funciones de streamlit
st.title("El Gran Salto: ¿Somos todos más ricos y saludables?")

# En lugar de usar HTML usamos Markdown
st.markdown("""
Durante décadas, el mundo ha experimentado cambios drásticos. Esta visualización interactiva te permite explorar la evolución de la riqueza (PIB per cápita) y la salud (Esperanza de Vida) de las naciones desde 1952.

**¿Ves una tendencia global o solo casos aislados?** Usa los controles para descubrir la historia.
""")

# --- SECCIÓN 2: EL VIAJE INTERACTIVO ---
st.header("1. La Evolución Global a través del Tiempo")

# Cargamos el dataset incluido en Plotly Express
df = px.data.gapminder()

# Creamos el gráfico interactivo y animado con Plotly Express
fig_plotly = px.scatter(
    df, 
    x="gdpPercap", 
    y="lifeExp", 
    animation_frame="year", # Definimos que cada frame corresponda a un año 
    animation_group="country",
    size="pop",             # Tamaño por población
    color="continent",      # Color diferenciado por continente
    hover_name="country",   # Hover para mostrar el país al pasar el ratón
    log_x=True,             # Usamos una escala logarítmica para ver mejor los datos
    size_max=55, 
    range_x='', 
    range_y='',
    labels={
        "gdpPercap": "PIB por Cápita (USD, Escala Log)",
        "lifeExp": "Esperanza de Vida (Años)",
        "continent": "Continente"
    }
)

# Mejoras de Storytelling con Plotly 
fig_plotly.update_layout(
    title="Esperanza de Vida vs. Riqueza por País (1952-2007)",
    xaxis=dict(showgrid=False), # Quitamos ruido
    yaxis=dict(showgrid=True, gridcolor='LightGray')
)

# Mostramos el gráfico de Plotly en Streamlit
st.plotly_chart(fig_plotly, width='stretch')

st.markdown("""
**Análisis del Viaje:** Observa cómo las burbujas (países) se mueven en general hacia arriba y hacia la derecha. Esto indica que gran parte del mundo se ha vuelto más rico y saludable simultáneamente. Los colores permiten identificar rápidamente qué continentes se quedaron atrás en ciertas décadas.
""")


# --- SECCIÓN 3: LA CONCLUSIÓN REGIONAL ---
st.header("2. El Zoom Regional: ¿Quién se beneficia?")

# Agrupamos datos para mostrar promedios por continente y año
df_regional = df.groupby(['continent', 'year'])['lifeExp'].mean().reset_index()

# Creamos gráfico estático con Altair para resaltar tendencias
chart_altair = alt.Chart(df_regional).mark_line(point=True).encode(
    x=alt.X('year:O', title='Año'),
    y=alt.Y('lifeExp:Q', title='Esperanza de Vida Promedio'),
    color=alt.Color('continent:N', title='Continente'),
    tooltip=['continent', 'year', 'lifeExp']
).properties(
    title='Evolución de la Esperanza de Vida Promedio por Continente'
).interactive() # Permite zoom y paneo básico

# Mostramos el gráfico en Streamlit
st.altair_chart(chart_altair, width='stretch')

st.markdown("""
**La Conclusión:** Aunque la tendencia global es positiva, este gráfico de líneas resalta la disparidad. Observa cómo Europa y Oceanía mantienen una ventaja constante, mientras que África, a pesar de su mejora, sigue luchando en los niveles más bajos de esperanza de vida promedio. La historia no es igual para todos.
""")
