import random
import time
import tracemalloc
import pandas as pd

from algorithms import PathAlgorithms

# ------------------ medir_tiempo_y_memoria ------------------


def medir_tiempo_y_memoria(algoritmos, grafo, origen, destino, nombre_algoritmo):
    """
    Ejecuta un algoritmo (Dijkstra, A* o Bidireccional) midiendo:
    - tiempo con time.time()
    - pico de memoria con tracemalloc
    - nodos expandidos (del resultado del algoritmo)

    Devuelve un diccionario con todas las métricas.
    """

    # Elegir la función correcta según el nombre
    if nombre_algoritmo == "dijkstra":
        func = algoritmos.dijkstra_con_contador
    elif nombre_algoritmo == "astar":
        func = algoritmos.astar_con_heuristica
    elif nombre_algoritmo == "bidireccional":
        func = algoritmos.dijkstra_bidireccional
    else:
        raise ValueError(f"Algoritmo desconocido: {nombre_algoritmo}")

    # Medición de tiempo + memoria
    tracemalloc.start()
    t0 = time.time()
    resultado = func(grafo, origen, destino)
    t1 = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Armamos un registro plano para el CSV
    registro = {
        "origen": origen,
        "destino": destino,
        "algoritmo": nombre_algoritmo,
        "distancia": resultado["distancia"],
        "nodos_expandidos": resultado["nodos_expandidos"],
        # el que ya calculas dentro del método
        "tiempo_interno_algoritmo": resultado["tiempo"],
        # medido externamente por ROL 3
        "tiempo_medido_experimento": t1 - t0,
        "memoria_peak_KB": peak / 1024.0                    # pico de memoria en KB
    }
    return registro


# ------------------ ejecutar_todos_los_casos ------------------

def ejecutar_todos_los_casos(grafo, num_casos=30, semilla=42):
    """
    Genera automáticamente varios pares (origen, destino) y
    ejecuta los 3 algoritmos para cada par.

    Devuelve un DataFrame con TODOS los resultados.
    """
    random.seed(semilla)
    nodos = list(grafo.nodes())
    algoritmos = PathAlgorithms()

    registros = []

    for i in range(num_casos):
        # Elegir origen y destino distintos al azar
        origen, destino = random.sample(nodos, 2)

        for nombre_alg in ["dijkstra", "astar", "bidireccional"]:
            reg = medir_tiempo_y_memoria(
                algoritmos, grafo, origen, destino, nombre_alg)
            reg["caso_id"] = i
            reg["num_nodos_grafo"] = grafo.number_of_nodes()
            reg["num_aristas_grafo"] = grafo.number_of_edges()
            registros.append(reg)

    df_resultados = pd.DataFrame(registros)
    return df_resultados


# ------------------ generar_csv_resultados ------------------

def generar_csv_resultados(df_resultados, nombre_archivo="resultados_experimentos.csv"):
    """
    Guarda el DataFrame con todos los experimentos en un CSV.
    """
    df_resultados.to_csv(nombre_archivo, index=False)
    print(f"CSV de resultados guardado en: {nombre_archivo}")


# ------------------ calcular_estadisticas ------------------

def calcular_estadisticas(df_resultados):
    """
    Calcula estadísticas agregadas por algoritmo:
    - tiempo promedio
    - desviación estándar del tiempo
    - promedio de nodos expandidos
    - promedio de memoria usada

    Devuelve otro DataFrame con el resumen.
    """
    resumen = (
        df_resultados
        .groupby("algoritmo")
        .agg(
            tiempo_promedio=("tiempo_medido_experimento", "mean"),
            tiempo_std=("tiempo_medido_experimento", "std"),
            expansiones_promedio=("nodos_expandidos", "mean"),
            memoria_promedio_KB=("memoria_peak_KB", "mean")
        )
        .reset_index()
    )
    return resumen
