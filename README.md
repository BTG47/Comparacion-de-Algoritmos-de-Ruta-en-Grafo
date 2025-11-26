# 🚀 Comparación de Algoritmos de Ruta en Grafos

**Proyecto de Matemáticas Discretas - Otoño 2025**  
*Sistema experimental para comparar algoritmos de búsqueda de rutas en grafos ponderados*
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://comparacion-de-algoritmos-de-ruta-en-grafo-d9tv4jmepazmwp7pfvl.streamlit.app/)
---

## 📋 Descripción del Proyecto

Este proyecto implementa y compara el rendimiento de tres algoritmos de búsqueda de rutas en grafos:
- **Algoritmo de Dijkstra**
- **Algoritmo A*** (con heurística admisible)
- **Dijkstra Bidireccional**

El sistema evalúa métricas como tiempo de ejecución, número de nodos expandidos, longitud de ruta y uso de memoria en grafos de diferentes tamaños.

---

## 🎯 Objetivos

- ✅ Implementar 3 algoritmos de búsqueda de rutas
- ✅ Diseñar experimentos con múltiples tamaños de grafo
- ✅ Comparar rendimiento empírico vs complejidad teórica
- ✅ Generar visualizaciones interactivas de los resultados

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje**: Python 3.9+
- **Librerías principales**:
  - `networkx` - Manipulación de grafos y algoritmos
  - `streamlit` - Interfaz web interactiva
  - `pyvis` - Visualización de grafos
  - `pandas` - Análisis de datos
  - `matplotlib` - Gráficas estáticas
  - `numpy` - Cálculos numéricos

---

## 📁 Estructura del Proyecto
```text
matematicas-discretas/
├── data/                  # Datos de grafos y resultados
├── resutls/               # Resultados
├── src/
│   ├── __init__.py          
│   ├── algorithms.py         # Implementación de algoritmos
│   ├── experiment_runner.py  # Scripts de experimentación
│   ├── visualization.py      # Código de visualización
│   └── graph_creator.py      # Código encargado de generar los grafos
├── app.py              # Aplicación principal Streamlit
├── run_experiments.py  # Integración de los modulos
├── requirements.txt    # Dependencias
└── README.md
```
---

## 🚀 Instalación y Uso

### Prerrequisitos
- Python 3.9 o superior
- Git

### Configuración del ambiente

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/matematicas-discretas-proyecto.git
   cd matematicas-discretas-proyecto
### Crear y activar ambiente virtual:

#### Opción 1: Con conda (recomendado)
   ```bash
conda create -n matematicas-discretas python=3.9
conda activate matematicas-discretas
```
#### Opción 2: Con venv
   ```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### Instalar dependencias:

```bash
pip install -r requirements.txt
Ejecutar la aplicación
Interfaz interactiva:
```

```bash
streamlit run app.py
```
### Ejecutar experimentos:

```bash
python src/experiments/run_experiments.py
```
### Generar reportes:

```bash
python src/visualization/generate_report.py
```
## 📊 Experimentos
### Tiempo Promedio de Ejecución (segundos)
| Algoritmo       | 100 nodos | 200 nodos | 300 nodos | 400 nodos | 500 nodos |
|-----------------|-----------|-----------|-----------|-----------|-----------|
| A*              | 0.000803  | 0.002209  | 0.002502  | 0.002777  | 0.003478  |
| Bidireccional   | 0.004902  | 0.041850  | 0.100776  | 0.140725  | 0.230989  |
| Dijkstra        | 0.001028  | 0.008705  | 0.017859  | 0.031198  | 0.046727  |

### Nodos Expandidos Promedio
| Algoritmo       | 100 nodos | 200 nodos | 300 nodos | 400 nodos | 500 nodos |
|-----------------|-----------|-----------|-----------|-----------|-----------|
| A*              | 24.04     | 14.90     | 9.96      | 11.34     | 12.68     |
| Bidireccional   | 249.28    | 622.64    | 1104.00   | 1551.40   | 2091.16   |
| Dijkstra        | 73.24     | 166.48    | 235.94    | 421.38    | 530.74    |

### Uso de Memoria Promedio (KB)
| Algoritmo       | 100 nodos | 200 nodos | 300 nodos | 400 nodos | 500 nodos |
|-----------------|-----------|-----------|-----------|-----------|-----------|
| A*              | 13.95     | 29.28     | 33.48     | 60.37     | 64.75     |
| Bidireccional   | 23.44     | 50.08     | 56.78     | 104.20    | 111.04    |
| Dijkstra        | 8.96      | 20.92     | 26.11     | 45.13     | 52.30     |

## 🔬 Análisis de Complejidad
| Algoritmo       | Complejidad Teórica | Observaciones Experimentales |
|-----------------|---------------------|------------------------------|
| Dijkstra        | O((V+E) log V)      | Tiempo crece linealmente con el tamaño del grafo |
| A*              | O((V+E) log V)      | Más eficiente con buena heurística, menos nodos expandidos |
| Bidireccional   | O((V+E) log V)      | Mayor overhead pero mejor escalabilidad en grafos grandes |

## 👥 Integrantes del Equipo
| Nombre                           | Rol                      | Responsabilidades |
|----------------------------------|--------------------------|-------------------|
| Axel Jesús Chávez Hernández      | Especialista en Grafos   | Generación de datos, validación |
| Daniel de Jesús Martínez Gallegos| Implementador de Algoritmos | Dijkstra, A*, Dijkstra Bidireccional |
| Diego Camargo Padilla            | Experimento y Métricas   | Scripts de experimentación, mediciones |
| Bruno Tarango Garay              | Visualización y Reporte  | Interfaz, gráficas, documentación |

## 🎮 Características de la Aplicación
- Generación de grafos en tiempo real con parámetros personalizables
- Carga de archivos CSV con grafos preexistentes
- Selección interactiva de nodos origen y destino
- Visualización de rutas con pyvis (grafos interactivos)
- Comparación side-by-side de algoritmos
- Exportación de resultados a CSV
- Métricas en tiempo real: tiempo, expansiones, distancia, memoria

## 🚀 Demo en Línea
La aplicación está disponible en:
https://comparacion-de-algoritmos-de-ruta-en-grafo-d9tv4jmepazmwp7pfvl.streamlit.app/

## 🤝 Contribuciones
Este proyecto es académico. Para sugerencias o issues, por favor contactar a los desarrolladores.

## 📜 Licencia
Este proyecto es con fines educativos. Desarrollado para la clase de Matemáticas Discretas, Otoño 2025.
