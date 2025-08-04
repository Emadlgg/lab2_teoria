# Simulador de Autómata Finito Determinista (AFD)

Un simulador completo e interactivo de Autómatas Finitos Deterministas implementado en Python, con soporte para múltiples formatos de archivo y una interfaz de línea de comandos fácil de usar.

## 📋 Características

- ✅ **Simulación completa de AFD** con todas las funciones fundamentales
- ✅ **Interfaz interactiva** con menú de opciones
- ✅ **Múltiples formatos de entrada**: JSON, YAML, XML
- ✅ **Creación manual de AFDs** paso a paso
- ✅ **Ejemplos predefinidos** para aprendizaje
- ✅ **Validación robusta** de entrada y transiciones
- ✅ **Prueba interactiva** de cadenas

## 🚀 Funciones Implementadas

### Funciones Core del AFD

- **`transition(q, a)`**: Función de transición δ(q,a)
- **`final_state(q, w)`**: Estado final después de procesar cadena w
- **`derivation(q, w)`**: Secuencia de transiciones para cadena w  
- **`accepted(q, w, F)`**: Verificación de aceptación de cadenas

### Características Adicionales

- Carga desde archivos estructurados (JSON, YAML, XML)
- Creación interactiva de AFDs
- Validación de símbolos y transiciones
- Manejo de errores robusto

## 📦 Instalación

### Requisitos

- Python 3.6+
- PyYAML (para soporte YAML)

### Instalación de dependencias

```bash
pip install pyyaml
```

### Clonar el repositorio

```bash
git clone https://github.com/Emadlgg/lab2_teoria.git
cd lab2_teoria
```

## 🎯 Uso

### Ejecución básica

```bash
python lab2.py
```

### Menú interactivo

El programa presenta un menú con las siguientes opciones:

```
==========================================================
          SIMULADOR DE AUTÓMATA FINITO DETERMINISTA
==========================================================
1. Ver ejemplos predefinidos
2. Cargar AFD desde archivo
3. Crear AFD manualmente
4. Crear archivos de ejemplo
5. Probar cadenas en el AFD actual
6. Ver información del AFD actual
0. Salir
```

## 📖 Ejemplos de Uso

### 1. Usando ejemplos predefinidos

El programa incluye dos AFDs de ejemplo:
- **AFD 1**: Acepta cadenas sobre {0,1} que terminan en '01'
- **AFD 2**: Acepta cadenas sobre {a,b} con número par de 'a's

### 2. Cargar AFD desde archivo

#### Formato JSON
```json
{
  "Q": ["q0", "q1", "q2"],
  "Sigma": ["0", "1"],
  "q0": "q0",
  "F": ["q2"],
  "delta": [
    ["q0", "0", "q1"],
    ["q0", "1", "q0"],
    ["q1", "0", "q1"],
    ["q1", "1", "q2"],
    ["q2", "0", "q1"],
    ["q2", "1", "q0"]
  ]
}
```

#### Formato YAML
```yaml
Q:
  - q0
  - q1
  - q2
Sigma:
  - '0'
  - '1'
q0: q0
F:
  - q2
delta:
  - [q0, '0', q1]
  - [q0, '1', q0]
  - [q1, '0', q1]
  - [q1, '1', q2]
  - [q2, '0', q1]
  - [q2, '1', q0]
```

#### Formato XML
```xml
<?xml version="1.0" encoding="UTF-8"?>
<AFD>
    <Q>
        <state>q0</state>
        <state>q1</state>
        <state>q2</state>
    </Q>
    <Sigma>
        <symbol>0</symbol>
        <symbol>1</symbol>
    </Sigma>
    <q0>q0</q0>
    <F>
        <state>q2</state>
    </F>
    <delta>
        <transition>
            <from>q0</from>
            <symbol>0</symbol>
            <to>q1</to>
        </transition>
        <!-- más transiciones... -->
    </delta>
</AFD>
```

### 3. Uso programático

```python
from afd_simulator import AFD

# Definir AFD
Q = ['q0', 'q1', 'q2']
Sigma = ['0', '1']
q0 = 'q0'
F = ['q2']
delta = [
    ('q0', '0', 'q1'),
    ('q0', '1', 'q0'),
    ('q1', '1', 'q2')
]

# Crear AFD
afd = AFD(Q, Sigma, q0, F, delta)

# Probar cadenas
print(afd.accepted('q0', '01'))  # True
print(afd.final_state('q0', '01'))  # 'q2'
print(afd.derivation('q0', '01'))  # [('q0', '0', 'q1'), ('q1', '1', 'q2')]
```

## 🔧 Estructura del Proyecto

```
simulador-afd/
│
├── afd_simulator.py          # Programa principal
├── README.md                 # Este archivo
├── afd_ejemplo.json         # Archivo de ejemplo (generado)
├── afd_ejemplo.yaml         # Archivo de ejemplo (generado)
└── afd_ejemplo.xml          # Archivo de ejemplo (generado)
```

## 📚 Documentación de la API

### Clase `AFD`

#### Constructor
```python
AFD(Q, Sigma, q0, F, delta)
```

**Parámetros:**
- `Q`: Lista de estados
- `Sigma`: Lista de símbolos del alfabeto
- `q0`: Estado inicial
- `F`: Lista de estados de aceptación
- `delta`: Función de transición (lista de tuplas o diccionario)

#### Métodos

- **`transition(q, a)`**: Devuelve el estado resultante de δ(q,a)
- **`final_state(q, w)`**: Estado final después de procesar w desde q
- **`derivation(q, w)`**: Lista de transiciones para procesar w
- **`accepted(q, w, F=None)`**: True si w es aceptada, False en caso contrario

### Funciones de utilidad

- **`load_afd_from_json(filename)`**: Carga AFD desde archivo JSON
- **`load_afd_from_yaml(filename)`**: Carga AFD desde archivo YAML
- **`load_afd_from_xml(filename)`**: Carga AFD desde archivo XML

## 🧪 Ejemplos de Prueba

### AFD que acepta cadenas terminadas en '01'

```python
# Cadenas aceptadas: "01", "001", "101", "1101"
# Cadenas rechazadas: "10", "11", "00", "1"
```

### AFD que acepta número par de 'a's

```python
# Cadenas aceptadas: "", "aa", "bb", "baba"
# Cadenas rechazadas: "a", "aaa", "aba"
```
