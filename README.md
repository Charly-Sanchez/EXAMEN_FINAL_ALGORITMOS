# 🏁 Simulador de Carreras de Tortugas - Versión Ultra Moderna

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

## 📋 Descripción

**Simulador de Carreras de Tortugas** es una aplicación gráfica interactiva desarrollada en Python que permite simular carreras de tortugas en diferentes mapas con una interfaz moderna estilo Windows 11. El proyecto combina gráficos `turtle` con una interfaz de usuario avanzada usando `CustomTkinter`.

### ✨ Características Principales

- 🎨 **Interfaz Ultra Moderna**: Diseño dark mode con CustomTkinter
- 🗺️ **3 Mapas Únicos**: Pista Recta Clásica, Óvalo NASCAR y Circuito en S
- 🎨 **Selector de Colores Vibrante**: Paleta de colores con vista previa en tiempo real
- 🐢 **Hasta 6 Tortugas**: Configura de 2 a 6 participantes
- 📊 **Historial de Carreras**: Guarda y visualiza todas las carreras anteriores
- 🏆 **Sistema de Resultados**: Muestra ganador, tiempo y estadísticas
- 🎮 **Nombres Personalizables**: Asigna nombres únicos a cada tortuga
- ⚡ **Efectos Visuales**: Animaciones y efectos especiales durante la carrera

---

## 🎯 Mapas Disponibles

### 1. 🏁 Pista Recta Clásica
- **Complejidad**: Fácil
- **Descripción**: Carrera horizontal directa de izquierda a derecha
- **Características**: Carriles paralelos, ideal para principiantes

### 2. 🏎️ Óvalo NASCAR
- **Complejidad**: Media
- **Descripción**: Circuito ovalado estilo NASCAR con curvas amplias
- **Características**: Curvas suaves, carriles concéntricos

### 3. 🌀 Circuito en S
- **Complejidad**: Alta
- **Descripción**: Pista sinuosa en forma de S doble
- **Características**: Curvas pronunciadas, requiere precisión

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar o Descargar el Proyecto

```bash
git clone https://github.com/Charly-Sanchez/EXAMEN_FINAL_ALGORITMOS.git
```

### Paso 2: Instalar Dependencias

```bash
pip install customtkinter
```

> **Nota**: Los módulos `turtle`, `random`, `datetime`, `json`, `os`, `threading`, `time`, `math` y `tkinter` son parte de la biblioteca estándar de Python.

---

## 📖 Uso

### Ejecución Básica

```bash
python Examen.py
```

### Flujo de Uso

1. **Seleccionar Mapa**: Elige uno de los 3 mapas disponibles con vista previa
2. **Configurar Tortugas**: 
   - Selecciona el número de participantes (2-6)
   - Personaliza nombres
   - Elige colores vibrantes usando la paleta
3. **Actualizar Configuración**: Haz clic en "🔄 Actualizar Configuración"
4. **Iniciar Carrera**: Presiona "🏁 Iniciar Carrera"
5. **Ver Resultados**: Al finalizar, se muestra el ganador y el tiempo
6. **Finalizar**: Usa "🏁 Finalizar Carrera" para volver al menú

---

## 🎮 Controles y Funciones

### Interfaz Principal

| Botón | Función |
|-------|---------|
| 🗺️ **Selector de Mapa** | Vista previa y selección de mapas |
| 🔄 **Actualizar Configuración** | Aplica cambios en tortugas |
| 🏁 **Iniciar Carrera** | Comienza la simulación |
| 🏁 **Finalizar Carrera** | Termina y limpia la carrera actual |
| 📊 **Ver Historial** | Muestra todas las carreras guardadas |
| 🗑️ **Limpiar Historial** | Borra el historial completo |
| ❌ **Salir** | Cierra la aplicación |

### Configuración de Tortugas

- **Campo Nombre**: Ingresa un nombre único para cada tortuga
- **Botón Color**: Vista previa del color actual
- **🎨 Paleta**: Abre selector de colores vibrantes
  - Colores vibrantes predefinidos
  - Paleta extendida de 20 colores
  - Selector avanzado personalizado

