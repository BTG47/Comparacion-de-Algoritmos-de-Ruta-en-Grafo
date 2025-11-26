import sys
import os
from pathlib import Path

# SOLUCIÓN: Añadir el directorio src al path de Python
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# AHORA las importaciones deberían funcionar
try:
    from algorithms import PathAlgorithms
    from graph_creator import crear_grafo, validar_grafo
    from visualization import visualizar_grafo_interactivo
except ImportError as e:
    print(f"Error de importación: {e}")
    print("Directorio actual:", os.getcwd())
    print("Src dir:", src_dir)
    raise

import streamlit as st
import pandas as pd
import networkx as nx

# Configuración de la página
st.set_page_config(
    page_title="Comparador de Algoritmos de Ruta",
    page_icon="🗺️",
    layout="wide"
)

# Título principal
st.title("🗺️ Comparador de Algoritmos de Ruta")
st.markdown("---")

# Inicializar el objeto de algoritmos
@st.cache_resource
def get_algorithms():
    return PathAlgorithms()

algoritmos = get_algorithms()

# ===== SELECTOR DE MODO =====
st.sidebar.header("🔧 Configuración")
modo = st.sidebar.radio(
    "Selecciona el modo:",
    ["📁 Cargar CSV Existente", "🔄 Generar Nuevo Grafo"]
)

grafo = None
nodos_disponibles = []

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
            grafo = nx.from_pandas_edgelist(df, 'nodo_origen', 'nodo_destino', ['weight'])
            nodos_disponibles = list(grafo.nodes())
            
            st.success(f"✅ Grafo cargado: {len(nodos_disponibles)} nodos, {grafo.number_of_edges()} aristas")
            
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
            step=10
        )
    
    with col2:
        tamano_mapa = st.number_input(
            "Tamaño del mapa",
            min_value=100,
            max_value=2000,
            value=1000,
            step=100
        )
    
    with col3:
        radio_conexion = st.number_input(
            "Radio de conexión",
            min_value=10,
            max_value=500,
            value=150,
            step=10
        )
    
    if st.button("🎯 Generar Grafo", type="primary"):
        with st.spinner("Generando grafo..."):
            try:
                grafo = crear_grafo(num_nodos, tamano_mapa, radio_conexion)
                nodos_disponibles = list(grafo.nodes())
                
                # Validar el grafo generado
                st.text("Validación del grafo:")
                validation_output = []
                
                # Validar pesos negativos
                pesos_negativos = any(
                    grafo[u][v].get('weight', 1) < 0 
                    for u, v in grafo.edges()
                )
                validation_output.append(f"✅ Sin pesos negativos: {not pesos_negativos}")
                
                # Validar conectividad
                es_conexo = nx.is_connected(grafo)
                validation_output.append(f"✅ Grafo conexo: {es_conexo}")
                
                for line in validation_output:
                    st.text(line)
                
                st.success(f"✅ Grafo generado: {len(nodos_disponibles)} nodos, {grafo.number_of_edges()} aristas")
                
            except Exception as e:
                st.error(f"❌ Error generando grafo: {e}")

# ===== CONFIGURACIÓN DE ALGORITMO (solo si tenemos grafo) =====
if grafo is not None and len(nodos_disponibles) > 0:
    st.markdown("---")
    st.header("🎯 Configurar Algoritmo")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        origen = st.selectbox(
            "Nodo Origen",
            options=nodos_disponibles,
            index=0
        )
    
    with col2:
        destino = st.selectbox(
            "Nodo Destino", 
            options=nodos_disponibles,
            index=min(1, len(nodos_disponibles)-1)
        )
    
    with col3:
        algoritmo_seleccionado = st.selectbox(
            "Algoritmo a ejecutar",
            options=["Dijkstra", "A*", "Dijkstra Bidireccional"]
        )
    
    # Mapeo de nombres a funciones
    algoritmo_funciones = {
        "Dijkstra": algoritmos.dijkstra_con_contador,
        "A*": algoritmos.astar_con_heuristica, 
        "Dijkstra Bidireccional": algoritmos.dijkstra_bidireccional
    }
    
    if st.button("🚀 Ejecutar Algoritmo", type="primary"):
        with st.spinner("Ejecutando algoritmo..."):
            try:
                # Ejecutar algoritmo seleccionado
                funcion_algoritmo = algoritmo_funciones[algoritmo_seleccionado]
                resultado = funcion_algoritmo(grafo, origen, destino)
                
                # ===== MOSTRAR RESULTADOS =====
                st.markdown("---")
                st.header("📊 Resultados")
                
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
                
                # ===== VISUALIZACIÓN =====
                st.subheader("🕸️ Visualización del Grafo")
                
                # Crear visualización interactiva
                try:
                    html_file = visualizar_grafo_interactivo(grafo, resultado['ruta'])
                    with open(html_file, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    st.components.v1.html(html_content, height=600)
                    
                except Exception as e:
                    st.warning(f"Visualización no disponible: {e}")
                    # Fallback: mostrar información del grafo
                    st.write(f"**Grafo:** {grafo.number_of_nodes()} nodos, {grafo.number_of_edges()} aristas")
                    st.write(f"**Ruta resaltada:** {len(resultado['ruta'])} nodos")
                
                # ===== COMPARACIÓN CON OTROS ALGORITMOS =====
                st.subheader("📈 Comparación Rápida")
                
                if st.checkbox("Mostrar comparación con todos los algoritmos"):
                    with st.spinner("Ejecutando comparación..."):
                        try:
                            resultados_completos = algoritmos.ejecutar_todos_algoritmos(grafo, origen, destino)
                            
                            # Crear tabla comparativa
                            comparacion_data = []
                            for algo_name in ['dijkstra', 'astar', 'bidireccional']:
                                algo_result = resultados_completos[algo_name]
                                comparacion_data.append({
                                    'Algoritmo': algo_name.title(),
                                    'Distancia': algo_result['distancia'],
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
                                
                        except Exception as e:
                            st.error(f"Error en comparación: {e}")
                
            except Exception as e:
                st.error(f"❌ Error ejecutando algoritmo: {e}")

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