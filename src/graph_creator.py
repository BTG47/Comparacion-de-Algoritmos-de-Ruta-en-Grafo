# -----------------------------------Creacion de los grafos-----------------------
import networkx as nx
import numpy as np
import math
import pandas as pd


def calcular_distancia_euclidiana(pos1, pos2):
    """Calcula la distancia Euclidiana entre dos puntos (x, y)"""
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


def crear_grafo(num_nodos, tamano_mapa, radio_conexion):
    """
    Crea un grafo geométrico aleatorio.

    Los nodos se esparcen en un cuadrado de 'tamano_mapa' x 'tamano_mapa'.
    Dos nodos se conectan si su distancia es menor o igual a 'radio_conexion'.
    """
    G = nx.Graph()

    # 1. Crear nodos con posiciones aleatorias
    for i in range(num_nodos):
        # Asignar coordenadas (x, y) aleatorias
        pos = (np.random.rand() * tamano_mapa, np.random.rand() * tamano_mapa)
        G.add_node(i, pos=pos)

    # 2. Conectar nodos basados en la distancia
    # Comparamos cada par de nodos
    for i in G.nodes():
        for j in G.nodes():
            if i >= j:
                continue  # Evitar duplicados y auto-bucles

            pos_i = G.nodes[i]['pos']
            pos_j = G.nodes[j]['pos']

            distancia = calcular_distancia_euclidiana(pos_i, pos_j)

            # Si están dentro del radio, crear arista con peso = distancia
            if distancia <= radio_conexion:
                G.add_edge(i, j, weight=distancia)

    return G


def validar_grafo(G):
    """
    Realiza validaciones básicas requeridas por el proyecto.
    """
    print("--- Iniciando Validación ---")

    # 1. Validar pesos negativos
    pesos_negativos = False
    for u, v, data in G.edges(data=True):
        if data['weight'] < 0:
            print(
                f"ERROR: Arista ({u}, {v}) tiene peso negativo: {data['weight']}")
            pesos_negativos = True

    if not pesos_negativos:
        print("Validación 1/2: OK. No se encontraron pesos negativos.")

    # 2. Validar conectividad
    if nx.is_connected(G):
        print("Validación 2/2: OK. El grafo es conexo.")
    else:
        print("ADVERTENCIA: El grafo NO es conexo. Algunos nodos están aislados.")
        # Podrías querer forzar la conexión o simplemente reportarlo.
        # Para este proyecto, mientras los pares (origen, destino) de las pruebas
        # estén en el mismo componente, debería funcionar.

    print("--- Validación Terminada ---")


def guardar_grafo_csv(G, nombre_archivo):
    """
    Exporta la lista de aristas del grafo a un archivo CSV.
    El formato será: nodo1, nodo2, peso
    """
    # Convertir el grafo a un DataFrame de Pandas (CORREGIDO)
    df = nx.to_pandas_edgelist(G)

    # Renombrar columnas para consistencia
    df = df.rename(columns={
        'source': 'nodo_origen',
        'target': 'nodo_destino'
    })

    # Seleccionar solo las columnas que nos interesan
    df_exportar = df[['nodo_origen', 'nodo_destino', 'weight']]

    # Guardar a CSV
    df_exportar.to_csv(nombre_archivo, index=False)
    print(f"Grafo guardado exitosamente en '{nombre_archivo}'")