---

## 📁 Estructura del Proyecto

```
simulador-carreras-tortugas/
│
├── Examen.py                 # Archivo principal de la aplicación
├── historial_carreras.txt    # Historial de carreras (JSON)
├── test_oval.py              # Prueba del óvalo NASCAR
├── test_s_doble.py           # Prueba del circuito en S
└── README.md                 # Documentación del proyecto
```

---

## 🔧 Arquitectura del Código

### Clase Principal: `CarreraModerna`

```python
class CarreraModerna:
    def __init__(self):
        # Inicialización de variables
        # Definición de colores vibrantes
        # Configuración de mapas disponibles
```

### Métodos Principales

#### Interfaz de Usuario

| Método | Descripción |
|--------|-------------|
| `crear_interfaz_principal()` | Crea la ventana principal con CustomTkinter |
| `crear_selector_mapas()` | Genera el selector de mapas con preview |
| `actualizar_preview_mapa()` | Actualiza vista previa del mapa seleccionado |
| `actualizar_config_tortugas()` | Actualiza configuración dinámica de tortugas |
| `mostrar_paleta_colores()` | Muestra paleta de colores personalizada |

#### Sistema de Pistas

| Método | Descripción |
|--------|-------------|
| `crear_pista_compleja()` | Crea la pista según el mapa seleccionado |
| `dibujar_pista_recta()` | Dibuja pista horizontal clásica |
| `dibujar_pista_ovalo()` | Dibuja circuito ovalado NASCAR |
| `dibujar_pista_s_doble()` | Dibuja circuito sinuoso en S |
| `calcular_puntos_navegacion()` | Calcula rutas de navegación para cada tortuga |

#### Sistema de Carreras

| Método | Descripción |
|--------|-------------|
| `iniciar_carrera()` | Valida y comienza una nueva carrera |
| `crear_tortugas_participantes()` | Crea tortugas con colores y nombres |
| `simular_carrera()` | Lógica principal de simulación de carrera |
| `actualizar_nombres_flotantes()` | Actualiza posición de nombres durante carrera |
| `mostrar_resultado_ganador()` | Muestra resultados con efectos visuales |
| `finalizar_carrera()` | Limpia y resetea la carrera |

#### Sistema de Historial

| Método | Descripción |
|--------|-------------|
| `guardar_resultado_carrera()` | Guarda resultado en archivo JSON |
| `mostrar_historial()` | Muestra ventana con historial completo |
| `limpiar_historial()` | Elimina todos los registros |

---

## 📊 Formato del Historial

El historial se guarda en formato JSON con la siguiente estructura:

```json
{
  "fecha_hora": "2025-11-06 23:12:17",
  "mapa": "Óvalo NASCAR",
  "participantes": [
    {
      "nombre": "Speedy_1",
      "color": "#FF0000",
      "posicion": 1
    }
  ],
  "ganador": {
    "nombre": "Speedy_3",
    "color": "#0000FF",
    "posicion": 3
  },
  "tiempo_carrera": 65.36,
  "num_participantes": 3
}
```

---

## 🎨 Paleta de Colores

### Colores Vibrantes Predefinidos

```python
colores_tortugas = [
    "#FF0000",  # Rojo brillante
    "#00FF00",  # Verde neón
    "#0000FF",  # Azul eléctrico
    "#FFFF00",  # Amarillo brillante
    "#FF00FF",  # Magenta
    "#00FFFF",  # Cyan brillante
    "#FF8000",  # Naranja vibrante
    "#8000FF",  # Púrpura brillante
    "#FF0080",  # Rosa fucsia
    "#00FF80",  # Verde menta
    "#FF6600",  # Naranja fuego
    "#00CCFF",  # Azul cielo
    "#FF3399",  # Rosa intenso
    "#99FF00",  # Lima eléctrico
    "#FF00CC"   # Magenta neón
]
```

---

## 🧪 Pruebas

