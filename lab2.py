import json
import yaml
import xml.etree.ElementTree as ET

class AFD:
    def __init__(self, Q, Sigma, q0, F, delta):
        """
        Inicializa el AFD con los componentes dados
        
        Args:
            Q: lista de estados
            Sigma: lista de símbolos del alfabeto
            q0: estado inicial
            F: lista de estados de aceptación
            delta: función de transición (diccionario o lista de tuplas)
        """
        self.Q = Q
        self.Sigma = Sigma
        self.q0 = q0
        self.F = F
        
        # Convertir delta a diccionario si es una lista de tuplas
        if isinstance(delta, list):
            self.delta = {}
            for (q, a, q_prime) in delta:
                self.delta[(q, a)] = q_prime
        else:
            self.delta = delta
    
    def transition(self, q, a):
        """
        Función de transición δ(q, a)
        
        Args:
            q: estado actual
            a: símbolo de entrada
            
        Returns:
            El estado resultante después de la transición, o None si no existe
        """
        return self.delta.get((q, a), None)
    
    def final_state(self, q, w):
        """
        Devuelve el estado final después de leer la cadena w desde el estado q
        
        Args:
            q: estado inicial
            w: cadena de entrada
            
        Returns:
            El estado final después de procesar toda la cadena
        """
        current_state = q
        
        for symbol in w:
            if symbol not in self.Sigma:
                raise ValueError(f"Símbolo '{symbol}' no está en el alfabeto")
            
            next_state = self.transition(current_state, symbol)
            if next_state is None:
                raise ValueError(f"No hay transición definida desde {current_state} con símbolo '{symbol}'")
            
            current_state = next_state
        
        return current_state
    
    def derivation(self, q, w):
        """
        Devuelve la derivación (secuencia de transiciones) de la cadena w desde el estado q
        
        Args:
            q: estado inicial
            w: cadena de entrada
            
        Returns:
            Lista de tuplas (estado_actual, símbolo, estado_siguiente)
        """
        derivation_steps = []
        current_state = q
        
        for symbol in w:
            if symbol not in self.Sigma:
                raise ValueError(f"Símbolo '{symbol}' no está en el alfabeto")
            
            next_state = self.transition(current_state, symbol)
            if next_state is None:
                raise ValueError(f"No hay transición definida desde {current_state} con símbolo '{symbol}'")
            
            derivation_steps.append((current_state, symbol, next_state))
            current_state = next_state
        
        return derivation_steps
    
    def accepted(self, q, w, F=None):
        """
        Determina si la cadena w es aceptada por el autómata partiendo desde el estado q
        
        Args:
            q: estado inicial
            w: cadena de entrada
            F: estados de aceptación (opcional, usa self.F por defecto)
            
        Returns:
            True si la cadena es aceptada, False en caso contrario
        """
        if F is None:
            F = self.F
        
        try:
            final_state = self.final_state(q, w)
            return final_state in F
        except ValueError:
            return False
    
    def __str__(self):
        """Representación en cadena del AFD"""
        return f"""AFD:
  Estados (Q): {self.Q}
  Alfabeto (Σ): {self.Sigma}
  Estado inicial (q0): {self.q0}
  Estados de aceptación (F): {self.F}
  Transiciones (δ): {dict(self.delta)}"""

def load_afd_from_json(filename):
    """Carga un AFD desde un archivo JSON"""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return AFD(
        Q=data['Q'],
        Sigma=data['Sigma'],
        q0=data['q0'],
        F=data['F'],
        delta=data['delta']
    )

