import networkx as nx
from pyvis.network import Network
import tempfile
import os

def visualizar_grafo_interactivo(grafo, ruta=None, altura="600px", ancho="100%"):
    """
    Crea una visualización interactiva del grafo usando PyVis
    
    Args:
        grafo: Grafo de NetworkX
        ruta: Lista de nodos que forman la ruta a resaltar
        altura: Altura del visualizador
        ancho: Ancho del visualizador
    
    Returns:
        str: Ruta al archivo HTML generado
    """
    # Crear red PyVis
    net = Network(height=altura, width=ancho, directed=False)
    
    # Configuraciones de visualización
    net.set_options("""
    var options = {
        "physics": {
            "enabled": true,
            "stabilization": {"iterations": 100}
        },
        "interaction": {"hover": true}
    }
    """)
    
    # Añadir nodos
    for nodo in grafo.nodes():
        # Obtener posición si existe
        pos = grafo.nodes[nodo].get('pos', (0, 0))
        
        # Configurar color según si está en la ruta
        color = "#97c2fc"  # Azul claro por defecto
        if ruta and nodo in ruta:
            color = "#ff6b6b"  # Rojo para nodos en ruta
        
        net.add_node(
            nodo, 
            label=str(nodo),
            x=pos[0] if pos else None,
            y=pos[1] if pos else None,
            color=color,
            size=25 if ruta and nodo in ruta else 15
        )
    
    # Añadir aristas
    for u, v in grafo.edges():
        # Configurar color según si está en la ruta
        color = "#2B7CE9"  # Azul por defecto
        width = 3
        if ruta and ((u in ruta and v in ruta) and 
                    (abs(ruta.index(u) - ruta.index(v)) == 1 if u in ruta and v in ruta else False)):
            color = "#ff0000"  # Rojo para aristas en ruta
            width = 5
        
        peso = grafo[u][v].get('weight', 1)
        net.add_edge(
            u, v, 
            color=color,
            width=width,
            title=f"Peso: {peso:.2f}"
        )
    
    # Generar archivo temporal
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        net.write_html(f.name)
        return f.name

def visualizar_grafo_simple(grafo, ruta=None):
    """
    Versión simple de visualización para casos de error
    """
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Obtener posiciones o usar layout por defecto
    pos = nx.get_node_attributes(grafo, 'pos')
    if not pos:
        pos = nx.spring_layout(grafo)
    
    # Dibujar grafo completo
    nx.draw_networkx_nodes(grafo, pos, node_color='lightblue', node_size=100, ax=ax)
    nx.draw_networkx_edges(grafo, pos, edge_color='gray', alpha=0.6, ax=ax)
    nx.draw_networkx_labels(grafo, pos, font_size=8, ax=ax)
    
    # Resaltar ruta si existe
    if ruta and len(ruta) > 1:
        edges_ruta = [(ruta[i], ruta[i+1]) for i in range(len(ruta)-1)]
        nx.draw_networkx_edges(grafo, pos, edgelist=edges_ruta, 
                              edge_color='red', width=2, ax=ax)
        nx.draw_networkx_nodes(grafo, pos, nodelist=ruta, 
                              node_color='red', node_size=150, ax=ax)
    
    ax.set_title("Visualización del Grafo")
    ax.axis('off')
    
    return fig