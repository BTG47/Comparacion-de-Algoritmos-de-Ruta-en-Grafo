import streamlit as st
import pandas as pd
import networkx as nx
from pathlib import Path
import sys
import os

# Configurar imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

try:
    from algorithms import PathAlgorithms
    from graph_creator import crear_grafo, validar_grafo
    from visualization import visualizar_grafo_interactivo
except ImportError as e:
    st.error(f"Error importando módulos: {e}")
    st.stop()

# Configuración de la página
st.set_page_config(
    page_title="Comparador de Algoritmos de Ruta",
    page_icon="🗺️",
    layout="wide"
)

# Inicializar estado de la sesión
if 'grafo' not in st.session_state:
    st.session_state.grafo = None
if 'nodos_disponibles' not in st.session_state:
    st.session_state.nodos_disponibles = []
if 'modo' not in st.session_state:
    st.session_state.modo = "📁 Cargar CSV Existente"

# Inicializar algoritmos
@st.cache_resource
def get_algorithms():
    return PathAlgorithms()

algoritmos = get_algorithms()

# Título principal
st.title("🗺️ Comparador de Algoritmos de Ruta")
st.markdown("---")

# ===== SELECTOR DE MODO EN SIDEBAR =====
st.sidebar.header("🔧 Configuración")
modo = st.sidebar.radio(
    "Selecciona el modo:",
    ["📁 Cargar CSV Existente", "🔄 Generar Nuevo Grafo"],
    key="modo_selector"
)

# ===== MODO: CARGAR CSV =====
if modo == "📁 Cargar CSV Existente":
    st.header("📁 Cargar Grafo desde CSV")
    
    archivo_csv = st.file_uploader(
        "Sube tu archivo CSV de grafo",
        type=['csv'],
        help="El CSV debe tener columnas: nodo_origen, nodo_destino, weight"
    )
    
    if archivo_csv is not None:
        try:
            # Leer CSV y crear grafo
            df = pd.read_csv(archivo_csv)
            # Verificar columnas necesarias
            if not all(col in df.columns for col in ['nodo_origen', 'nodo_destino', 'weight']):
                st.error("El CSV debe contener las columnas: nodo_origen, nodo_destino, weight")
            else:
                grafo = nx.from_pandas_edgelist(df, 'nodo_origen', 'nodo_destino', ['weight'])
                st.session_state.grafo = grafo
                st.session_state.nodos_disponibles = list(grafo.nodes())
                st.success(f"✅ Grafo cargado: {len(st.session_state.nodos_disponibles)} nodos, {grafo.number_of_edges()} aristas")
                
        except Exception as e:
            st.error(f"❌ Error cargando el CSV: {e}")

# ===== MODO: GENERAR GRAFO =====
else:
    st.header("🔄 Generar Nuevo Grafo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num_nodos = st.number_input(
            "Número de nodos",
            min_value=10,
            max_value=2000,
            value=100,
            step=10,
            key="num_nodos_input"
        )
    
    with col2:
        tamano_mapa = st.number_input(
            "Tamaño del mapa",
            min_value=100,
            max_value=2000,
            value=1000,
            step=100,
            key="tamano_mapa_input"
        )
    
    with col3:
        radio_conexion = st.number_input(
            "Radio de conexión",
            min_value=10,
            max_value=500,
            value=150,
            step=10,
            key="radio_conexion_input"
        )
    
    # Botón para generar grafo
    if st.button("🎯 Generar Grafo", type="primary", key="generar_grafo_btn"):
        with st.spinner("Generando grafo..."):
            try:
                grafo = crear_grafo(num_nodos, tamano_mapa, radio_conexion)
                st.session_state.grafo = grafo
                st.session_state.nodos_disponibles = list(grafo.nodes())
                
                # Mostrar validación básica
                st.success(f"✅ Grafo generado: {len(st.session_state.nodos_disponibles)} nodos, {grafo.number_of_edges()} aristas")
                
                # Validación simple
                es_conexo = nx.is_connected(grafo)
                if not es_conexo:
                    st.warning("⚠️ El grafo generado NO es conexo. Algunos nodos pueden estar aislados.")
                
            except Exception as e:
                st.error(f"❌ Error generando grafo: {e}")

