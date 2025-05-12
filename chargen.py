import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import json
import random
import os
import requests
import threading
import time
from datetime import datetime

class TkinterCustomTheme:
    """Clase para aplicar tema personalizado a Tkinter"""
    
    def __init__(self, root, theme_data):
        self.root = root
        self.colors = theme_data["colors"]
        
        # Configurar estilos
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Usar clam como base
        
        # Configurar colores del tema
        self.configure_styles()
        
        # Configurar opciones globales para los menús desplegables
        self.root.option_add('*TCombobox*Listbox.background', '#d0d0d0')  # Fondo gris claro
        self.root.option_add('*TCombobox*Listbox.foreground', '#000000')  # Texto negro
        self.root.option_add('*TCombobox*Listbox.selectBackground', self.colors["accent"])
        self.root.option_add('*TCombobox*Listbox.selectForeground', '#ffffff')
        
        # Aplicar color de fondo a la ventana principal
        root.configure(bg=self.colors["background"])
    
    def configure_styles(self):
        # Estilo de widget TFrame
        self.style.configure(
            "Custom.TFrame",
            background=self.colors["background"]
        )
        
        # Estilo de widget TLabel
        self.style.configure(
            "Custom.TLabel",
            background=self.colors["background"],
            foreground=self.colors["text"]
        )
        
        # Estilo de widget TLabel para títulos
        self.style.configure(
            "Title.TLabel",
            background=self.colors["background"],
            foreground=self.colors["accent"],
            font=("Helvetica", 14, "bold")
        )
        
        # Estilo de widget TButton
        self.style.configure(
            "Custom.TButton",
            background=self.colors["button"],
            foreground=self.colors["text"],
            borderwidth=1,
            focusthickness=3,
            focuscolor=self.colors["accent"]
        )
        self.style.map(
            "Custom.TButton",
            background=[("active", self.colors["accent"]), ("pressed", self.colors["button_hover"])],
            foreground=[("active", self.colors["text"])]
        )
        
        # Estilo de widget TCombobox
        self.style.configure(
            "Custom.TCombobox",
            fieldbackground=self.colors["secondary_bg"],
            background=self.colors["accent"],
            foreground=self.colors["text"],
            arrowcolor=self.colors["text"],
            borderwidth=1
        )
        
        # Estilo de widget TCheckbutton
        self.style.configure(
            "Custom.TCheckbutton",
            background=self.colors["background"],
            foreground=self.colors["text"]
        )
        
        # Estilo de separador
        self.style.configure(
            "Custom.TSeparator",
            background=self.colors["accent"]
        )
        
        # Estilo de progreso
        self.style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=self.colors["secondary_bg"],
            background=self.colors["accent"],
            borderwidth=0
        )