def load_afd_from_yaml(filename):
    """Carga un AFD desde un archivo YAML"""
    with open(filename, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    return AFD(
        Q=data['Q'],
        Sigma=data['Sigma'],
        q0=data['q0'],
        F=data['F'],
        delta=data['delta']
    )

def load_afd_from_xml(filename):
    """Carga un AFD desde un archivo XML"""
    tree = ET.parse(filename)
    root = tree.getroot()
    
    # Parsear estados
    Q = [state.text for state in root.find('Q').findall('state')]
    
    # Parsear alfabeto
    Sigma = [symbol.text for symbol in root.find('Sigma').findall('symbol')]
    
    # Parsear estado inicial
    q0 = root.find('q0').text
    
    # Parsear estados de aceptación
    F = [state.text for state in root.find('F').findall('state')]
    
    # Parsear transiciones
    delta = {}
    for transition in root.find('delta').findall('transition'):
        from_state = transition.find('from').text
        symbol = transition.find('symbol').text
        to_state = transition.find('to').text
        delta[(from_state, symbol)] = to_state
    
    return AFD(Q, Sigma, q0, F, delta)

# Ejemplos de uso
def ejemplo_afd_1():
    """
    AFD que acepta cadenas sobre {0,1} que terminan en '01'
    """
    print("=== EJEMPLO 1: AFD que acepta cadenas que terminan en '01' ===")
    
    Q = ['q0', 'q1', 'q2']
    Sigma = ['0', '1']
    q0 = 'q0'
    F = ['q2']
    
    # Función de transición como lista de tuplas
    delta = [
        ('q0', '0', 'q1'),
        ('q0', '1', 'q0'),
        ('q1', '0', 'q1'),
        ('q1', '1', 'q2'),
        ('q2', '0', 'q1'),
        ('q2', '1', 'q0')
    ]
    
    afd1 = AFD(Q, Sigma, q0, F, delta)
    print(afd1)
    print()
    
    # Probar algunas cadenas
    test_strings = ['01', '001', '101', '1101', '10', '11', '00']
    
    for w in test_strings:
        print(f"Cadena '{w}':")
        print(f"  Estado final: {afd1.final_state(q0, w)}")
        print(f"  Derivación: {afd1.derivation(q0, w)}")
        print(f"  ¿Aceptada?: {afd1.accepted(q0, w)}")
        print()

def ejemplo_afd_2():
    """
    AFD que acepta cadenas sobre {a,b} con número par de 'a's
    """
    print("=== EJEMPLO 2: AFD que acepta cadenas con número par de 'a's ===")
    
    Q = ['par', 'impar']
    Sigma = ['a', 'b']
    q0 = 'par'
    F = ['par']
    
    # Función de transición como diccionario
    delta = {
        ('par', 'a'): 'impar',
        ('par', 'b'): 'par',
        ('impar', 'a'): 'par',
        ('impar', 'b'): 'impar'
    }
    
    afd2 = AFD(Q, Sigma, q0, F, delta)
    print(afd2)
    print()
    
    # Probar algunas cadenas
    test_strings = ['', 'a', 'aa', 'ab', 'ba', 'aba', 'aab', 'baba']
    
    for w in test_strings:
        print(f"Cadena '{w}':")
        print(f"  Estado final: {afd2.final_state(q0, w)}")
        if w:  # Solo mostrar derivación si la cadena no está vacía
            print(f"  Derivación: {afd2.derivation(q0, w)}")
        print(f"  ¿Aceptada?: {afd2.accepted(q0, w)}")
        print()

# Crear archivos de ejemplo para demostrar la carga desde archivos
def crear_archivos_ejemplo():
    """Crea archivos de ejemplo en diferentes formatos"""
    
    # Ejemplo en JSON
    afd_json = {
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
    
    with open('afd_ejemplo.json', 'w') as f:
        json.dump(afd_json, f, indent=2)
    
    # Ejemplo en YAML
    with open('afd_ejemplo.yaml', 'w') as f:
        yaml.dump(afd_json, f, default_flow_style=False)
    
    # Ejemplo en XML
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
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
        <transition>
            <from>q0</from>
            <symbol>1</symbol>
            <to>q0</to>
        </transition>
        <transition>
            <from>q1</from>
            <symbol>0</symbol>
            <to>q1</to>
        </transition>
        <transition>
            <from>q1</from>
            <symbol>1</symbol>
            <to>q2</to>
        </transition>
        <transition>
            <from>q2</from>
            <symbol>0</symbol>
            <to>q1</to>
        </transition>
        <transition>
            <from>q2</from>
            <symbol>1</symbol>
            <to>q0</to>
        </transition>
    </delta>
</AFD>'''
    
    with open('afd_ejemplo.xml', 'w') as f:
        f.write(xml_content)

def probar_cadenas_interactivo(afd):
    """Permite al usuario probar cadenas de forma interactiva"""
    print(f"\n=== PROBANDO CADENAS EN EL AFD ===")
    print(f"Alfabeto disponible: {afd.Sigma}")
    print("Ingresa cadenas para probar (presiona Enter sin texto para salir):")
    
    while True:
        cadena = input("\nCadena a probar: ").strip()
        if not cadena and input("¿Quieres probar la cadena vacía? (s/n): ").lower() != 's':
            break
            
        try:
            print(f"\nResultados para la cadena '{cadena}':")
            estado_final = afd.final_state(afd.q0, cadena)
            print(f"  Estado final: {estado_final}")
            
            if cadena:  # Solo mostrar derivación si no es cadena vacía
                derivacion = afd.derivation(afd.q0, cadena)
                print(f"  Derivación: {derivacion}")
            
            aceptada = afd.accepted(afd.q0, cadena)
            print(f"  ¿Aceptada?: {'SÍ' if aceptada else 'NO'}")
            
        except ValueError as e:
            print(f"  Error: {e}")

def cargar_afd_desde_archivo():
    """Interfaz para cargar AFD desde archivo"""
    print("\n=== CARGAR AFD DESDE ARCHIVO ===")
    
    while True:
        print("\nFormatos soportados:")
        print("1. JSON (.json)")
        print("2. YAML (.yaml/.yml)")
        print("3. XML (.xml)")
        print("4. Volver al menú principal")
        
        opcion = input("\nSelecciona el formato (1-4): ").strip()
        
        if opcion == '4':
            return None
        elif opcion in ['1', '2', '3']:
            filename = input("Ingresa el nombre del archivo (con extensión): ").strip()
            
            try:
                if opcion == '1':
                    afd = load_afd_from_json(filename)
                elif opcion == '2':
                    afd = load_afd_from_yaml(filename)
                else:  # opcion == '3'
                    afd = load_afd_from_xml(filename)
                
                print(f"\n✓ AFD cargado exitosamente desde {filename}")
                print(afd)
                return afd
                
            except FileNotFoundError:
                print(f"✗ Error: No se encontró el archivo '{filename}'")
            except (json.JSONDecodeError, yaml.YAMLError, ET.ParseError) as e:
                print(f"✗ Error al parsear el archivo: {e}")
            except Exception as e:
                print(f"✗ Error inesperado: {e}")
        else:
            print("Opción no válida. Intenta de nuevo.")

def crear_afd_manual():
    """Interfaz para crear AFD manualmente"""
    print("\n=== CREAR AFD MANUALMENTE ===")
    
    try:
        # Estados
        print("\n1. Definir estados:")
        estados_input = input("Ingresa los estados separados por comas (ej: q0,q1,q2): ").strip()
        Q = [s.strip() for s in estados_input.split(',') if s.strip()]
        
        if not Q:
            print("Error: Debes definir al menos un estado.")
            return None
        
        # Alfabeto
        print("\n2. Definir alfabeto:")
        alfabeto_input = input("Ingresa los símbolos separados por comas (ej: 0,1): ").strip()
        Sigma = [s.strip() for s in alfabeto_input.split(',') if s.strip()]
        
        if not Sigma:
            print("Error: Debes definir al menos un símbolo.")
            return None
        
        # Estado inicial
        print(f"\n3. Estado inicial (estados disponibles: {Q}):")
        q0 = input("Ingresa el estado inicial: ").strip()
        
        if q0 not in Q:
            print(f"Error: '{q0}' no está en la lista de estados.")
            return None
        
        # Estados de aceptación
        print(f"\n4. Estados de aceptación (estados disponibles: {Q}):")
        final_input = input("Ingresa los estados de aceptación separados por comas: ").strip()
        F = [s.strip() for s in final_input.split(',') if s.strip() and s.strip() in Q]
        
        # Función de transición
        print(f"\n5. Función de transición:")
        print("Ingresa las transiciones en formato: estado_origen,símbolo,estado_destino")
        print("Presiona Enter sin texto para terminar.")
        
        delta = []
        transiciones_dict = {}
        
        while True:
            trans_input = input("Transición: ").strip()
            if not trans_input:
                break
                
            try:
                partes = [p.strip() for p in trans_input.split(',')]
                if len(partes) != 3:
                    print("Error: Formato incorrecto. Usa: estado_origen,símbolo,estado_destino")
                    continue
                
                q_from, symbol, q_to = partes
                
                if q_from not in Q:
                    print(f"Error: Estado '{q_from}' no existe.")
                    continue
                if symbol not in Sigma:
                    print(f"Error: Símbolo '{symbol}' no está en el alfabeto.")
                    continue
                if q_to not in Q:
                    print(f"Error: Estado '{q_to}' no existe.")
                    continue
                
                if (q_from, symbol) in transiciones_dict:
                    print(f"Advertencia: Ya existe una transición para ({q_from}, {symbol}). Sobrescribiendo.")
                
                delta.append((q_from, symbol, q_to))
                transiciones_dict[(q_from, symbol)] = q_to
                print(f"✓ Transición agregada: δ({q_from}, {symbol}) = {q_to}")
                
            except Exception as e:
                print(f"Error: {e}")
        
        if not delta:
            print("Advertencia: No se definieron transiciones.")
        
        afd = AFD(Q, Sigma, q0, F, delta)
        print(f"\n✓ AFD creado exitosamente:")
        print(afd)
        return afd
        
    except KeyboardInterrupt:
        print("\nOperación cancelada.")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None

def menu_principal():
    """Menú principal del programa"""
    afd_actual = None
    
    while True:
        print("\n" + "="*60)
        print("          SIMULADOR DE AUTÓMATA FINITO DETERMINISTA")
        print("="*60)
        print("1. Ver ejemplos predefinidos")
        print("2. Cargar AFD desde archivo")
        print("3. Crear AFD manualmente")
        print("4. Crear archivos de ejemplo")
        if afd_actual:
            print("5. Probar cadenas en el AFD actual")
            print("6. Ver información del AFD actual")
        print("0. Salir")
        
        if afd_actual:
            print(f"\nAFD actual cargado: ✓")
        else:
            print(f"\nNo hay AFD cargado")
        
        opcion = input("\nSelecciona una opción: ").strip()
        
        if opcion == '0':
            print("¡Hasta luego!")
            break
            
        elif opcion == '1':
            print("\n¿Qué ejemplo quieres ver?")
            print("1. AFD que acepta cadenas terminadas en '01'")
            print("2. AFD que acepta cadenas con número par de 'a's")
            print("3. Ambos ejemplos")
            
            sub_opcion = input("Selecciona (1-3): ").strip()
            
            if sub_opcion == '1':
                ejemplo_afd_1()
            elif sub_opcion == '2':
                ejemplo_afd_2()
            elif sub_opcion == '3':
                ejemplo_afd_1()
                print("\n" + "="*60 + "\n")
                ejemplo_afd_2()
            else:
                print("Opción no válida.")
                
        elif opcion == '2':
            afd_cargado = cargar_afd_desde_archivo()
            if afd_cargado:
                afd_actual = afd_cargado
                
        elif opcion == '3':
            afd_creado = crear_afd_manual()
            if afd_creado:
                afd_actual = afd_creado
                
        elif opcion == '4':
            print("\n=== CREANDO ARCHIVOS DE EJEMPLO ===")
            crear_archivos_ejemplo()
            print("✓ Archivos creados exitosamente:")
            print("  - afd_ejemplo.json")
            print("  - afd_ejemplo.yaml")
            print("  - afd_ejemplo.xml")
            print("\nPuedes usar estos archivos con la opción 'Cargar AFD desde archivo'")
            
        elif opcion == '5' and afd_actual:
            probar_cadenas_interactivo(afd_actual)
            
        elif opcion == '6' and afd_actual:
            print(f"\n=== INFORMACIÓN DEL AFD ACTUAL ===")
            print(afd_actual)
            
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu_principal()