# ===== CONFIGURACIÓN DE ALGORITMO (solo si tenemos grafo) =====
if st.session_state.grafo is not None and len(st.session_state.nodos_disponibles) > 0:
    st.markdown("---")
    st.header("🎯 Configurar y Ejecutar Algoritmo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        origen = st.selectbox(
            "Nodo Origen",
            options=st.session_state.nodos_disponibles,
            index=0,
            key="origen_select"
        )
    
    with col2:
        destino = st.selectbox(
            "Nodo Destino", 
            options=st.session_state.nodos_disponibles,
            index=min(1, len(st.session_state.nodos_disponibles)-1),
            key="destino_select"
        )
    
    with col3:
        algoritmo_seleccionado = st.selectbox(
            "Algoritmo a ejecutar",
            options=["Dijkstra", "A*", "Dijkstra Bidireccional"],
            key="algoritmo_select"
        )
    
    # Mapeo de nombres a funciones
    algoritmo_funciones = {
        "Dijkstra": algoritmos.dijkstra_con_contador,
        "A*": algoritmos.astar_con_heuristica, 
        "Dijkstra Bidireccional": algoritmos.dijkstra_bidireccional
    }
    
    # Botón para ejecutar algoritmo individual
    if st.button("🚀 Ejecutar Algoritmo Seleccionado", type="primary", key="ejecutar_algoritmo_btn"):
        with st.spinner(f"Ejecutando {algoritmo_seleccionado}..."):
            try:
                # Ejecutar algoritmo seleccionado
                funcion_algoritmo = algoritmo_funciones[algoritmo_seleccionado]
                resultado = funcion_algoritmo(st.session_state.grafo, origen, destino)
                
                # Guardar resultado en estado de sesión
                st.session_state.ultimo_resultado = resultado
                st.session_state.algoritmo_ejecutado = algoritmo_seleccionado
                
                # Mostrar resultados inmediatamente
                st.markdown("---")
                st.header("📊 Resultados del Algoritmo")
                
                # Métricas principales
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Distancia Total", f"{resultado['distancia']:.2f}")
                
                with col2:
                    st.metric("Nodos Expandidos", resultado['nodos_expandidos'])
                
                with col3:
                    st.metric("Tiempo Ejecución", f"{resultado['tiempo']:.4f}s")
                
                with col4:
                    st.metric("Longitud Ruta", len(resultado['ruta']))
                
                # Mostrar ruta
                st.subheader("📍 Ruta Encontrada")
                st.write(" → ".join(map(str, resultado['ruta'])))
                
                # Visualización
                st.subheader("🕸️ Visualización del Grafo")
                try:
                    html_file = visualizar_grafo_interactivo(st.session_state.grafo, resultado['ruta'])
                    with open(html_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    st.components.v1.html(html_content, height=600, scrolling=True)
                    
                except Exception as e:
                    st.warning(f"Visualización no disponible: {e}")
                    st.info(f"**Grafo:** {st.session_state.grafo.number_of_nodes()} nodos, {st.session_state.grafo.number_of_edges()} aristas")
                    st.info(f"**Ruta resaltada:** {len(resultado['ruta'])} nodos")
                
            except Exception as e:
                st.error(f"❌ Error ejecutando algoritmo: {e}")
    
    # ===== COMPARACIÓN CON TODOS LOS ALGORITMOS =====
    st.markdown("---")
    st.header("📈 Comparación Completa")
    
    # Usar un botón separado para la comparación
    if st.button("🔄 Ejecutar Comparación con los 3 Algoritmos", key="comparar_algoritmos_btn"):
        with st.spinner("Ejecutando comparación completa..."):
            try:
                # Ejecutar todos los algoritmos
                resultados_completos = algoritmos.ejecutar_todos_algoritmos(
                    st.session_state.grafo, origen, destino
                )
                
                # Guardar en estado de sesión
                st.session_state.comparacion_completa = resultados_completos
                
                # Crear tabla comparativa
                st.subheader("📋 Comparativa de Resultados")
                comparacion_data = []
                for algo_name in ['dijkstra', 'astar', 'bidireccional']:
                    algo_result = resultados_completos[algo_name]
                    comparacion_data.append({
                        'Algoritmo': algo_name.title(),
                        'Distancia': f"{algo_result['distancia']:.2f}",
                        'Nodos Expandidos': algo_result['nodos_expandidos'],
                        'Tiempo (s)': f"{algo_result['tiempo']:.6f}",
                        'Longitud Ruta': len(algo_result['ruta'])
                    })
                
                df_comparacion = pd.DataFrame(comparacion_data)
                st.dataframe(df_comparacion, use_container_width=True)
                
                # Mostrar validación
                validacion = resultados_completos['validacion']
                if validacion['validacion_exitosa']:
                    st.success("✅ Todos los algoritmos encontraron la misma ruta óptima")
                else:
                    st.warning("⚠️ Los algoritmos encontraron rutas diferentes")
                    
                # Mostrar detalles de validación
                with st.expander("📊 Detalles de Validación"):
                    st.json(validacion['comparacion_detallada'])
                    
            except Exception as e:
                st.error(f"❌ Error en comparación completa: {e}")
                st.info("💡 Tip: Verifica que los nodos origen y destino estén conectados en el grafo")

else:
    # Estado inicial - mostrar instrucciones
    st.markdown("---")
    st.info("👆 Selecciona un modo y configura tu grafo para comenzar")

# ===== INSTRUCCIONES EN EL SIDEBAR =====
st.sidebar.markdown("---")
st.sidebar.header("ℹ️ Instrucciones")

st.sidebar.markdown("""
1. **Selecciona modo**: Cargar CSV o generar grafo nuevo
2. **Configura** los parámetros del grafo
3. **Elige** nodos origen y destino  
4. **Selecciona** el algoritmo a ejecutar
5. **Visualiza** resultados y comparativas
""")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Algoritmos disponibles:**\n"
    "- Dijkstra: Ruta más corta garantizada\n"  
    "- A*: Optimizado con heurística\n"
    "- Dijkstra Bidireccional: Búsqueda desde ambos extremos"
)