class PersonajeGenerator:
    """Clase principal para generar personajes ficticios"""
    
    def __init__(self, config_file="config.json"):
        # Cargar configuración
        self.load_config(config_file)
        
        # Cargar datos
        self.load_data(self.config["data_file"])
        
        # Historial de personajes generados
        self.history = []
    
    def load_config(self, config_file):
        """Carga la configuración desde un archivo JSON"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error al cargar configuracion: {e}")
            # Configuración por defecto
            self.config = {
                "app_name": "Generador de Personajes",
                "data_file": "personajes_data.json",
                "settings": {"default_mode": "offline"}
            }
    
    def load_data(self, data_file):
        """Carga los datos desde un archivo JSON"""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            self.data = {"categorias": {}, "profesiones": {}, "motivaciones": []}
    
    def save_history(self):
        """Guarda el historial de personajes generados"""
        if self.config["settings"].get("save_history", False):
            try:
                history_file = self.config["settings"].get("history_file", "historico_personajes.json")
                with open(history_file, 'w', encoding='utf-8') as f:
                    json.dump(self.history, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"Error al guardar historial: {e}")
    
    def generar_nombre_offline(self, genero="aleatorio", estilo="fantasia", incluir_titulo=False):
        """Genera un nombre de personaje usando datos offline"""
        # Determinar género si es aleatorio
        if genero == "aleatorio":
            genero = random.choice(["masculino", "femenino", "neutro"])
        
        # Comprobar que existe la categoría seleccionada
        if estilo not in self.data["categorias"]:
            estilo = "fantasia"  # Fallback a fantasía
        
        # Obtener los datos de la categoría seleccionada
        cat_data = self.data["categorias"][estilo]
        
        # Seleccionar nombre según género
        nombres = cat_data["nombres"].get(genero + "s", [])
        if not nombres:  # Si no hay nombres del género solicitado
            nombres = cat_data["nombres"]["neutros"] if "neutros" in cat_data["nombres"] else []
            if not nombres:  # Si tampoco hay neutros, usar masculinos
                nombres = cat_data["nombres"]["masculinos"]
        
        nombre = random.choice(nombres)
        apellido = random.choice(cat_data["apellidos"]) if "apellidos" in cat_data else ""
        
        # Nombre completo
        nombre_completo = f"{nombre} {apellido}" if apellido else nombre
        
        # Agregar título si se solicita
        if incluir_titulo and "titulos" in cat_data:
            titulos = cat_data["titulos"].get(genero + "s", [])
            if not titulos:
                titulos = cat_data["titulos"].get("neutros", [])
            
            if titulos:
                titulo = random.choice(titulos)
                nombre_completo = f"{nombre_completo} {titulo}"
        
        return nombre_completo
    
    def generar_personaje_offline(self, genero="aleatorio", estilo="fantasia", detallado=False):
        """Genera un personaje completo usando datos offline"""
        # Nombre del personaje
        nombre_completo = self.generar_nombre_offline(genero, estilo, incluir_titulo=False)
        
        # Si solo queremos el nombre, devolvemos
        if not detallado:
            return nombre_completo
        
        # Determinar género si es aleatorio
        if genero == "aleatorio":
            genero = random.choice(["masculino", "femenino", "neutro"])
        
        # Comprobar que existe la categoría seleccionada
        if estilo not in self.data["categorias"]:
            estilo = "fantasia"  # Fallback a fantasía
        
        # Obtener los datos de la categoría seleccionada
        cat_data = self.data["categorias"][estilo]
        
        # Generar título
        titulo = ""
        if "titulos" in cat_data:
            titulos = cat_data["titulos"].get(genero + "s", [])
            if not titulos:
                titulos = cat_data["titulos"].get("neutros", [])
            
            if titulos and random.random() > 0.5:  # 50% de probabilidad de tener título
                titulo = random.choice(titulos)
        
        # Generar profesión
        profesion = ""
        if "profesiones" in self.data and estilo in self.data["profesiones"]:
            profesion = random.choice(self.data["profesiones"][estilo])
        
        # Generar edad apropiada para el contexto
        if estilo == "medieval":
            edad = random.randint(16, 60)
        elif estilo == "moderno":
            edad = random.randint(18, 75)
        else:
            edad = random.randint(20, 500)  # Para fantasía y ciencia ficción
        
        # Generar rasgo distintivo
        rasgo = ""
        if "rasgos" in cat_data:
            rasgo = random.choice(cat_data["rasgos"])
        
        # Generar motivación
        motivacion = ""
        if "motivaciones" in self.data:
            motivacion = random.choice(self.data["motivaciones"])
        
        # Crear objeto de personaje
        personaje = {
            "nombre": nombre_completo,
            "titulo": titulo,
            "edad": edad,
            "profesion": profesion,
            "rasgo": rasgo,
            "motivacion": motivacion,
            "estilo": estilo,
            "genero": genero,
            "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Agregar al historial
        self.history.append(personaje)
        
        return personaje
    
    def generar_personaje_con_ia(self, genero="aleatorio", estilo="fantasia", detallado=False):
        """Genera un personaje usando la API de IA"""
        # Determinar género si es aleatorio
        if genero == "aleatorio":
            genero = random.choice(["masculino", "femenino", "neutro"])
        
        # Comprobar que existe la categoría seleccionada
        if estilo not in self.data["categorias"]:
            estilo = "fantasia"  # Fallback a fantasía
        
        # Obtener la configuración de la API
        api_config = self.config.get("api", {}).get("grok-2-latest", {})
        prompts = self.config.get("api", {}).get("prompts", {})
        
        if not api_config or not api_config.get("api_key"):
            return {"error": "No hay configuracion API disponible"}
        
        # Seleccionar el prompt adecuado
        if detallado:
            prompt_template = prompts.get("personaje_detallado", "")
        else:
            prompt_template = prompts.get("personaje", "")
        
        if not prompt_template:
            return {"error": "No hay prompt definido"}
        
        # Preparar el prompt
        prompt = prompt_template.format(genero=genero, estilo=estilo)
        
        try:
            # Hacer la petición a la API
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_config['api_key']}"
            }
            
            payload = {
                "model": api_config["model"],
                "messages": [{"role": "system", "content": "Eres un asistente que genera nombres y personajes de ficcion."},
                             {"role": "user", "content": prompt}],
                "temperature": 0.8,
                "max_tokens": 500
            }
            
            print(f"Enviando solicitud a API: {api_config['api_base_url']}")
            
            response = requests.post(
                f"{api_config['api_base_url']}/chat/completions",
                headers=headers,
                json=payload
            )
            
            print(f"Estado de respuesta: {response.status_code}")
            
            if response.status_code != 200:
                print(f"Error en API: {response.text}")
                return {"error": f"Error en API ({response.status_code}): {response.text[:100]}..."}
            
            result = response.json()
            
            # Verificar que la respuesta tiene la estructura esperada
            if "choices" not in result or not result["choices"]:
                print(f"Respuesta sin choices: {result}")
                return {"error": "Formato de respuesta inválido"}
            
            content = result["choices"][0].get("message", {}).get("content", "")
            
            if not content:
                return {"error": "Respuesta vacía de la API"}
            
            print(f"Contenido recibido: {content[:50]}...")
            
            if detallado:
                try:
                    # Intentar extraer el JSON de la respuesta
                    content_clean = content
                    if "```json" in content:
                        content_clean = content.split("```json")[1].split("```")[0]
                    elif "```" in content:
                        content_clean = content.split("```")[1].split("```")[0]
                    
                    # Limpiar espacios en blanco al inicio y fin
                    content_clean = content_clean.strip()
                    
                    print(f"Contenido JSON después de limpieza: {content_clean[:50]}...")
                    
                    # Verificar si comienza con una llave para ser un JSON válido
                    if not content_clean.startswith("{"):
                        if "{" in content_clean:
                            # Intentar encontrar el inicio del JSON
                            content_clean = content_clean[content_clean.find("{"):]
                            print(f"Contenido JSON después de buscar llave inicial: {content_clean[:50]}...")
                        else:
                            # No hay JSON válido, construir manualmente
                            raise json.JSONDecodeError("No se encontró estructura JSON", content_clean, 0)
                    
                    # Verificar si termina con una llave para ser un JSON válido
                    if not content_clean.endswith("}"):
                        if "}" in content_clean:
                            # Intentar encontrar el final del JSON
                            content_clean = content_clean[:content_clean.rfind("}")+1]
                            print(f"Contenido JSON después de buscar llave final: {content_clean[:50]}...")
                    
                    # Convertir a JSON
                    try:
                        personaje = json.loads(content_clean)
                    except:
                        # Intento alternativo: extraer propiedades individualmente
                        print("Intento alternativo: extracción manual de propiedades")
                        personaje = {}
                        
                        # Buscar propiedades comunes
                        for prop in ["nombre", "titulo", "edad", "profesion", "descripcion", "motivacion", "rasgo"]:
                            # Buscar "prop": "valor" o "prop": valor
                            prop_pattern = f'"{prop}"\\s*:\\s*"([^"]*)"'
                            prop_pattern2 = f'"{prop}"\\s*:\\s*([^,"\\n]*)'
                            
                            import re
                            # Buscar con comillas (para strings)
                            matches = re.search(prop_pattern, content)
                            if matches:
                                personaje[prop] = matches.group(1)
                            else:
                                # Buscar sin comillas (para números)
                                matches = re.search(prop_pattern2, content)
                                if matches and prop == "edad":
                                    try:
                                        personaje[prop] = int(matches.group(1).strip())
                                    except:
                                        personaje[prop] = matches.group(1).strip()
                                elif matches:
                                    personaje[prop] = matches.group(1).strip()
                        
                        print(f"Propiedades extraídas manualmente: {personaje}")
                    
                    # Verificar campos mínimos necesarios
                    if "nombre" not in personaje or not personaje["nombre"]:
                        # Extraer primera línea como nombre si está vacío
                        primera_linea = content.split("\n")[0].strip() if "\n" in content else content.strip()
                        # Eliminar markdown, caracteres de puntuación y otras decoraciones
                        for prefijo in ["#", "*", "_", "- ", "\"", "nombre:", "Nombre:"]:
                            if primera_linea.startswith(prefijo):
                                primera_linea = primera_linea[len(prefijo):].strip()
                        personaje["nombre"] = primera_linea or "Personaje sin nombre"
                    
                    # Asegurarse de que todas las propiedades esperadas existan
                    for prop in ["titulo", "edad", "profesion", "descripcion", "motivacion", "rasgo"]:
                        if prop not in personaje:
                            if prop == "edad":
                                personaje[prop] = random.randint(20, 50)
                            else:
                                personaje[prop] = ""
                    
                    personaje["estilo"] = estilo
                    personaje["genero"] = genero
                    personaje["fecha_generacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Agregar al historial
                    self.history.append(personaje)
                    return personaje
                except json.JSONDecodeError as e:
                    print(f"Error de decodificación JSON: {e}")
                    print(f"Contenido que falló: {content_clean}")
                    
                    # Intentar crear un personaje básico a partir del texto
                    lineas = content.strip().split("\n")
                    nombre = lineas[0] if lineas else "Personaje sin nombre"
                    # Limpiar posibles caracteres markdown
                    for prefijo in ["#", "*", "_", "- ", "\"", "nombre:", "Nombre:"]:
                        if nombre.startswith(prefijo):
                            nombre = nombre[len(prefijo):].strip()
                    
                    personaje = {
                        "nombre": nombre,
                        "titulo": "",
                        "edad": random.randint(20, 50),
                        "profesion": "",
                        "descripcion": content,
                        "motivacion": "",
                        "rasgo": "",
                        "estilo": estilo,
                        "genero": genero,
                        "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "error_formato": "La respuesta no tenía formato JSON válido"
                    }
                    
                    self.history.append(personaje)
                    return personaje
                except Exception as e:
                    print(f"Error al procesar JSON de IA: {e}")
                    return {
                        "nombre": "Personaje de " + estilo,
                        "descripcion": content,
                        "error": f"Error al procesar respuesta: {str(e)}",
                        "estilo": estilo,
                        "genero": genero,
                        "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
            else:
                # Para respuestas simples (solo nombre)
                nombre = content.strip()
                return nombre
            
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return {"error": f"Error de conexión: {str(e)}"}
        except Exception as e:
            print(f"Error general: {e}")
            return {"error": f"Error inesperado: {str(e)}"}

class App:
    """Clase principal de la aplicación con interfaz Tkinter"""
    
    def __init__(self, root):
        self.root = root
        
        # Cargar configuración
        self.load_config()
        
        # Inicializar generador de personajes
        self.generator = PersonajeGenerator(config_file="config.json")
        
        # Configurar la ventana principal
        self.setup_window()
        
        # Aplicar tema personalizado
        self.theme = TkinterCustomTheme(root, self.config["theme"])
        
        # Crear interfaz
        self.create_ui()
        
        # Estado de generación
        self.generating = False
    
    def load_config(self):
        """Carga la configuración desde un archivo JSON"""
        try:
            with open("config.json", 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"Error al cargar configuracion: {e}")
            # Configuración por defecto
            self.config = {
                "app_name": "Generador de Personajes",
                "theme": {
                    "colors": {
                        "background": "#282828",
                        "secondary_bg": "#3c3c3c",
                        "accent": "#ff6c37",
                        "text": "#f8f8f8",
                        "text_secondary": "#cccccc",
                        "button": "#505050",
                        "button_hover": "#656565"
                    }
                },
                "settings": {"default_mode": "offline"}
            }
    
    def setup_window(self):
        """Configura la ventana principal"""
        app_name = self.config.get("app_name", "Generador de Personajes")
        self.root.title(app_name)
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        
        # Configurar color de fondo
        bg_color = self.config.get("theme", {}).get("colors", {}).get("background", "#282828")
        self.root.configure(bg=bg_color)
        
        # Configurar para que los widgets se expandan con la ventana
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def create_ui(self):
        """Crea la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.root, style="Custom.TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        app_name = self.config.get("app_name", "Generador de Personajes")
        title_label = ttk.Label(
            main_frame, 
            text=app_name, 
            style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, pady=(0, 10), sticky="w")
        
        # Contenedor de pestañas
        self.tab_control = ttk.Notebook(main_frame)
        self.tab_control.grid(row=1, column=0, sticky="nsew")
        
        # Pestaña de generación
        self.tab_generate = ttk.Frame(self.tab_control, style="Custom.TFrame")
        self.tab_history = ttk.Frame(self.tab_control, style="Custom.TFrame")
        
        self.tab_control.add(self.tab_generate, text="Generador")
        self.tab_control.add(self.tab_history, text="Historial")
        
        self.tab_generate.columnconfigure(0, weight=1)
        self.tab_generate.rowconfigure(2, weight=1)
        
        self.tab_history.columnconfigure(0, weight=1)
        self.tab_history.rowconfigure(1, weight=1)
        
        # Configurar pestaña de generación
        self.setup_generator_tab()
        
        # Configurar pestaña de historial
        self.setup_history_tab()
        
        # Barra de estado
        status_frame = ttk.Frame(main_frame, style="Custom.TFrame")
        status_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        status_frame.columnconfigure(1, weight=1)
        
        # Etiqueta de estado
        self.status_label = ttk.Label(
            status_frame, 
            text="Listo", 
            style="Custom.TLabel"
        )
        self.status_label.grid(row=0, column=0, sticky="w")
        
        # Barra de progreso
        self.progress = ttk.Progressbar(
            status_frame, 
            style="Custom.Horizontal.TProgressbar",
            mode="indeterminate", 
            length=200
        )
        self.progress.grid(row=0, column=1, sticky="e", padx=(10, 0))
        self.progress.grid_remove()  # Ocultar inicialmente
    
    def setup_generator_tab(self):
        """Configura la pestaña de generación"""
        # Frame de opciones
        options_frame = ttk.Frame(self.tab_generate, style="Custom.TFrame")
        options_frame.grid(row=0, column=0, sticky="ew", pady=(10, 10))
        options_frame.columnconfigure(1, weight=1)
        options_frame.columnconfigure(3, weight=1)
        options_frame.columnconfigure(5, weight=1)
        
        # Etiquetas y controles
        ttk.Label(options_frame, text="Modo:", style="Custom.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 5))
        
        self.mode_var = tk.StringVar(value=self.config["settings"].get("default_mode", "offline"))
        mode_combo = ttk.Combobox(
            options_frame, 
            textvariable=self.mode_var,
            values=["offline", "ia"],
            state="readonly",
            style="Custom.TCombobox",
            width=10
        )
        mode_combo.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        mode_combo.config(foreground='#000000')  # Texto negro para el valor seleccionado
        
        ttk.Label(options_frame, text="Género:", style="Custom.TLabel").grid(row=0, column=2, sticky="w", padx=(10, 5))
        
        self.gender_var = tk.StringVar(value=self.config["settings"].get("default_gender", "aleatorio"))
        gender_combo = ttk.Combobox(
            options_frame, 
            textvariable=self.gender_var,
            values=["aleatorio", "masculino", "femenino", "neutro"],
            state="readonly",
            style="Custom.TCombobox",
            width=10
        )
        gender_combo.grid(row=0, column=3, sticky="ew", padx=(0, 10))
        gender_combo.config(foreground='#000000')  # Texto negro para el valor seleccionado
        
        ttk.Label(options_frame, text="Estilo:", style="Custom.TLabel").grid(row=0, column=4, sticky="w", padx=(10, 5))
        
        self.style_var = tk.StringVar(value=self.config["settings"].get("default_style", "fantasia"))
        style_combo = ttk.Combobox(
            options_frame, 
            textvariable=self.style_var,
            values=["fantasia", "ciencia_ficcion", "medieval", "moderno"],
            state="readonly",
            style="Custom.TCombobox",
            width=12
        )
        style_combo.grid(row=0, column=5, sticky="ew")
        style_combo.config(foreground='#000000')  # Texto negro para el valor seleccionado
        
        # Frame de opciones adicionales
        more_options_frame = ttk.Frame(self.tab_generate, style="Custom.TFrame")
        more_options_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        
        # Opciones adicionales
        self.detailed_var = tk.BooleanVar(value=True)
        detailed_check = ttk.Checkbutton(
            more_options_frame, 
            text="Generar personaje detallado",
            variable=self.detailed_var,
            style="Custom.TCheckbutton"
        )
        detailed_check.grid(row=0, column=0, sticky="w")
        
        self.multi_var = tk.BooleanVar(value=False)
        multi_check = ttk.Checkbutton(
            more_options_frame, 
            text="Generar múltiples",
            variable=self.multi_var,
            style="Custom.TCheckbutton",
            command=self.toggle_multi_options
        )
        multi_check.grid(row=0, column=1, sticky="w", padx=(20, 0))
        
        # Opciones para generación múltiple (inicialmente ocultas)
        self.multi_options_frame = ttk.Frame(more_options_frame, style="Custom.TFrame")
        self.multi_options_frame.grid(row=0, column=2, sticky="w", padx=(10, 0))
        self.multi_options_frame.grid_remove()  # Ocultar inicialmente
        
        ttk.Label(self.multi_options_frame, text="Cantidad:", style="Custom.TLabel").grid(row=0, column=0, sticky="w")
        
        self.quantity_var = tk.StringVar(value="5")
        quantity_spinbox = ttk.Spinbox(
            self.multi_options_frame, 
            from_=1, 
            to=50, 
            textvariable=self.quantity_var,
            width=5
        )
        quantity_spinbox.grid(row=0, column=1, sticky="w", padx=(5, 0))
        
        # Frame para el botón de generación
        button_frame = ttk.Frame(more_options_frame, style="Custom.TFrame")
        button_frame.grid(row=0, column=3, sticky="e", padx=(0, 0))
        more_options_frame.columnconfigure(3, weight=1)
        
        # Botón de generación
        self.generate_button = ttk.Button(
            button_frame,
            text="Generar",
            style="Custom.TButton",
            command=self.generate_character
        )
        self.generate_button.grid(row=0, column=0, sticky="e")
        
        # Frame de resultados
        results_frame = ttk.Frame(self.tab_generate, style="Custom.TFrame")
        results_frame.grid(row=2, column=0, sticky="nsew")
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Área de texto para mostrar los resultados
        self.result_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            bg=self.config["theme"]["colors"]["secondary_bg"],
            fg=self.config["theme"]["colors"]["text"],
            insertbackground=self.config["theme"]["colors"]["text"],
            font=("Consolas", 10),
            borderwidth=1,
            relief=tk.FLAT
        )
        self.result_text.grid(row=0, column=0, sticky="nsew")
        
        # Botones de acciones
        actions_frame = ttk.Frame(self.tab_generate, style="Custom.TFrame")
        actions_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        
        # Botón para copiar al portapapeles
        self.copy_button = ttk.Button(
            actions_frame,
            text="Copiar",
            style="Custom.TButton",
            command=self.copy_to_clipboard
        )
        self.copy_button.grid(row=0, column=0, sticky="w")
        
        # Botón para guardar en archivo
        self.save_button = ttk.Button(
            actions_frame,
            text="Guardar",
            style="Custom.TButton",
            command=self.save_to_file
        )
        self.save_button.grid(row=0, column=1, sticky="w", padx=(10, 0))
        
        # Botón para limpiar
        self.clear_button = ttk.Button(
            actions_frame,
            text="Limpiar",
            style="Custom.TButton",
            command=self.clear_results
        )
        self.clear_button.grid(row=0, column=2, sticky="w", padx=(10, 0))
    
    def setup_history_tab(self):
        """Configura la pestaña de historial"""
        # Etiqueta
        ttk.Label(self.tab_history, text="Personajes generados:", style="Custom.TLabel").grid(row=0, column=0, sticky="w", pady=(10, 5))
        
        # Lista de personajes
        self.history_text = scrolledtext.ScrolledText(
            self.tab_history,
            wrap=tk.WORD,
            bg=self.config["theme"]["colors"]["secondary_bg"],
            fg=self.config["theme"]["colors"]["text"],
            insertbackground=self.config["theme"]["colors"]["text"],
            font=("Consolas", 10),
            borderwidth=1,
            relief=tk.FLAT
        )
        self.history_text.grid(row=1, column=0, sticky="nsew")
        
        # Botones de acciones
        history_actions_frame = ttk.Frame(self.tab_history, style="Custom.TFrame")
        history_actions_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        
        # Botón para refrescar historial
        self.refresh_button = ttk.Button(
            history_actions_frame,
            text="Refrescar",
            style="Custom.TButton",
            command=self.refresh_history
        )
        self.refresh_button.grid(row=0, column=0, sticky="w")
        
        # Botón para exportar historial
        self.export_button = ttk.Button(
            history_actions_frame,
            text="Exportar",
            style="Custom.TButton",
            command=self.export_history
        )
        self.export_button.grid(row=0, column=1, sticky="w", padx=(10, 0))
        
        # Botón para limpiar historial
        self.clear_history_button = ttk.Button(
            history_actions_frame,
            text="Limpiar historial",
            style="Custom.TButton",
            command=self.clear_history
        )
        self.clear_history_button.grid(row=0, column=2, sticky="w", padx=(10, 0))
    
    def toggle_multi_options(self):
        """Muestra u oculta las opciones de generación múltiple"""
        if self.multi_var.get():
            self.multi_options_frame.grid()
        else:
            self.multi_options_frame.grid_remove()
    
    def update_status(self, message):
        """Actualiza el mensaje de estado"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def start_progress(self):
        """Inicia la barra de progreso"""
        self.progress.grid()
        self.progress.start(10)
        self.root.update_idletasks()
    
    def stop_progress(self):
        """Detiene la barra de progreso"""
        self.progress.stop()
        self.progress.grid_remove()
        self.root.update_idletasks()
    
    def generate_character(self):
        """Genera un personaje o múltiples personajes"""
        if self.generating:
            return
        
        self.generating = True
        self.generate_button.config(state="disabled")
        self.clear_results()
        
        # Obtener parámetros
        mode = self.mode_var.get()
        gender = self.gender_var.get()
        style = self.style_var.get()
        detailed = self.detailed_var.get()
        multi = self.multi_var.get()
        
        try:
            quantity = int(self.quantity_var.get())
            if quantity < 1:
                quantity = 1
            elif quantity > 50:
                quantity = 50
        except:
            quantity = 5
        
        # Actualizar la interfaz para mostrar estado
        self.update_status("Generando personaje(s)...")
        self.start_progress()
        
        # Iniciar generación en un hilo para no bloquear la interfaz
        thread = threading.Thread(
            target=self._generate_in_thread,
            args=(mode, gender, style, detailed, multi, quantity)
        )
        thread.daemon = True
        thread.start()
    
    def _generate_in_thread(self, mode, gender, style, detailed, multi, quantity):
        """Genera personajes en un hilo separado"""
        try:
            results = []
            
            if multi:
                self.result_text.insert(tk.END, f"Generando {quantity} personajes...\n\n")
                self.result_text.update_idletasks()
                
                for i in range(quantity):
                    try:
                        if mode == "offline":
                            result = self.generator.generar_personaje_offline(gender, style, detailed)
                        else:  # mode == "ia"
                            result = self.generator.generar_personaje_con_ia(gender, style, detailed)
                        
                        results.append(result)
                        
                        # Mostrar progreso
                        if detailed and isinstance(result, dict) and "nombre" in result:
                            nombre = result.get("nombre", "Sin nombre")
                            self.result_text.insert(tk.END, f"{i+1}. {nombre}\n")
                        elif isinstance(result, dict) and "error" in result:
                            self.result_text.insert(tk.END, f"{i+1}. Error: {result['error']}\n")
                        else:
                            self.result_text.insert(tk.END, f"{i+1}. {result}\n")
                        
                        self.result_text.see(tk.END)
                        self.result_text.update_idletasks()
                        
                        # Pequeña pausa para no saturar la API
                        if mode == "ia" and i < quantity - 1:
                            time.sleep(1)
                    except Exception as e:
                        error_msg = f"Error en personaje {i+1}: {str(e)}"
                        print(error_msg)
                        self.result_text.insert(tk.END, f"{error_msg}\n")
                        results.append({"error": str(e), "nombre": f"Error en personaje {i+1}"})
            else:
                try:
                    if mode == "offline":
                        result = self.generator.generar_personaje_offline(gender, style, detailed)
                    else:  # mode == "ia"
                        result = self.generator.generar_personaje_con_ia(gender, style, detailed)
                    
                    results.append(result)
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    print(error_msg)
                    results.append({"error": str(e), "nombre": "Error en personaje"})
            
            # Mostrar resultados completos
            self.result_text.delete(1.0, tk.END)
            
            for i, result in enumerate(results):
                if detailed and isinstance(result, dict) and not "error" in result:
                    # Formato para personaje detallado
                    self.result_text.insert(tk.END, f"{'=' * 40}\n")
                    self.result_text.insert(tk.END, f"PERSONAJE {i+1 if multi else ''}\n")
                    self.result_text.insert(tk.END, f"{'=' * 40}\n\n")
                    
                    self.result_text.insert(tk.END, f"Nombre: {result.get('nombre', 'Sin nombre')}\n")
                    
                    if result.get('titulo'):
                        self.result_text.insert(tk.END, f"Título: {result['titulo']}\n")
                    
                    self.result_text.insert(tk.END, f"Edad: {result.get('edad', 'Desconocida')}\n")
                    
                    if result.get('profesion'):
                        self.result_text.insert(tk.END, f"Profesión: {result['profesion']}\n")
                    
                    if result.get('rasgo'):
                        self.result_text.insert(tk.END, f"Rasgo distintivo: {result['rasgo']}\n")
                    
                    if result.get('motivacion'):
                        self.result_text.insert(tk.END, f"Motivación: {result['motivacion']}\n")
                    
                    # Si hay descripción (generada por IA)
                    if result.get('descripcion'):
                        self.result_text.insert(tk.END, f"\nDescripción: {result['descripcion']}\n")
                    
                    # Si hubo un error de formato pero se logró recuperar
                    if result.get('error_formato'):
                        self.result_text.insert(tk.END, f"\nNota: {result['error_formato']}\n")
                    
                    self.result_text.insert(tk.END, f"\n")
                else:
                    # Formato simple o error
                    if isinstance(result, dict) and "error" in result:
                        if multi:
                            self.result_text.insert(tk.END, f"{i+1}. Error: {result['error']}\n\n")
                        else:
                            self.result_text.insert(tk.END, f"Error: {result['error']}\n\n")
                            # Mostrar respuesta cruda si está disponible
                            if result.get('descripcion'):
                                self.result_text.insert(tk.END, f"Respuesta recibida:\n{result['descripcion']}\n\n")
                    else:
                        if multi:
                            self.result_text.insert(tk.END, f"{i+1}. {result}\n")
                        else:
                            self.result_text.insert(tk.END, f"{result}\n")
            
            # Guardar historial si está habilitado
            self.generator.save_history()
            
            # Actualizar la pestaña de historial
            if self.tab_control.index("current") == 1:  # Si estamos en la pestaña de historial
                self.refresh_history()
            
            # Mostrar mensaje de finalización
            self.update_status(f"Generados {len(results)} personaje(s)")
            
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"Error durante la generación: {str(e)}")
            print(f"Detalles: {error_detail}")
            self.result_text.insert(tk.END, f"Error durante la generación: {str(e)}\n")
            self.result_text.insert(tk.END, f"Detalles del error:\n{error_detail}\n")
            self.update_status(f"Error: {str(e)}")
        finally:
            self.stop_progress()
            self.generate_button.config(state="normal")
            self.generating = False
    
    def copy_to_clipboard(self):
        """Copia el contenido del área de resultados al portapapeles"""
        text = self.result_text.get(1.0, tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.update_status("Copiado al portapapeles")
    
    def save_to_file(self):
        """Guarda el contenido del área de resultados a un archivo"""
        text = self.result_text.get(1.0, tk.END).strip()
        if not text:
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            title="Guardar personaje(s)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.update_status(f"Guardado en {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def clear_results(self):
        """Limpia el área de resultados"""
        self.result_text.delete(1.0, tk.END)
        self.update_status("Listo")
    
    def refresh_history(self):
        """Actualiza la lista de historial"""
        self.history_text.delete(1.0, tk.END)
        
        if not self.generator.history:
            self.history_text.insert(tk.END, "No hay personajes en el historial.")
            return
        
        for i, personaje in enumerate(reversed(self.generator.history), 1):
            self.history_text.insert(tk.END, f"{'=' * 40}\n")
            self.history_text.insert(tk.END, f"PERSONAJE {i} - {personaje.get('fecha_generacion', 'Fecha desconocida')}\n")
            self.history_text.insert(tk.END, f"{'=' * 40}\n\n")
            
            self.history_text.insert(tk.END, f"Nombre: {personaje.get('nombre', 'Sin nombre')}\n")
            
            if personaje.get('titulo'):
                self.history_text.insert(tk.END, f"Título: {personaje['titulo']}\n")
            
            if 'edad' in personaje:
                self.history_text.insert(tk.END, f"Edad: {personaje['edad']}\n")
            
            if personaje.get('profesion'):
                self.history_text.insert(tk.END, f"Profesión: {personaje['profesion']}\n")
            
            if personaje.get('rasgo'):
                self.history_text.insert(tk.END, f"Rasgo distintivo: {personaje['rasgo']}\n")
            
            if personaje.get('motivacion'):
                self.history_text.insert(tk.END, f"Motivación: {personaje['motivacion']}\n")
            
            if personaje.get('descripcion'):
                self.history_text.insert(tk.END, f"\nDescripción: {personaje['descripcion']}\n")
            
            self.history_text.insert(tk.END, f"\nGénero: {personaje.get('genero', 'No especificado')}\n")
            self.history_text.insert(tk.END, f"Estilo: {personaje.get('estilo', 'No especificado')}\n")
            
            self.history_text.insert(tk.END, f"\n\n")
    
    def export_history(self):
        """Exporta el historial a un archivo JSON"""
        if not self.generator.history:
            messagebox.showinfo("Información", "No hay personajes en el historial para exportar.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
            title="Exportar historial"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.generator.history, f, ensure_ascii=False, indent=2)
                self.update_status(f"Historial exportado a {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def clear_history(self):
        """Limpia el historial de personajes"""
        if not self.generator.history:
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de borrar todo el historial?"):
            self.generator.history = []
            self.generator.save_history()
            self.refresh_history()
            self.update_status("Historial borrado")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()