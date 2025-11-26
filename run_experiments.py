"""
Integrador Sencillo - Prueba de Funcionalidad
Versión Simplificada y Robusta
"""

import os
import sys
import matplotlib.pyplot as plt

# Configuración robusta del path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)
sys.path.insert(0, current_dir)

# Importaciones directas desde los módulos
try:
    from algorithms import PathAlgorithms
    from experiment_runner import ejecutar_todos_los_casos, generar_csv_resultados, calcular_estadisticas
    from graph_creator import crear_grafo, validar_grafo
    print("✅ Todas las importaciones funcionaron correctamente")
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    sys.exit(1)


def crear_estructura_carpetas():
    """Crea la estructura de carpetas necesaria"""
    carpetas = ['data', 'results', 'docs', 'tests']
    for carpeta in carpetas:
        os.makedirs(carpeta, exist_ok=True)
    print("✅ Estructura de carpetas creada")


def prueba_super_basica():
    """Prueba mínima para verificar que todo funciona"""
    print("🧪 PRUEBA SUPER BÁSICA")
    print("=" * 40)
    
    try:
        # Crear grafo mínimo
        grafo = crear_grafo(10, 50, 20)
        print(f"✅ Grafo creado: {grafo.number_of_nodes()} nodos")
        
        # Probar algoritmos
        algoritmos = PathAlgorithms()
        resultado = algoritmos.dijkstra_con_contador(grafo, 0, 9)
        print(f"✅ Dijkstra funcionó: distancia = {resultado['distancia']:.2f}")
        
        return True, grafo
    except Exception as e:
        print(f"❌ Error en prueba básica: {e}")
        return False, None


def main():
    """
    Función principal - Versión simplificada
    """
    print("🚀 INICIANDO PRUEBA DEL SISTEMA (Versión Simplificada)")
    print("=" * 60)

    # Crear estructura de carpetas
    crear_estructura_carpetas()

    # 1. Prueba super básica
    exito, grafo = prueba_super_basica()
    
    if not exito:
        print("❌ La prueba básica falló. Revisa los módulos.")
        return

    # 2. Prueba con experiment_runner
    print("\n🔬 EJECUTANDO EXPERIMENTO PEQUEÑO")
    print("=" * 40)
    
    try:
        # Crear grafo 
        grafo = crear_grafo(30, 100, 25)
        
        # Ejecutar solo 2 casos para prueba rápida
        df_resultados = ejecutar_todos_los_casos(grafo, num_casos=2)
        
        # Guardar resultados
        archivo_resultados = "results/prueba_rapida.csv"
        generar_csv_resultados(df_resultados, archivo_resultados)
        
        # Mostrar estadísticas
        estadisticas = calcular_estadisticas(df_resultados)
        print("Experimento completado")
        print("\nRESULTADOS:")
        print(estadisticas.to_string(index=False))
        
        # Gráfica simple
        plt.figure(figsize=(8, 5))
        algoritmos = df_resultados['algoritmo'].unique()
        tiempos = [df_resultados[df_resultados['algoritmo'] == algo]['tiempo_medido_experimento'].mean() for algo in algoritmos]
        
        plt.bar(algoritmos, tiempos)
        plt.title('Comparación de Tiempos')
        plt.ylabel('Segundos')
        plt.savefig('results/comparacion_tiempos.png')
        plt.close()
        
        print("✅ Gráfica guardada en results/comparacion_tiempos.png")
        print("\n🎯 ¡SISTEMA FUNCIONANDO CORRECTAMENTE!")
        
    except Exception as e:
        print(f"Error en experimento: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()