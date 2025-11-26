# 🚀 Comparación de Algoritmos de Ruta en Grafos

**Proyecto de Matemáticas Discretas - Otoño 2025**  
*Sistema experimental para comparar algoritmos de búsqueda de rutas en grafos ponderados*

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
### Configuración experimental
Tamaños de grafo: 100, 500, 1000 nodos

Pares origen-destino: 10 pares por tamaño (cortos, medios, largos)

Repeticiones: 3 ejecuciones por caso

Métricas: Tiempo, expansiones, longitud de ruta, memoria

### Ejecutar todos los experimentos
```bash
python src/experiments/main.py
```
## 👥 Integrantes del Equipo
Nombre	Rol	Responsabilidades
[Axel Jesús Chávez Hernández]	Especialista en Grafos	Generación de datos, validación
[Daniel de Jesús Martínez Gallegos]	Implementador de Algoritmos	Dijkstra, A*, Dijkstra Bidireccional
[Diego Camargo Padilla]	Experimento y Métricas	Scripts de experimentación, mediciones
[Bruno Tarango Garay]	Visualización y Reporte	Interfaz, gráficas, documentación
## 📈 Resultados Clave
(Esta sección se completará con los hallazgos del proyecto)

### Comparación de Tiempos de Ejecución
Algoritmo	Grafo 100 nodos	Grafo 500 nodos	Grafo 1000 nodos
Dijkstra	-	-	-
A*	-	-	-
Bidireccional	-	-	-
## 🔬 Análisis de Complejidad
Algoritmo	Complejidad Teórica	Observado Experimentalmente
Dijkstra	O((V+E) log V)	-
A*	O((V+E) log V)	-
Bidireccional	O((V+E) log V)	-
## 🎮 Características de la Interfaz
Generación de grafos en tiempo real

Selección interactiva de nodos origen y destino

Visualización de rutas con pyvis

Comparación side-by-side de algoritmos

Exportación de resultados a CSV

## 🤝 Contribuciones
Este proyecto es académico. Para sugerencias o issues, por favor contactar a los desarrolladores.

## 📜 Licencia
Este proyecto es con fines educativos. Desarrollado para la clase de Matemáticas Discretas, Otoño 2025.