El proyecto incluye archivos de prueba para validar la navegación en los mapas:

### test_oval.py
Prueba el dibujo y navegación del óvalo NASCAR.

```bash
python test_oval.py
```

### test_s_doble.py
Prueba el cálculo de rutas del circuito en S.

```bash
python test_s_doble.py
```

---

## 🐛 Solución de Problemas

### Error: `ModuleNotFoundError: No module named 'customtkinter'`

**Solución**: Instala CustomTkinter
```bash
pip install customtkinter
```

### La ventana de carrera se cierra inesperadamente

**Causa**: Cierre manual de la ventana turtle durante la carrera.

**Solución**: Usa el botón "🏁 Finalizar Carrera" en la interfaz principal.

### Las tortugas no siguen la pista correctamente

**Causa**: Error en el cálculo de puntos de navegación.

**Solución**: Verifica que el mapa seleccionado coincida con el tipo de pista dibujada.

### Error al guardar historial

**Causa**: Permisos de escritura o archivo corrupto.

**Solución**: 
1. Verifica permisos en la carpeta del proyecto
2. Elimina `historial_carreras.txt` y reinicia

---

## 📈 Estadísticas del Historial

El visor de historial incluye:

- ✅ Total de carreras realizadas
- ⏱️ Tiempo promedio de carreras
- 🏆 Mejor corredor (más victorias)
- 📅 Fecha y hora de cada carrera
- 🗺️ Mapa utilizado
- 👥 Lista completa de participantes

---

## 🎓 Conceptos de Programación Implementados

### Programación Orientada a Objetos (POO)
- Clase `CarreraModerna` encapsula toda la funcionalidad
- Métodos organizados por responsabilidad

### Estructuras de Datos
- **Listas**: Almacenamiento de tortugas, colores, nombres
- **Diccionarios**: Definición de mapas y configuraciones
- **JSON**: Persistencia de datos del historial

### Algoritmos
- **Navegación por puntos**: Cálculo de rutas para cada mapa
- **Simulación aleatoria**: Velocidad variable con efectos especiales
- **Trigonometría**: Cálculo de curvas (óvalos, S, círculos)

### Programación de Interfaces Gráficas
- **CustomTkinter**: Interfaz moderna y responsive
- **Turtle Graphics**: Visualización de carreras
- **Event Handling**: Manejo de eventos de usuario

### Manejo de Archivos
- **Lectura/Escritura JSON**: Persistencia del historial
- **Gestión de rutas**: Uso de `os.path` para compatibilidad

---

## 🔮 Futuras Mejoras

- [ ] Modo multijugador en red
- [ ] Más mapas temáticos (espacio, volcán, playa)
- [ ] Sistema de power-ups durante la carrera
- [ ] Sonidos y música de fondo
- [ ] Exportación de resultados a CSV/PDF
- [ ] Gráficos de estadísticas avanzados
- [ ] Modo torneo con bracket elimination
- [ ] Replay de carreras guardadas

---

## 👨‍💻 Autor

**Desarrollado para**: Curso de Algoritmos - UMG Sistemas Ciclo II

**Fecha**: Noviembre 2025

---


## 🙏 Agradecimientos

- **Python Turtle Graphics**: Por la base de visualización
- **CustomTkinter**: Por la interfaz moderna
- **Comunidad de Python**: Por la documentación y soporte

---

## 🎯 Conclusión

Este simulador demuestra la integración de múltiples conceptos de programación en Python para crear una aplicación interactiva y visualmente atractiva. Es ideal para aprender sobre:

- Gráficos con Turtle
- Interfaces modernas con CustomTkinter
- Manejo de eventos y threading
- Persistencia de datos
- Algoritmos de navegación
- Diseño de software orientado a objetos

**¡Disfruta las carreras! 🏁🐢**

---

**Carlos Armando Sánchez Rodríguez || 1290 - 25 - 2060** 
## *INGENIERIA EN SISTEMAS CICLO II - SEDE DE ANTIGUA GUATEMALA - ALGORITMOS*
