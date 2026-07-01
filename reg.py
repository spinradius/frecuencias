import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from functools import lru_cache
import io

# Datos de instrumentos y voces, incluyendo piano y guitarra
data = {
    'Instrumento': [
        'Piano', 'Guitarra', 'Violín', 'Viola', 'Violonchelo', 'Contrabajo',
        'Flauta', 'Oboe', 'Clarinete', 'Fagot',
        'Voz de niño (soprano)', 'Voz de mujer (soprano)', 'Voz de mujer (alto)',
        'Voz de hombre (tenor)', 'Voz de hombre (bajo)'
    ],
    'Frecuencia_min': [
        27.5, 82.4, 196, 131, 65, 41,
        262, 247, 147, 58,
        260, 230, 175, 130, 80
    ],
    'Frecuencia_max': [
        4186, 1175, 3136, 1568, 1047, 247,
        2093, 1568, 1568, 587,
        1000, 1046, 698, 523, 349
    ],
    'Nota_min': [
        'A0', 'E2', 'G3', 'C3', 'C2', 'E1',
        'C4', 'B3', 'D3', 'Bb1',
        'C4', 'Bb3', 'F3', 'C3', 'E2'
    ],
    'Nota_max': [
        'C8', 'D6', 'G7', 'G6', 'C6', 'B3',
        'C7', 'G6', 'G6', 'D5',
        'C6', 'C6', 'F5', 'C5', 'F4'
    ],
    'Tipo': [
        'Cuerda percutida', 'Cuerda pulsada', 'Cuerda frotada', 'Cuerda frotada', 'Cuerda frotada', 'Cuerda frotada',
        'Viento madera', 'Viento madera', 'Viento madera', 'Viento madera',
        'Voz', 'Voz', 'Voz', 'Voz', 'Voz'
    ],
    'Color': [
        '#000000', '#8B4513', '#FFB3BA', '#BAFFC9', '#BAE1FF', '#FFFFBA',
        '#FFD700', '#FF69B4', '#00CED1', '#FFA500',
        '#FF1493', '#FF69B4', '#DA70D6', '#4169E1', '#000080'
    ]
}

df = pd.DataFrame(data)

# Función optimizada para convertir frecuencia a posición logarítmica
@lru_cache(maxsize=128)
def freq_to_y(freq):
    return np.log2(freq / 440) * 12 + 49

# Preparar datos para el gráfico una sola vez
df['y_min'] = df['Frecuencia_min'].apply(freq_to_y)
df['y_max'] = df['Frecuencia_max'].apply(freq_to_y)
df['y_range'] = df['y_max'] - df['y_min']

st.title('Tesitura de Instrumentos y Voces para Arregladores Musicales')

def main():
    # Sidebar Controls
    st.sidebar.header("Controles")
    
    # Instrument Filtering
    all_instruments = sorted(df['Instrumento'].unique())
    selected_instruments = st.sidebar.multiselect(
        "Seleccionar Instrumentos",
        options=all_instruments,
        default=all_instruments
    )
    
    # Type Filtering
    all_types = sorted(df['Tipo'].unique())
    selected_types = st.sidebar.multiselect(
        "Seleccionar Tipo",
        options=all_types,
        default=all_types
    )
    
    # Filter Data
    if not selected_instruments or not selected_types:
        st.warning("Por favor seleccione al menos un instrumento y un tipo.")
        return
            
    filtered_df = df[
        (df['Instrumento'].isin(selected_instruments)) & 
        (df['Tipo'].isin(selected_types))
    ]
    
    if filtered_df.empty:
        st.info("No hay datos que coincidan con los filtros actuales. Intente ajustar los filtros.")
    else:
        # Display Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Instrumentos", len(selected_instruments))
        col2.metric("Tipos", len(selected_types))
        col3.metric("Visible", len(filtered_df))
    
        # Crear el gráfico
        fig = go.Figure()
    
        # Agregar líneas para las octavas (pre-computado)
        octavas_data = [(440 * 2**i, f'C{i}') for i in range(-1, 8)]
        for freq, nota in octavas_data:
            y = freq_to_y(freq)
            fig.add_shape(type="line", x0=0, x1=1, y0=y, y1=y, 
                          line=dict(color="LightGrey", width=1, dash="dash"))
            fig.add_annotation(x=1.02, y=y, text=nota, showarrow=False, 
                               xanchor="left", font=dict(size=8))
    
        # Optimización: Usar un solo trace con múltiples barras en lugar de iterar
        custom_data = np.column_stack([
            filtered_df['Instrumento'],
            filtered_df['Tipo'],
            filtered_df['Nota_min'],
            filtered_df['Nota_max'],
            filtered_df['Frecuencia_min'],
            filtered_df['Frecuencia_max']
        ])
    
        fig.add_trace(go.Bar(
            y=filtered_df['y_range'],
            x=filtered_df['Instrumento'],
            base=filtered_df['y_min'],
            marker_color=filtered_df['Color'],
            customdata=custom_data,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>" +
                "Tipo: %{customdata[1]}<br>" +
                "Rango: %{customdata[2]} - %{customdata[3]}<br>" +
                "Frecuencia: %{customdata[4]:.0f} - %{customdata[5]:.0f} Hz" +
                "<extra></extra>"
            ),
            orientation='v'
        ))
    
        fig.update_layout(
            title='Tesitura de Instrumentos y Voces',
            xaxis_title='',
            yaxis_title='Altura (Notas)',
            barmode='overlay',
            hoverlabel=dict(bgcolor="white", font_size=10),
            showlegend=False,
            height=800,
            margin=dict(l=50, r=50, t=50, b=50)
        )
    
        fig.update_xaxes(tickangle=45)
        fig.update_yaxes(showticklabels=False, showgrid=False)
    
        st.plotly_chart(fig, use_container_width=True)
    
        # Export Options
        st.sidebar.markdown("---")
        st.sidebar.subheader("Exportar")
        
        # CSV Export
        csv_buffer = io.StringIO()
        filtered_df.to_csv(csv_buffer, index=False)
        st.sidebar.download_button(
            label="Descargar Datos (CSV)",
            data=csv_buffer.getvalue(),
            file_name="tesitura_datos.csv",
            mime="text/csv"
        )
        
        # Data Preview (Optional)
        with st.expander("Ver Datos Completos"):
            st.dataframe(filtered_df)

if __name__ == "__main__":
    main()
    st.markdown("""
Este gráfico muestra la tesitura de varios instrumentos musicales y voces humanas de una manera compacta y visual:
- Cada barra representa el rango de un instrumento o voz.
- El eje Y muestra la altura musical en una escala logarítmica, con líneas punteadas marcando las octavas.
- Los colores distinguen entre diferentes tipos de instrumentos y voces.
- Al pasar el mouse sobre una barra, se muestra información detallada incluyendo el rango en notas y frecuencias.

Esta representación es particularmente útil para arregladores musicales, ya que permite visualizar rápidamente cómo los diferentes instrumentos y voces se superponen en términos de rango tonal.
""")
