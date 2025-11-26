
import heapq
import time
from collections import defaultdict


class PathAlgorithms:  # Implementa los 3 algoritmos de búsqueda de rutas

    # en este bloque se pretende encontrar la ruta más corta expandiendo nodos por orden de distancia
    def dijkstra_con_contador(self, grafo, origen, destino):
        """
        Configura Dijkstra con contador de nodos expandidos

        Returns:
            dict con ruta, distancia, nodos_expandidos, tiempo
        """
        start_time = time.time()  # Inicia desde el nodo origen con distancia 0
        nodos_expandidos = 0  # Expande siempre el nodo más cercano no visitado
        # Actualiza distancias de vecinos si encuentra un camino mejor
        # Inicialización                                                                              #Cuenta cada nodo que expande
        # Reconstruye la ruta óptima al llegar al destino
        distancias = {nodo: float('inf') for nodo in grafo.nodes()}
        # Garantiza la ruta más corta pero explora muchos nodos.
        distancias[origen] = 0

        predecesores = {}
        cola_prioridad = [(0, origen)]

        while cola_prioridad:
            distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
            nodos_expandidos += 1  # CONTADOR DE NODOS EXPANDIDOS

            # Condición de término
            if nodo_actual == destino:
                break

            # Expansión de vecinos
            for vecino in grafo.neighbors(nodo_actual):
                peso = grafo[nodo_actual][vecino].get('weight', 1)
                nueva_distancia = distancia_actual + peso

                # Relajación
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    predecesores[vecino] = nodo_actual
                    heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

        # Reconstrucción de ruta
        ruta = self._reconstruir_ruta(predecesores, origen, destino)

        return {
            'ruta': ruta,
            'distancia': distancias[destino],
            'nodos_expandidos': nodos_expandidos,
            'tiempo': time.time() - start_time
        }

    # se pretende mejorar Dijkstra usando intuicion sobre hacia donde esta el destino.
    def _heuristica_euclidiana(self, grafo, nodo_actual, destino):
        """
        Implementa heurística admisible y consistente para A*
        Usa distancia euclidiana entre nodos
        """
        if 'pos' in grafo.nodes[nodo_actual] and 'pos' in grafo.nodes[destino]:  # Combina distancia real + estimación al destino
            # Prioriza nodos que parecen estar en dirección al destino
            pos_actual = grafo.nodes[nodo_actual]['pos']
            # Usa heurística euclidiana (distancia en línea recta)
            pos_destino = grafo.nodes[destino]['pos']
            return ((pos_actual[0] - pos_destino[0])**2 +  # Expande menos nodos que Dijkstra cuando la heurística es buena
                    (pos_actual[1] - pos_destino[1])**2)**0.5  # Más inteligente, menos expansiones, misma ruta óptima.
        else:
            # Fallback para grafos sin posiciones
            return 0

    def astar_con_heuristica(self, grafo, origen, destino):
        """
        Configura A* con la heurística euclidiana implementada

        Returns:
            dict con ruta, distancia, nodos_expandidos, tiempo
        """
        start_time = time.time()
        nodos_expandidos = 0

        # Inicialización A*
        g_score = {nodo: float('inf') for nodo in grafo.nodes()}
        g_score[origen] = 0

        f_score = {nodo: float('inf') for nodo in grafo.nodes()}
        f_score[origen] = self._heuristica_euclidiana(grafo, origen, destino)

        predecesores = {}
        cola_prioridad = [(f_score[origen], origen)]

        while cola_prioridad:
            _, nodo_actual = heapq.heappop(cola_prioridad)
            nodos_expandidos += 1  # CONTADOR DE NODOS EXPANDIDOS

            if nodo_actual == destino:
                break

            for vecino in grafo.neighbors(nodo_actual):
                peso = grafo[nodo_actual][vecino].get('weight', 1)
                tentative_g_score = g_score[nodo_actual] + peso

                if tentative_g_score < g_score[vecino]:
                    predecesores[vecino] = nodo_actual
                    g_score[vecino] = tentative_g_score
                    f_score[vecino] = tentative_g_score + \
                        self._heuristica_euclidiana(grafo, vecino, destino)
                    heapq.heappush(cola_prioridad, (f_score[vecino], vecino))

        # Reconstrucción de ruta
        ruta = self._reconstruir_ruta(predecesores, origen, destino)

        return {
            'ruta': ruta,
            'distancia': g_score[destino],
            'nodos_expandidos': nodos_expandidos,
            'tiempo': time.time() - start_time
        }

    # Buscar desde ambos extremos simultáneamente para mayor eficiencia.
    def dijkstra_bidireccional(self, grafo, origen, destino):
        """
        Configura Dijkstra Bidireccional para búsqueda optimizada

        Returns:
            dict con ruta, distancia, nodos_expandidos, tiempo
        """
        start_time = time.time()  # Dos búsquedas simultáneas: origen→destino y destino→origen
        nodos_expandidos_total = 0  # Expande alternadamente de ambas colas
        # Encuentra punto medio donde se juntan las búsquedas
        # Búsqueda forward (origen → destino)                                             #Combina ambas mitades de la ruta
        # Característica clave: Más rápido en grafos grandes, menos nodos expandidos.
        dist_forward = {nodo: float('inf') for nodo in grafo.nodes()}
        dist_forward[origen] = 0
        pred_forward = {}
        cola_forward = [(0, origen)]

        # Búsqueda backward (destino → origen)
        dist_backward = {nodo: float('inf') for nodo in grafo.nodes()}
        dist_backward[destino] = 0
        pred_backward = {}
        cola_backward = [(0, destino)]

        # Variables para el encuentro
        mejor_distancia = float('inf')
        nodo_encuentro = None

        while cola_forward and cola_backward:
            # Expansión desde el origen
            if cola_forward:
                dist_f, nodo_f = heapq.heappop(cola_forward)
                nodos_expandidos_total += 1  # CONTADOR DE NODOS EXPANDIDOS

                # Verificar mejora en la distancia
                if dist_f + dist_backward.get(nodo_f, float('inf')) < mejor_distancia:
                    mejor_distancia = dist_f + \
                        dist_backward.get(nodo_f, float('inf'))
                    nodo_encuentro = nodo_f

                # Expandir vecinos en dirección forward
                for vecino in grafo.neighbors(nodo_f):
                    peso = grafo[nodo_f][vecino].get('weight', 1)
                    nueva_dist = dist_f + peso
                    if nueva_dist < dist_forward[vecino]:
                        dist_forward[vecino] = nueva_dist
                        pred_forward[vecino] = nodo_f
                        heapq.heappush(cola_forward, (nueva_dist, vecino))

            # Expansión desde el destino
            if cola_backward:
                dist_b, nodo_b = heapq.heappop(cola_backward)
                nodos_expandidos_total += 1  # CONTADOR DE NODOS EXPANDIDOS

                # Verificar mejora en la distancia
                if dist_b + dist_forward.get(nodo_b, float('inf')) < mejor_distancia:
                    mejor_distancia = dist_b + \
                        dist_forward.get(nodo_b, float('inf'))
                    nodo_encuentro = nodo_b

                # Expandir vecinos en dirección backward
                for vecino in grafo.neighbors(nodo_b):
                    peso = grafo[nodo_b][vecino].get('weight', 1)
                    nueva_dist = dist_b + peso
                    if nueva_dist < dist_backward[vecino]:
                        dist_backward[vecino] = nueva_dist
                        pred_backward[vecino] = nodo_b
                        heapq.heappush(cola_backward, (nueva_dist, vecino))

        # Reconstrucción de ruta bidireccional
        ruta = self._reconstruir_ruta_bidireccional(
            pred_forward, pred_backward, origen, destino, nodo_encuentro
        )

        return {
            'ruta': ruta,
            'distancia': mejor_distancia,
            'nodos_expandidos': nodos_expandidos_total,
            'tiempo': time.time() - start_time
        }

    # Funciones helper para construir la ruta final a partir de los predecesores
    def _reconstruir_ruta(self, predecesores, origen, destino):
        """Reconstruye la ruta desde el destino hasta el origen"""
        if destino not in predecesores:                                       # Convierten la información de "quién viene de dónde" en una ruta ordenada.
            return []

        ruta = []
        nodo_actual = destino

        while nodo_actual != origen:
            ruta.insert(0, nodo_actual)
            nodo_actual = predecesores[nodo_actual]

        ruta.insert(0, origen)
        return ruta

    def _reconstruir_ruta_bidireccional(self, pred_forward, pred_backward, origen, destino, nodo_encuentro):
        """Reconstruye la ruta para Dijkstra bidireccional"""
        if nodo_encuentro is None:
            return []

        # Primera mitad: origen → nodo_encuentro
        primera_mitad = []
        nodo_actual = nodo_encuentro
        while nodo_actual != origen:
            primera_mitad.insert(0, nodo_actual)
            nodo_actual = pred_forward[nodo_actual]
        primera_mitad.insert(0, origen)

        # Segunda mitad: nodo_encuentro → destino
        segunda_mitad = []
        nodo_actual = nodo_encuentro
        while nodo_actual != destino:
            nodo_actual = pred_backward[nodo_actual]
            segunda_mitad.append(nodo_actual)

        return primera_mitad + segunda_mitad

    # Confirmar que los 3 algoritmos encontraron la misma solución óptima
    def verificar_rutas_iguales(self, resultado_dijkstra, resultado_astar, resultado_bidireccional, tolerancia=1e-6):
        """
        VALIDA que todos los algoritmos dan la misma ruta óptima

        Args:
            resultado_*: resultados de cada algoritmo
            tolerancia: margen para comparación de distancias

        Returns:
            dict con resultados de validación
        """
        # Verificar que las rutas son idénticas                                                                                                # verifica rutas idénticas: Misma secuencia de nodos
        rutas_identicas = (  # Distancias iguales: Misma longitud total del camino
            # Consistencia: Todos llegaron a la solución óptima
            resultado_dijkstra['ruta'] == resultado_astar['ruta'] == resultado_bidireccional['ruta']
        )  # Garantiza que las implementaciones son correctas

        # Verificar que las distancias son iguales (dentro de tolerancia)
        distancias_iguales = (
            abs(resultado_dijkstra['distancia'] - resultado_astar['distancia']) < tolerancia and
            abs(resultado_astar['distancia'] - resultado_bidireccional['distancia']) < tolerancia and
            abs(resultado_dijkstra['distancia'] -
                resultado_bidireccional['distancia']) < tolerancia
        )

        # Información detallada para debugging
        comparacion_detallada = {
            'dijkstra': {
                'distancia': resultado_dijkstra['distancia'],
                'longitud_ruta': len(resultado_dijkstra['ruta']),
                'nodos_expandidos': resultado_dijkstra['nodos_expandidos']
            },
            'astar': {
                'distancia': resultado_astar['distancia'],
                'longitud_ruta': len(resultado_astar['ruta']),
                'nodos_expandidos': resultado_astar['nodos_expandidos']
            },
            'bidireccional': {
                'distancia': resultado_bidireccional['distancia'],
                'longitud_ruta': len(resultado_bidireccional['ruta']),
                'nodos_expandidos': resultado_bidireccional['nodos_expandidos']
            }
        }

        return {
            'rutas_identicas': rutas_identicas,
            'distancias_iguales': distancias_iguales,
            'validacion_exitosa': rutas_identicas and distancias_iguales,
            'comparacion_detallada': comparacion_detallada
        }

    # Orquestar la ejecución completa de los 3 algoritmos + validación.
    def ejecutar_todos_algoritmos(self, grafo, origen, destino):
        """
        Ejecuta los 3 algoritmos y valida que den la misma ruta óptima

        Returns:
            dict con resultados de los 3 algoritmos y validación
        """
        print(
            f"Ejecutando algoritmos: {origen} → {destino}")  # Ejecuta Dijkstra, A* y Bidireccional
        # Recolecta resultados de cada uno
        # Configurar y ejecutar los 3 algoritmos                                             #Valida consistencia entre ellos
        resultado_dijkstra = self.dijkstra_con_contador(
            grafo, origen, destino)  # Retorna todos los resultados organizados
        # Punto de entrada principal para usar los algoritmos
        resultado_astar = self.astar_con_heuristica(grafo, origen, destino)
        resultado_bidireccional = self.dijkstra_bidireccional(
            grafo, origen, destino)

        # Validar que todos dan la misma ruta óptima
        validacion = self.verificar_rutas_iguales(
            resultado_dijkstra, resultado_astar, resultado_bidireccional
        )

        return {
            'dijkstra': resultado_dijkstra,
            'astar': resultado_astar,
            'bidireccional': resultado_bidireccional,
            'validacion': validacion
        }
