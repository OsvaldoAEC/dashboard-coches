import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuración esencial de la página
st.set_page_config(
    page_title="Vehicle Market Analysis",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar tus datos - CON EL NOMBRE CORRECTO
@st.cache_data
def load_data():
    try:
        # Usamos el nombre exacto de tu archivo
        df = pd.read_csv('vehicles_us_complete.csv')
        return df
    except FileNotFoundError:
        st.error("❌ Archivo 'vehicles_us_complete.csv' no encontrado")
        st.info("⚠️ Asegúrate de que el archivo esté en la misma carpeta que app.py")
        return pd.DataFrame()

# Cargar datos
df = load_data()

# Verificar si tenemos datos
if df.empty:
    st.warning("⚠️ No se pudieron cargar los datos. Verifica que el archivo esté en la carpeta correcta.")
    st.stop()

# Título principal
st.title("🚗 Vehicle Market Analysis Dashboard")

# Crear pestañas
tab1, tab2, tab3, tab4 = st.tabs([
    "Data Viewer", 
    "Histogram of condition vs model_year", 
    "Compare price distribution between manufacturers",
    "Vehicle types by manufacturer"
])
# Pestaña 1: Data Viewer
with tab1:
    st.header("Data Viewer")
    
    # Filtros en sidebar
    st.sidebar.header("Filtros Data Viewer")
    
    # Filtrar por manufacturer
    manufacturers = sorted(df['manufacturer'].unique())
    selected_manufacturers = st.sidebar.multiselect(
        'Seleccionar fabricantes:',
        options=manufacturers,
        default=manufacturers[:3]  # Primeros 3 por defecto
    )
    
    # Filtrar por condición
    conditions = sorted(df['condition'].unique())
    selected_conditions = st.sidebar.multiselect(
        'Seleccionar condiciones:',
        options=conditions,
        default=conditions  # Todas por defecto
    )
    
    # Filtrar por tipo de vehículo
    vehicle_types = sorted(df['type'].unique())
    selected_types = st.sidebar.multiselect(
        'Seleccionar tipos:',
        options=vehicle_types,
        default=vehicle_types  # Todos por defecto
    )
    
    # Checkbox para incluir manufacturers con menos de 1000 ads
    include_small_manufacturers = st.sidebar.checkbox(
        "Include manufacturers with less than 1000 ads",
        value=True
    )
    
    # Aplicar filtros
    filtered_df = df.copy()
    
    if selected_manufacturers:
        filtered_df = filtered_df[filtered_df['manufacturer'].isin(selected_manufacturers)]
    
    if selected_conditions:
        filtered_df = filtered_df[filtered_df['condition'].isin(selected_conditions)]
    
    if selected_types:
        filtered_df = filtered_df[filtered_df['type'].isin(selected_types)]
    
    if not include_small_manufacturers:
        # Filtrar manufacturers con más de 1000 anuncios
        manufacturer_counts = filtered_df['manufacturer'].value_counts()
        large_manufacturers = manufacturer_counts[manufacturer_counts >= 1000].index
        filtered_df = filtered_df[filtered_df['manufacturer'].isin(large_manufacturers)]
    
    # Mostrar datos
    st.write(f"**Mostrando {len(filtered_df)} registros**")
    st.dataframe(
        filtered_df[
            ['price', 'model_year', 'model', 'condition', 'type', 'manufacturer', 'odometer']
        ].head(20),
        height=400
    )
    
    # Mostrar estadísticas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Precio promedio", f"${filtered_df['price'].mean():,.0f}")
    with col2:
        st.metric("Total de vehículos", len(filtered_df))
    with col3:
        st.metric("Fabricantes únicos", filtered_df['manufacturer'].nunique())
    # Pestaña 2: Histogram of condition vs model_year
with tab2:
    st.header("Histogram of condition vs model_year")
    
    # Configuración del histograma
    st.sidebar.header("Configuración del Histograma")
    
    # Seleccionar condiciones a mostrar
    available_conditions = sorted(df['condition'].unique())
    selected_hist_conditions = st.sidebar.multiselect(
        'Condiciones a mostrar:',
        options=available_conditions,
        default=available_conditions,
        key='hist_conditions'
    )
    
    # Filtrar años (eliminar NaN)
    valid_years = df['model_year'].dropna()
    min_year = int(valid_years.min())
    max_year = int(valid_years.max())
    
    # Rango de años
    year_range = st.sidebar.slider(
        'Rango de años:',
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        key='year_range'
    )
    
    # Aplicar filtros
    hist_df = df[
        (df['condition'].isin(selected_hist_conditions)) &
        (df['model_year'] >= year_range[0]) &
        (df['model_year'] <= year_range[1])
    ].copy()
    
    # Crear el histograma
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Colores para cada condición
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    # Plot para cada condición
    for i, condition in enumerate(selected_hist_conditions):
        condition_data = hist_df[hist_df['condition'] == condition]
        ax.hist(
            condition_data['model_year'].dropna(),
            bins=30,
            alpha=0.7,
            label=condition,
            color=colors[i % len(colors)]
        )
    
    # Configurar el gráfico
    ax.set_xlabel('Model Year', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('Histogram of Condition vs Model Year', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Mostrar el gráfico
    st.pyplot(fig)
    
    # Estadísticas
    st.write(f"**Total de vehículos mostrados:** {len(hist_df)}")
    st.write(f"**Rango de años:** {year_range[0]} - {year_range[1]}")
    # Pestaña 3: Compare price distribution between manufacturers
with tab3:
    st.header("Compare price distribution between manufacturers")
    
    # Configuración de la comparación
    st.sidebar.header("Comparación de Fabricantes")
    
    # Seleccionar fabricantes para comparar
    available_manufacturers = sorted(df['manufacturer'].unique())
    
    col1, col2 = st.columns(2)
    
    with col1:
        manufacturer_1 = st.selectbox(
            "Select manufacturer 1:",
            options=available_manufacturers,
            index=available_manufacturers.index('chevrolet') if 'chevrolet' in available_manufacturers else 0,
            key='manuf1'
        )
    
    with col2:
        manufacturer_2 = st.selectbox(
            "Select manufacturer 2:",
            options=available_manufacturers,
            index=available_manufacturers.index('hyundai') if 'hyundai' in available_manufacturers else 1,
            key='manuf2'
        )
    
    # Checkbox para normalizar
    normalize = st.checkbox("Normalize histogram", value=False)
    
    # Filtrar datos
    manuf1_data = df[df['manufacturer'] == manufacturer_1]['price'].dropna()
    manuf2_data = df[df['manufacturer'] == manufacturer_2]['price'].dropna()
    
    # Crear el histograma comparativo
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Configurar bins
    max_price = max(manuf1_data.max(), manuf2_data.max())
    bins = np.linspace(0, max_price, 50)
    
    # Plot histogramas
    ax.hist(
        manuf1_data,
        bins=bins,
        alpha=0.7,
        label=manufacturer_1.title(),
        density=normalize,
        color='#1f77b4'
    )
    
    ax.hist(
        manuf2_data,
        bins=bins,
        alpha=0.7,
        label=manufacturer_2.title(),
        density=normalize,
        color='#ff7f0e'
    )
    
    # Configurar el gráfico
    ax.set_xlabel('Price', fontsize=12)
    ax.set_ylabel('Percent' if normalize else 'Count', fontsize=12)
    ax.set_title(f'Price Distribution: {manufacturer_1.title()} vs {manufacturer_2.title()}', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Limitar eje x para mejor visualización
    ax.set_xlim(0, min(max_price, 100000))
    
    # Mostrar el gráfico
    st.pyplot(fig)
    
    # Estadísticas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(f"{manufacturer_1.title()} - Precio promedio", f"${manuf1_data.mean():,.0f}")
    with col2:
        st.metric(f"{manufacturer_2.title()} - Precio promedio", f"${manuf2_data.mean():,.0f}")
    with col3:
        price_diff = manuf1_data.mean() - manuf2_data.mean()
        st.metric("Diferencia", f"${abs(price_diff):,.0f}", 
                 delta=f"{'Más caro' if price_diff > 0 else 'Más barato'}")
    # Pestaña 4: Vehicle types by manufacturer
with tab4:
    st.header("Vehicle types by manufacturer")
    
    # Crear un sidebar específico para esta pestaña
    with st.sidebar:
        st.header("Configuración de Tipos de Vehículos")
        
        # Seleccionar fabricantes a mostrar
        selected_manuf_types = st.multiselect(
            'Fabricantes a mostrar:',
            options=available_manufacturers,
            default=available_manufacturers[:5],  # Primeros 5 por defecto
            key='manuf_types_tab4'
        )
        
        # Seleccionar tipos de vehículo
        available_types = sorted(df['type'].dropna().unique())
        selected_vehicle_types = st.multiselect(
            'Tipos de vehículo a mostrar:',
            options=available_types,
            default=available_types,
            key='vehicle_types_tab4'
        )
    
    # Verificar que se hayan seleccionado fabricantes y tipos
    if not selected_manuf_types or not selected_vehicle_types:
        st.warning("Por favor selecciona al menos un fabricante y un tipo de vehículo")
    else:
        # Aplicar filtros
        types_df = df[
            (df['manufacturer'].isin(selected_manuf_types)) &
            (df['type'].isin(selected_vehicle_types))
        ]
        
        if types_df.empty:
            st.warning("No hay datos que coincidan con los filtros seleccionados")
        else:
            # Crear tabla pivot para el gráfico de barras
            pivot_data = types_df.pivot_table(
                index='manufacturer',
                columns='type',
                values='price',  # Usamos price como valor, pero contaremos occurrences
                aggfunc='count',
                fill_value=0
            )
            
            # Reordenar para mantener el orden de selección
            pivot_data = pivot_data.loc[selected_manuf_types]
            
            # Crear el gráfico de barras apiladas
            fig, ax = plt.subplots(figsize=(14, 8))
            
            # Colores para los tipos de vehículo
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
            
            # Plot barras apiladas
            bottom = None
            for i, vehicle_type in enumerate(selected_vehicle_types):
                if vehicle_type in pivot_data.columns:
                    counts = pivot_data[vehicle_type]
                    ax.bar(
                        pivot_data.index.astype(str),  # Convertir a string para evitar problemas
                        counts,
                        bottom=bottom,
                        label=vehicle_type,
                        color=colors[i % len(colors)],
                        alpha=0.8
                    )
                    if bottom is None:
                        bottom = counts
                    else:
                        bottom = bottom + counts
            
            # Configurar el gráfico
            ax.set_xlabel('Manufacturer', fontsize=12)
            ax.set_ylabel('Count', fontsize=12)
            ax.set_title('Vehicle Types by Manufacturer', fontsize=14)
            ax.legend(title='Vehicle Type', bbox_to_anchor=(1.05, 1), loc='upper left')
            ax.grid(True, alpha=0.3, axis='y')
            
            # Rotar labels del eje x para mejor lectura
            plt.xticks(rotation=45, ha='right')
            
            # Ajustar layout
            plt.tight_layout()
            
            # Mostrar el gráfico
            st.pyplot(fig)
            
            # Mostrar tabla de datos
            st.subheader("Datos detallados")
            st.dataframe(
                pivot_data,
                height=300
            )
            
            # Estadísticas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total de vehículos", len(types_df))
            with col2:
                st.metric("Fabricantes", len(selected_manuf_types))
            with col3:
                st.metric("Tipos de vehículo", len(selected_vehicle_types))