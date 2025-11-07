"""
Simulador de Carreras de Tortugas - Versión Ultra Moderna con CustomTkinter
Desarrollado para el curso de Algoritmos
Características:
- Interfaz gráfica ULTRA MODERNA con CustomTkinter
- Múltiples mapas complejos con vista previa
- Selector de colores con paleta visual vibrante
- Nombres flotantes para cada tortuga
- Historial de carreras
- Diseño moderno estilo Windows 11
"""

import turtle
import random
import datetime
import json
import os
import threading
import time
import math
import customtkinter as ctk
from tkinter import messagebox, colorchooser
import colorsys

class CarreraModerna:
    def __init__(self):
        self.ventana = None
        self.screen = None
        self.tortugas = []
        self.nombres_tortugas = []
        self.labels_nombres = []
        
        # Colores VIBRANTES para las tortugas (NO metálicos)
        self.colores_tortugas = [
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
        
        # Obtener el directorio del script actual
        directorio_actual = os.path.dirname(os.path.abspath(__file__))
        self.archivo_historial = os.path.join(directorio_actual, "historial_carreras.txt")
        
        self.pista_creada = False
        self.carrera_en_progreso = False
        self.mapa_seleccionado = "Pista Recta Clásica"
        
        # Definición de 3 mapas ÚNICOS y diferentes
        self.mapas_disponibles = {
            "Pista Recta Clásica": {
                "descripcion": "Carrera horizontal directa de izquierda a derecha",
                "color_fondo": "#0a0a1a",
                "color_asfalto": "#2c2c3c",
                "complejidad": "Fácil",
                "forma": "recta"
            },
            "Óvalo NASCAR": {
                "descripcion": "Circuito ovalado estilo NASCAR con curvas amplias",
                "color_fondo": "#1a0a0a",
                "color_asfalto": "#3c2c2c",
                "complejidad": "Media",
                "forma": "ovalo"
            },
            "Circuito en S": {
                "descripcion": "Pista sinuosa en forma de S doble",
                "color_fondo": "#0a1a0a",
                "color_asfalto": "#2c3c2c",
                "complejidad": "Alta",
                "forma": "s_doble"
            }
        }
        
    def crear_interfaz_principal(self):
        """Crea la interfaz principal moderna con CustomTkinter"""
        # Configurar tema y apariencia
        ctk.set_appearance_mode("dark")  # Modo oscuro
        ctk.set_default_color_theme("blue")  # Tema azul
        
        self.root = ctk.CTk()
        self.root.title("🏁 Simulador de Carreras de Tortugas - Ultra Moderno")
        self.root.geometry("1200x750")
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título con gradiente visual
        title_label = ctk.CTkLabel(
            main_frame, 
            text="🏁 SIMULADOR DE CARRERAS DE TORTUGAS 🏁",
            font=("Segoe UI", 28, "bold"),
            text_color=("#00d4ff", "#00ffff")
        )
        title_label.pack(pady=(10, 25))
        
        # Frame superior: Selector de mapa y configuración
        top_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        top_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Panel izquierdo: Selector de mapa
        mapa_frame = ctk.CTkFrame(top_frame, corner_radius=10)
        mapa_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        ctk.CTkLabel(
            mapa_frame,
            text="🗺️ Selector de Mapa",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(10, 10))
        
        # Lista de mapas con vista previa
        self.crear_selector_mapas(mapa_frame)
        
        # Panel derecho: Configuración de tortugas
        config_frame = ctk.CTkFrame(top_frame, corner_radius=10)
        config_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        ctk.CTkLabel(
            config_frame,
            text="⚙️ Configuración de Tortugas",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(10, 10))
        
        # Selección de número de tortugas
        num_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        num_frame.pack(fill="x", pady=(0, 15), padx=15)
        
        ctk.CTkLabel(
            num_frame,
            text="Número de tortugas:",
            font=("Segoe UI", 12)
        ).pack(side="left", padx=(0, 10))
        
        self.num_tortugas_var = ctk.StringVar(value="3")
        num_spinbox = ctk.CTkOptionMenu(
            num_frame,
            variable=self.num_tortugas_var,
            values=["2", "3", "4", "5", "6"],
            width=80
        )
        num_spinbox.pack(side="left")
        
        # Botones en el mismo frame
        buttons_config_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        buttons_config_frame.pack(fill="x", pady=(0, 15), padx=15)
        
        ctk.CTkButton(
            buttons_config_frame,
            text="🔄 Actualizar Configuración",
            command=self.actualizar_config_tortugas,
            height=35,
            width=170,
            corner_radius=8
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            buttons_config_frame,
            text="🏁 Iniciar Carrera",
            command=self.iniciar_carrera,
            height=35,
            width=140,
            corner_radius=8,
            fg_color=("#00d4ff", "#0099cc"),
            hover_color=("#00a3cc", "#007799")
        ).pack(side="left")
        
        # Frame para configuración de tortugas con scroll
        self.scroll_frame = ctk.CTkScrollableFrame(
            config_frame,
            width=400,
            height=300,
            corner_radius=10
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.tortugas_config_frame = self.scroll_frame
        
        # Frame de botones principales (ahora solo historial y salir)
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(10, 10))
        
        # Botón para finalizar carrera (oculto inicialmente)
        self.btn_finalizar = ctk.CTkButton(
            buttons_frame,
            text="🏁 Finalizar Carrera",
            command=self.finalizar_carrera,
            width=150,
            height=40,
            corner_radius=10,
            fg_color=("#ff6b6b", "#cc5555")
        )
        
        ctk.CTkButton(
            buttons_frame,
            text="📊 Ver Historial",
            command=self.mostrar_historial,
            width=150,
            height=40,
            corner_radius=10
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="🗑️ Limpiar Historial",
            command=self.limpiar_historial,
            width=150,
            height=40,
            corner_radius=10,
            fg_color=("#ff9800", "#cc7700")
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="❌ Salir",
            command=self.root.quit,
            width=100,
            height=40,
            corner_radius=10,
            fg_color=("#ff0000", "#cc0000")
        ).pack(side="right", padx=5)
        
        # Inicializar configuración
        self.actualizar_config_tortugas()
        
        self.root.mainloop()
    
    def crear_selector_mapas(self, parent):
        """Crea el selector de mapas con vista previa"""
        # Canvas para vista previa del mapa seleccionado
        ctk.CTkLabel(
            parent,
            text="Vista Previa del Mapa:",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(5, 5), padx=10)
        
        # Usar tk.Canvas porque CustomTkinter no tiene canvas nativo
        import tkinter as tk
        self.canvas_preview = tk.Canvas(
            parent,
            width=400,
            height=200,
            bg='#000000',
            highlightthickness=2,
            highlightbackground='#00d4ff'
        )
        self.canvas_preview.pack(pady=(0, 15), padx=10)
        
        # Lista de mapas
        ctk.CTkLabel(
            parent,
            text="Mapas Disponibles:",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(5, 5), padx=10)
        
        self.mapa_var = ctk.StringVar(value="Pista Recta Clásica")
        
        for nombre_mapa, datos in self.mapas_disponibles.items():
            mapa_btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
            mapa_btn_frame.pack(fill="x", pady=2, padx=10)
            
            radio = ctk.CTkRadioButton(
                mapa_btn_frame,
                text=f"{nombre_mapa}",
                variable=self.mapa_var,
                value=nombre_mapa,
                command=self.actualizar_preview_mapa,
                font=("Segoe UI", 11)
            )
            radio.pack(side="left", anchor="w")
            
            # Etiqueta de complejidad con colores
            color_complejidad = "#ff6b6b" if datos['complejidad'] == 'Extrema' else "#ffd93d"
            complejidad_label = ctk.CTkLabel(
                mapa_btn_frame,
                text=f"[{datos['complejidad']}]",
                font=("Segoe UI", 9, "bold"),
                text_color=color_complejidad
            )
            complejidad_label.pack(side="right", padx=(10, 0))
        
        # Mostrar preview inicial
        self.actualizar_preview_mapa()
    
    def actualizar_preview_mapa(self):
        """Actualiza la vista previa del mapa seleccionado"""
        self.mapa_seleccionado = self.mapa_var.get()
        mapa_info = self.mapas_disponibles[self.mapa_seleccionado]
        
        # Limpiar canvas
        self.canvas_preview.delete("all")
        
        # Dibujar preview del mapa
        width = 400
        height = 200
        
        # Fondo
        self.canvas_preview.create_rectangle(0, 0, width, height, fill=mapa_info['color_fondo'], outline='')
        
        # Asfalto
        self.canvas_preview.create_rectangle(50, 30, width-50, height-30, fill=mapa_info['color_asfalto'], outline='')
        
        # Líneas de carril (3 carriles para preview)
        for i in range(4):
            y = 30 + (i * (height-60) / 3)
            # Línea discontinua amarilla
            for x in range(50, width-50, 20):
                self.canvas_preview.create_line(x, y, x+10, y, fill='#ffff00', width=2)
        
        # Línea de salida (verde)
        self.canvas_preview.create_line(70, 30, 70, height-30, fill='#00ff00', width=4)
        
        # Línea de meta (rojo con patrón de cuadros)
        for i in range(8):
            y_start = 30 + (i * (height-60) / 8)
            color = '#ff0000' if i % 2 == 0 else '#ffffff'
            self.canvas_preview.create_rectangle(width-70, y_start, width-66, y_start + (height-60)/8, 
                                                fill=color, outline='')
        
        # Decoraciones específicas del mapa
        self.dibujar_decoraciones_preview(mapa_info['color_fondo'])
        
        # Texto del mapa
        self.canvas_preview.create_text(width/2, 15, text=self.mapa_seleccionado, 
                                       fill='#00d4ff', font=('Arial', 12, 'bold'))
    
    def dibujar_decoraciones_preview(self, color_fondo):
        """Dibuja decoraciones específicas en la vista previa"""
        nombre = self.mapa_seleccionado
        
        if nombre == "Ciudad Nocturna":
            # Edificios
            for x in [20, 360]:
                for y_offset in [0, 60, 120]:
                    self.canvas_preview.create_rectangle(x, 50+y_offset, x+30, 80+y_offset, 
                                                        fill='#1a1a1a', outline='#00d4ff')
                    # Ventanas
                    for wx in range(3):
                        for wy in range(2):
                            self.canvas_preview.create_rectangle(x+5+wx*8, 55+y_offset+wy*10, 
                                                                x+10+wx*8, 60+y_offset+wy*10, 
                                                                fill='#ffff00', outline='')
        
        elif nombre == "Desierto Rojo":
            # Dunas
            for x in [10, 340, 370]:
                self.canvas_preview.create_arc(x, 140, x+60, 200, start=0, extent=180, 
                                              fill='#8b5a3c', outline='')
            # Sol
            self.canvas_preview.create_oval(360, 10, 390, 40, fill='#ff6b35', outline='')
        
        elif nombre == "Bosque Místico":
            # Árboles
            for x in [15, 25, 365, 375]:
                self.canvas_preview.create_rectangle(x, 60, x+10, 190, fill='#3d2817', outline='')
                self.canvas_preview.create_oval(x-10, 40, x+20, 80, fill='#1a5c1a', outline='')
        
        elif nombre == "Playa Tropical":
            # Palmeras
            for x in [15, 370]:
                self.canvas_preview.create_line(x, 180, x, 80, fill='#8B4513', width=4)
                # Hojas
                for angle in range(0, 360, 45):
                    x2 = x + 20 * math.cos(math.radians(angle))
                    y2 = 80 + 15 * math.sin(math.radians(angle))
                    self.canvas_preview.create_line(x, 80, x2, y2, fill='#228B22', width=3)
            # Olas
            for y in [25, 175]:
                for x in range(50, 350, 30):
                    self.canvas_preview.create_arc(x, y, x+20, y+10, start=0, extent=180, 
                                                  fill='#4a7a8a', outline='')
        
        elif nombre == "Montaña Nevada":
            # Montañas
            self.canvas_preview.create_polygon(20, 180, 60, 40, 100, 180, fill='#5a6d7e', outline='')
            self.canvas_preview.create_polygon(300, 180, 360, 30, 400, 180, fill='#5a6d7e', outline='')
            # Nieve en picos
            self.canvas_preview.create_polygon(50, 60, 60, 40, 70, 60, fill='#ffffff', outline='')
            self.canvas_preview.create_polygon(350, 50, 360, 30, 370, 50, fill='#ffffff', outline='')
        
        elif nombre == "Volcán Activo":
            # Volcán
            self.canvas_preview.create_polygon(350, 180, 380, 50, 410, 180, fill='#2d1414', outline='')
            # Lava
            for x in range(380, 400, 5):
                for y in range(50, 70, 5):
                    if random.random() > 0.5:
                        self.canvas_preview.create_oval(x, y, x+3, y+3, fill='#ff4500', outline='')
        
        elif nombre == "Espacio Sideral":
            # Estrellas
            for _ in range(20):
                x = random.randint(0, 400)
                y = random.randint(0, 200)
                self.canvas_preview.create_oval(x, y, x+2, y+2, fill='#ffffff', outline='')
            # Planeta
            self.canvas_preview.create_oval(350, 10, 390, 50, fill='#4a4a9a', outline='#8a8aff')
        
        elif nombre == "Selva Amazónica":
            # Vegetación densa
            for x in range(0, 400, 30):
                for y in [20, 170]:
                    self.canvas_preview.create_oval(x, y, x+25, y+30, fill='#2d5c2d', outline='')
            # Lianas
            for x in [20, 380]:
                self.canvas_preview.create_line(x, 0, x-5, 200, fill='#3d6d3d', width=2)
    
    def actualizar_config_tortugas(self):
        """Actualiza la configuración de tortugas dinámicamente"""
        # Limpiar frame anterior
        for widget in self.tortugas_config_frame.winfo_children():
            widget.destroy()
        
        self.tortuga_entries = []
        self.color_vars = []
        self.color_buttons = []
        
        num_tortugas = int(self.num_tortugas_var.get())
        
        for i in range(num_tortugas):
            # Frame para cada tortuga
            tortuga_frame = ctk.CTkFrame(self.tortugas_config_frame, fg_color="transparent")
            tortuga_frame.pack(fill="x", pady=8, padx=5)
            
            # Nombre de la tortuga
            ctk.CTkLabel(
                tortuga_frame,
                text=f"🐢 Tortuga {i+1}:",
                font=("Segoe UI", 11)
            ).pack(side="left", padx=(0, 5))
            
            nombre_var = ctk.StringVar(value=f"Speedy_{i+1}")
            nombre_entry = ctk.CTkEntry(
                tortuga_frame,
                textvariable=nombre_var,
                width=120,
                height=30
            )
            nombre_entry.pack(side="left", padx=(5, 15))
            self.tortuga_entries.append(nombre_var)
            
            # Color de la tortuga con paleta visual
            ctk.CTkLabel(
                tortuga_frame,
                text="Color:",
                font=("Segoe UI", 11)
            ).pack(side="left", padx=(0, 5))
            
            color_var = ctk.StringVar(value=self.colores_tortugas[i % len(self.colores_tortugas)])
            self.color_vars.append(color_var)
            
            # Botón de color visual (usar tk.Button porque CustomTkinter no soporta cambio de bg fácilmente)
            import tkinter as tk
            color_btn = tk.Button(
                tortuga_frame,
                text="  ",
                bg=color_var.get(),
                width=3,
                height=1,
                relief="raised",
                bd=3,
                command=lambda idx=i: self.abrir_selector_color(idx)
            )
            color_btn.pack(side=tk.LEFT, padx=(0, 5))
            self.color_buttons.append(color_btn)
            
            # Botón para abrir paleta
            ctk.CTkButton(
                tortuga_frame,
                text="🎨 Paleta",
                command=lambda idx=i: self.mostrar_paleta_colores(idx),
                width=80,
                height=28
            ).pack(side="left", padx=5)
    
    def abrir_selector_color(self, index):
        """Abre el selector de color estándar"""
        color_actual = self.color_vars[index].get()
        color = colorchooser.askcolor(
            title=f"Seleccionar color para Tortuga {index+1}",
            initialcolor=color_actual
        )
        if color[1]:  # Si se seleccionó un color
            self.color_vars[index].set(color[1])
            self.color_buttons[index].config(bg=color[1])
    
    def mostrar_paleta_colores(self, index):
        """Muestra una paleta de colores personalizada"""
        # Crear ventana de paleta con CTkToplevel
        import tkinter as tk
        paleta_window = ctk.CTkToplevel(self.root)
        paleta_window.title(f"🎨 Paleta de Colores - Tortuga {index+1}")
        paleta_window.geometry("650x600")
        paleta_window.transient(self.root)
        paleta_window.grab_set()
        
        # Frame principal
        main_frame = ctk.CTkFrame(paleta_window, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text=f"Selecciona un color para {self.tortuga_entries[index].get()}",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(10, 20))
        
        # Color actual
        current_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        current_frame.pack(fill="x", pady=(0, 15), padx=15)
        
        ctk.CTkLabel(
            current_frame,
            text="Color Actual:",
            font=("Segoe UI", 12, "bold")
        ).pack(side="left", padx=(0, 10))
        
        color_actual_display = tk.Canvas(
            current_frame,
            width=100,
            height=40,
            bg=self.color_vars[index].get(),
            highlightthickness=2,
            highlightbackground='#00d4ff'
        )
        color_actual_display.pack(side="left")
        
        # Paleta de colores vibrantes predefinidos
        ctk.CTkLabel(
            main_frame,
            text="Colores Vibrantes:",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(10, 10), padx=15)
        
        vibrant_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        vibrant_frame.pack(fill="x", pady=(0, 15), padx=15)
        
        cols = 5
        for i, color in enumerate(self.colores_tortugas):
            btn = tk.Button(
                vibrant_frame,
                bg=color,
                width=8,
                height=3,
                relief="raised",
                bd=3,
                command=lambda c=color: self.aplicar_color_paleta(index, c, color_actual_display, paleta_window)
            )
            btn.grid(row=i//cols, column=i%cols, padx=5, pady=5)
        
        # Colores adicionales variados
        ctk.CTkLabel(
            main_frame,
            text="Más Colores:",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(15, 10), padx=15)
        
        colores_extra = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8",
            "#F7DC6F", "#BB8FCE", "#85C1E2", "#F8B500", "#52B788",
            "#E63946", "#F1FAEE", "#A8DADC", "#457B9D", "#1D3557",
            "#FF595E", "#FFCA3A", "#8AC926", "#1982C4", "#6A4C93"
        ]
        
        extra_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        extra_frame.pack(fill="x", pady=(0, 15), padx=15)
        
        for i, color in enumerate(colores_extra):
            btn = tk.Button(
                extra_frame,
                bg=color,
                width=8,
                height=3,
                relief="raised",
                bd=3,
                command=lambda c=color: self.aplicar_color_paleta(index, c, color_actual_display, paleta_window)
            )
            btn.grid(row=i//cols, column=i%cols, padx=5, pady=5)
        
        # Botones de acción
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(15, 10), padx=15)
        
        ctk.CTkButton(
            button_frame,
            text="🎨 Selector Avanzado",
            command=lambda: self.abrir_selector_color(index),
            width=150,
            height=35
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            button_frame,
            text="❌ Cerrar",
            command=paleta_window.destroy,
            width=100,
            height=35,
            fg_color="#ff0000"
        ).pack(side="right")
    
    def aplicar_color_paleta(self, index, color, display_canvas, window):
        """Aplica el color seleccionado de la paleta"""
        self.color_vars[index].set(color)
        self.color_buttons[index].config(bg=color)
        display_canvas.config(bg=color)
        # Cerrar ventana de paleta después de seleccionar
        window.after(200, window.destroy)
    
    def dibujar_pista_recta(self, dibujante, mapa_info, num_tortugas):
        """Dibuja una pista recta horizontal con carriles paralelos"""
        # Ajustar ancho de carril según número de tortugas para que quepan en pantalla
        altura_disponible = 550  # Altura útil de la ventana (700 - márgenes)
        ancho_carril = min(80, altura_disponible // num_tortugas)
        inicio_y = (num_tortugas * ancho_carril) // 2
        
        for i in range(num_tortugas):
            y = inicio_y - (i * ancho_carril)
            
            # Dibujar asfalto del carril
            dibujante.penup()
            dibujante.goto(-450, y)
            dibujante.setheading(0)
            dibujante.color(mapa_info['color_asfalto'])
            dibujante.width(70)
            dibujante.pendown()
            dibujante.forward(900)
            
            # Línea divisoria blanca entre carriles
            if i < num_tortugas - 1:
                dibujante.penup()
                dibujante.goto(-450, y - 40)
                dibujante.color('#ffffff')
                dibujante.width(3)
                for x in range(-450, 450, 40):
                    dibujante.goto(x, y - 40)
                    dibujante.pendown()
                    dibujante.forward(20)
                    dibujante.penup()
        
        # Línea de salida (verde)
        dibujante.penup()
        dibujante.goto(-430, inicio_y + 40)
        dibujante.setheading(270)
        dibujante.color('#00ff00')
        dibujante.width(8)
        dibujante.pendown()
        dibujante.forward(num_tortugas * ancho_carril)
        
        # Línea de meta (ajedrez rojo y blanco)
        dibujante.penup()
        dibujante.goto(430, inicio_y + 40)
        cuadro_alto = (num_tortugas * ancho_carril) / 10
        for i in range(10):
            dibujante.goto(430, inicio_y + 40 - i * cuadro_alto)
            dibujante.setheading(0)
            dibujante.color('#ff0000' if i % 2 == 0 else '#ffffff')
            dibujante.pendown()
            dibujante.begin_fill()
            for _ in range(2):
                dibujante.forward(15)
                dibujante.right(90)
                dibujante.forward(cuadro_alto)
                dibujante.right(90)
            dibujante.end_fill()
            dibujante.penup()
    
    def dibujar_pista_ovalo(self, dibujante, mapa_info, num_tortugas):
        """Dibuja una pista ovalada estilo NASCAR"""
        # Parámetros del óvalo
        ancho = 700
        alto = 400
        radio_curva = alto / 2
        # Ajustar offset según número de tortugas (max 150px para 6 tortugas)
        offset_carril = min(35, 150 // num_tortugas)
        
        for i in range(num_tortugas):
            offset = i * offset_carril
            dibujante.penup()
            dibujante.color(mapa_info['color_asfalto'])
            dibujante.width(60)
            
            # Parte recta superior
            dibujante.goto(-ancho/2 + offset, alto/2 - offset)
            dibujante.setheading(0)
            dibujante.pendown()
            dibujante.forward(ancho - 2*offset)
            
            # Curva derecha
            dibujante.circle(-(radio_curva - offset), 180)
            
            # Parte recta inferior
            dibujante.setheading(180)
            dibujante.forward(ancho - 2*offset)
            
            # Curva izquierda
            dibujante.circle(-(radio_curva - offset), 180)
            
            # Líneas amarillas discontinuas (solo primer carril)
            if i == 0:
                dibujante.penup()
                dibujante.goto(-ancho/2, alto/2)
                dibujante.color('#ffff00')
                dibujante.width(3)
                dibujante.setheading(0)
                
                # Superior
                for x in range(int(-ancho/2), int(ancho/2), 40):
                    dibujante.goto(x, alto/2)
                    dibujante.pendown()
                    dibujante.forward(20)
                    dibujante.penup()
                
                # Inferior
                for x in range(int(ancho/2), int(-ancho/2), -40):
                    dibujante.goto(x, -alto/2)
                    dibujante.pendown()
                    dibujante.forward(-20)
                    dibujante.penup()
        
        # Línea de salida/meta (verde/rojo)
        dibujante.penup()
        dibujante.goto(-ancho/2 + 50, alto/2 + 30)
        dibujante.setheading(270)
        dibujante.color('#00ff00')
        dibujante.width(8)
        dibujante.pendown()
        dibujante.forward((num_tortugas * offset_carril) + 60)
        
        dibujante.penup()
        dibujante.goto(ancho/2 - 50, alto/2 + 30)
        dibujante.color('#ff0000')
        dibujante.pendown()
        dibujante.forward((num_tortugas * offset_carril) + 60)
    
    def dibujar_pista_s_doble(self, dibujante, mapa_info, num_tortugas):
        """Dibuja una pista sinuosa en forma de S doble"""
        # Ajustar ancho de carril según número de tortugas
        altura_disponible = 550
        ancho_carril = min(70, altura_disponible // num_tortugas)
        
        for i in range(num_tortugas):
            y_offset = 150 - (i * ancho_carril)
            dibujante.penup()
            dibujante.goto(-450, y_offset)
            dibujante.color(mapa_info['color_asfalto'])
            dibujante.width(65)
            dibujante.pendown()
            
            # Crear curva S doble suave
            puntos = []
            for x in range(-450, 451, 5):
                # Primera S
                if x < -150:
                    y = y_offset + 80 * math.sin((x + 450) * 0.015)
                # Transición
                elif x < 150:
                    y = y_offset + 80 * math.sin((x + 150) * 0.015)
                # Segunda S invertida
                else:
                    y = y_offset - 80 * math.sin((x - 150) * 0.015)
                
                puntos.append((x, y))
            
            # Dibujar la curva
            for x, y in puntos:
                dibujante.goto(x, y)
            
            # Línea central amarilla (solo primer carril)
            if i == 0:
                dibujante.penup()
                dibujante.color('#ffff00')
                dibujante.width(3)
                for j, (x, y) in enumerate(puntos):
                    if j % 8 == 0:
                        dibujante.goto(x, y)
                        dibujante.pendown()
                        if j + 4 < len(puntos):
                            dibujante.goto(puntos[j + 4][0], puntos[j + 4][1])
                        dibujante.penup()
        
        # Línea de salida (verde)
        dibujante.penup()
        dibujante.goto(-435, 150 + 40)
        dibujante.setheading(270)
        dibujante.color('#00ff00')
        dibujante.width(8)
        dibujante.pendown()
        dibujante.forward(num_tortugas * ancho_carril + 40)
        
        # Línea de meta (roja)
        dibujante.penup()
        dibujante.goto(435, 150 + 40)
        dibujante.color('#ff0000')
        dibujante.pendown()
        dibujante.forward(num_tortugas * ancho_carril + 40)
    
    def crear_pista_compleja(self):
        """Crea una pista de carreras según el mapa seleccionado"""
        self.screen.clear()
        
        # Obtener información del mapa
        mapa_info = self.mapas_disponibles[self.mapa_seleccionado]
        
        # Configurar la pantalla
        self.screen.setup(1000, 700)
        self.screen.bgcolor(mapa_info['color_fondo'])
        self.screen.title(f"🏁 Carrera de Tortugas - {self.mapa_seleccionado}")
        
        # Desactivar animaciones para dibujo rápido
        self.screen.tracer(0)
        
        # Crear tortuga para dibujar
        dibujante = turtle.Turtle()
        dibujante.speed(0)
        dibujante.penup()
        dibujante.hideturtle()
        
        # Dibujar estrellas de fondo
        dibujante.color('#ffffff')
        for _ in range(50):
            x = random.randint(-490, 490)
            y = random.randint(-340, 340)
            dibujante.goto(x, y)
            dibujante.dot(2)
        
        # Dibujar la pista según su forma
        forma = mapa_info['forma']
        num_tortugas = int(self.num_tortugas_var.get())
        
        if forma == "recta":
            self.dibujar_pista_recta(dibujante, mapa_info, num_tortugas)
        elif forma == "ovalo":
            self.dibujar_pista_ovalo(dibujante, mapa_info, num_tortugas)
        elif forma == "s_doble":
            self.dibujar_pista_s_doble(dibujante, mapa_info, num_tortugas)
        
        # Texto de título
        dibujante.penup()
        dibujante.goto(0, 320)
        dibujante.color('#00d4ff')
        dibujante.write(f"🏁 {self.mapa_seleccionado.upper()} 🏁", 
                       align="center", font=("Arial", 16, "bold"))
        
        dibujante.hideturtle()
        
        # Guardar los puntos de la pista para navegación (una ruta por tortuga)
        num_tortugas = int(self.num_tortugas_var.get())
        self.calcular_puntos_navegacion(forma, num_tortugas)
        
        # Actualizar pantalla
        self.screen.update()
        
        # REACTIVAR animaciones para la carrera
        self.screen.tracer(1)
        
        self.pista_creada = True
    
    def calcular_puntos_navegacion(self, forma, num_tortugas):
        """Calcula los puntos de navegación para cada tortuga en su carril"""
        self.puntos_ruta = []  # Lista de listas: una ruta por cada tortuga
        
        if forma == "recta":
            # Pista Recta Clásica: cada tortuga en su línea horizontal
            altura_disponible = 550
            ancho_carril = min(80, altura_disponible // num_tortugas)
            inicio_y = (num_tortugas * ancho_carril) // 2
            for i in range(num_tortugas):
                ruta_tortuga = []
                y_carril = inicio_y - (i * ancho_carril)
                for x in range(-450, 450, 5):
                    ruta_tortuga.append((x, y_carril))
                self.puntos_ruta.append(ruta_tortuga)
        
        elif forma == "ovalo":
            # Óvalo NASCAR: cada tortuga en su óvalo concéntrico
            ancho = 700
            alto = 400
            radio_curva = alto / 2
            offset_carril = min(35, 150 // num_tortugas)
            
            for i in range(num_tortugas):
                ruta_tortuga = []
                offset = i * offset_carril  # Separación entre carriles
                radio_actual = radio_curva - offset
                
                # Coordenadas clave del óvalo (según test)
                x_izq = -ancho/2 + offset   # -350 + offset
                x_der = ancho/2 - offset    # 350 - offset
                y_sup = alto/2 - offset     # 200 - offset
                y_inf = -alto/2 + offset    # -200 + offset
                
                # RECTA SUPERIOR: de (x_izq, y_sup) a (x_der, y_sup)
                num_puntos = int(ancho - 2*offset) // 5
                for j in range(num_puntos + 1):
                    t = j / num_puntos if num_puntos > 0 else 0
                    x = x_izq + (x_der - x_izq) * t
                    y = y_sup
                    ruta_tortuga.append((x, y))
                
                # CURVA DERECHA: semicírculo de (x_der, y_sup) a (x_der, y_inf)
                # Centro en (x_der, 0), radio = radio_actual
                # Gira en sentido horario de 90° a -90°
                for angle in range(90, -91, -2):
                    x = x_der + radio_actual * math.cos(math.radians(angle))
                    y = 0 + radio_actual * math.sin(math.radians(angle))
                    ruta_tortuga.append((x, y))
                
                # RECTA INFERIOR: de (x_der, y_inf) a (x_izq, y_inf)
                for j in range(num_puntos + 1):
                    t = j / num_puntos if num_puntos > 0 else 0
                    x = x_der - (x_der - x_izq) * t
                    y = y_inf
                    ruta_tortuga.append((x, y))
                
                # CURVA IZQUIERDA: semicírculo de (x_izq, y_inf) a (x_izq, y_sup)
                # Centro en (x_izq, 0), radio = radio_actual
                # Gira en sentido horario desde -90° (sur) hasta 90° (norte)
                # Ruta horaria: -90° → -180° → -270° (equivale a 90°)
                for i_angle in range(91):  # 0 a 90 pasos
                    angle = -90 - (i_angle * 2)  # -90, -92, -94... hasta -270
                    x = x_izq + radio_actual * math.cos(math.radians(angle))
                    y = 0 + radio_actual * math.sin(math.radians(angle))
                    ruta_tortuga.append((x, y))
                
                self.puntos_ruta.append(ruta_tortuga)
        
        elif forma == "s_doble":
            # Circuito en S: cada tortuga en su curva sinusoidal paralela
            altura_disponible = 550
            ancho_carril = min(70, altura_disponible // num_tortugas)
            
            for i in range(num_tortugas):
                ruta_tortuga = []
                y_offset = 150 - (i * ancho_carril)
                
                # Usar el mismo rango que en el dibujo para consistencia
                for x in range(-450, 451, 3):
                    # Primera S
                    if x < -150:
                        y = y_offset + 80 * math.sin((x + 450) * 0.015)
                    # Transición
                    elif x < 150:
                        y = y_offset + 80 * math.sin((x + 150) * 0.015)
                    # Segunda S invertida
                    else:
                        y = y_offset - 80 * math.sin((x - 150) * 0.015)
                    
                    ruta_tortuga.append((x, y))
                
                self.puntos_ruta.append(ruta_tortuga)
        
        else:
            # Por defecto: línea recta para cada tortuga
            ancho_carril = 80
            inicio_y = 150
            for i in range(num_tortugas):
                ruta_tortuga = []
                y_carril = inicio_y - (i * ancho_carril)
                for x in range(-450, 450, 5):
                    ruta_tortuga.append((x, y_carril))
                self.puntos_ruta.append(ruta_tortuga)
    
    def dibujar_decoraciones_mapa(self, dibujante):
        """Añade decoraciones adicionales según el mapa"""
        # Indicadores de distancia
        dibujante.penup()
        dibujante.color('#ffffff')
        for i, x in enumerate(range(-400, 500, 200)):
            dibujante.goto(x, -370)
            dibujante.write(f"{i*200}m", align="center", font=("Arial", 12, "bold"))
    
    def crear_tortugas_participantes(self):
        """Crea las tortugas participantes con nombres flotantes"""
        self.tortugas = []
        self.nombres_tortugas = []
        self.labels_nombres = []
        self.tortuga_indices = []  # Índice de posición en la ruta para cada tortuga
        
        num_tortugas = int(self.num_tortugas_var.get())
        
        # Obtener forma del mapa
        forma = self.mapas_disponibles[self.mapa_seleccionado]['forma']
        
        for i in range(num_tortugas):
            # Crear tortuga
            tortuga = turtle.Turtle()
            tortuga.shape("turtle")
            tortuga.color(self.color_vars[i].get())
            tortuga.penup()
            tortuga.speed(0)
            
            # Posición inicial según la forma del mapa (todas en el mismo carril/anillo)
            if forma == "recta":
                # Pista recta: cada tortuga en su carril (de arriba hacia abajo)
                altura_disponible = 550
                ancho_carril = min(80, altura_disponible // num_tortugas)
                inicio_y = (num_tortugas * ancho_carril) // 2
                tortuga.goto(-430, inicio_y - (i * ancho_carril))
                tortuga.setheading(0)
            elif forma == "ovalo":
                # Óvalo: cada tortuga en su carril (círculos concéntricos)
                ancho = 700
                alto = 400
                offset_carril = min(35, 150 // num_tortugas)
                offset = i * offset_carril  # Mismo offset que en dibujo
                # Posición inicial exacta (igual al dibujo y navegación)
                tortuga.goto(-ancho/2 + offset, alto/2 - offset)
                tortuga.setheading(0)
            elif forma == "s_doble":
                # Circuito en S: cada tortuga en su carril (ondas paralelas)
                altura_disponible = 550
                ancho_carril = min(70, altura_disponible // num_tortugas)
                y_offset = 150 - (i * ancho_carril)
                tortuga.goto(-450, y_offset)
                tortuga.setheading(0)
            elif forma == "circular":
                # Todas en el mismo radio, distribuidas alrededor del círculo
                radio = 200  # Mismo radio para todas
                angulo_separacion = 360 / num_tortugas
                angulo = i * angulo_separacion
                x = radio * math.cos(math.radians(angulo))
                y = radio * math.sin(math.radians(angulo))
                tortuga.goto(x, y)
                tortuga.setheading(angulo + 90)  # Perpendicular al radio
            elif forma == "espiral":
                # Distribuidas en la línea de salida
                espacio = 50
                offset_x = -380
                offset_y = -(num_tortugas - 1) * espacio / 2
                tortuga.goto(offset_x, offset_y + i * espacio)
                tortuga.setheading(0)
            elif forma == "cuadrado" or forma == "hexagono":
                # Distribuidas en la línea de salida del cuadrado/hexágono
                lado = 380 if forma == "cuadrado" else 155
                espacio = 40
                offset = -(num_tortugas - 1) * espacio / 2
                tortuga.goto(-lado/2, -lado/2 + offset + i * espacio)
                tortuga.setheading(0)
            elif forma == "estrella":
                # Distribuidas alrededor del círculo exterior de la estrella
                radio = 210  # Mismo radio para todas
                angulo_separacion = 360 / num_tortugas
                angulo = i * angulo_separacion
                x = radio * math.cos(math.radians(angulo - 90))
                y = radio * math.sin(math.radians(angulo - 90))
                tortuga.goto(x, y)
                tortuga.setheading(angulo)
            elif forma == "infinito":
                # Distribuidas en el círculo izquierdo del infinito
                radio = 115
                angulo_separacion = 360 / num_tortugas
                angulo = 90 + i * angulo_separacion
                x = -150 + radio * math.cos(math.radians(angulo))
                y = radio * math.sin(math.radians(angulo))
                tortuga.goto(x, y)
                tortuga.setheading(angulo + 90)
            else:
                # Por defecto (zigzag, onda, montañarusa, túnel3d) - distribuidas en línea de salida
                espacio = 50
                offset_y = -(num_tortugas - 1) * espacio / 2
                tortuga.goto(-450, offset_y + i * espacio)
                tortuga.setheading(0)
            
            self.tortugas.append(tortuga)
            self.tortuga_indices.append(0)  # Empezar en el índice 0 de la ruta
            
            # Nombre de la tortuga
            nombre = self.tortuga_entries[i].get()
            self.nombres_tortugas.append(nombre)
    
    def iniciar_carrera(self):
        """Inicia una nueva carrera"""
        # Verificar si hay carrera en progreso
        if self.carrera_en_progreso:
            messagebox.showwarning("⚠️ Carrera en Progreso", "Ya hay una carrera en progreso. Espera a que termine o cierra la ventana de la carrera.")
            return
            
            # Divisor de carril (línea blanca ondulada entre carriles)
            if i < num_tortugas - 1:
                dibujante.penup()
                dibujante.color('#ffffff')
                dibujante.width(1)
                for x in range(-450, 450, 15):
                    y = (y_base - ancho_carril/2) + 45 * math.sin((x + 450) * 0.02)
                    dibujante.goto(x, y)
                    if x % 30 == 0:
                        dibujante.pendown()
                    else:
                        dibujante.penup()
            
            # Líneas amarillas simplificadas (solo primer carril)
            if i == 0:
                dibujante.penup()
                dibujante.goto(-450, y_base)
                dibujante.color('#ffff00')
                dibujante.width(2)
                for x in range(-450, 450, 40):
                    y = y_base + 45 * math.sin((x + 450) * 0.02)
                    dibujante.goto(x, y)
                    dibujante.pendown()
                    dibujante.forward(10)
                    dibujante.penup()
    
    def dibujar_pista_cuadrado(self, dibujante, mapa_info, num_tortugas):
        """Dibuja una pista en forma de cuadrado"""
        lado = 380
        
        for i in range(num_tortugas):
            offset = i * 40
            dibujante.penup()
            dibujante.goto(-lado/2 + offset, -lado/2 + offset)
            dibujante.setheading(0)
            dibujante.color(mapa_info['color_asfalto'])
            dibujante.width(35)
            dibujante.pendown()
            
            for _ in range(4):
                dibujante.forward(lado - 2*offset)
                dibujante.left(90)
            
            # Líneas amarillas discontinuas simplificadas (solo primer carril)
            if i == 0:
                dibujante.penup()
                dibujante.goto(-lado/2 + offset, -lado/2 + offset)
                dibujante.setheading(0)
                dibujante.color('#ffff00')
                dibujante.width(3)
                
                for _ in range(4):
                    for _ in range(int((lado - 2*offset) / 50)):
                        dibujante.pendown()
                        dibujante.forward(20)
                        dibujante.penup()
                        dibujante.forward(30)
                    dibujante.left(90)
    
    def dibujar_pista_tunel3d(self, dibujante, mapa_info, num_tortugas):
        """Dibuja una pista con efecto 3D de túnel"""
        # Dibujar rectángulos concéntricos reducidos para efecto de profundidad
        for profundidad in range(8, 0, -1):
            escala = profundidad / 8
            ancho = 450 * escala
            alto = 300 * escala
            
            dibujante.penup()
            dibujante.goto(-ancho/2, -alto/2)
            dibujante.setheading(0)
            
            # Color más claro cuanto más lejos
            gris = int(40 + (8 - profundidad) * 25)
            dibujante.color(f'#{gris:02x}{gris:02x}{gris:02x}')
            dibujante.width(3)
            dibujante.pendown()
            
            for _ in range(2):
                dibujante.forward(ancho)
                dibujante.left(90)
                dibujante.forward(alto)
                dibujante.left(90)
        
        # Dibujar carriles para las tortugas
        ancho_carril = 60
        for i in range(num_tortugas):
            y_pos = 200 - (i * ancho_carril)
            dibujante.penup()
            dibujante.goto(-550, y_pos)
            dibujante.color('#ffff00')
            dibujante.width(2)
            
            for x in range(-550, 550, 30):
                escala_x = 1 - (x + 550) / 1100 * 0.3
                dibujante.goto(x, y_pos)
                dibujante.pendown()
                dibujante.forward(15)
                dibujante.penup()
    
    def dibujar_pista_estrella(self, dibujante, mapa_info, num_tortugas):
        """Dibuja una pista en forma de estrella de 5 puntas"""
        centro = (0, 0)
        radio_exterior = 210
        radio_interior = 90
        
        for i in range(num_tortugas):
            radio_ext = radio_exterior - (i * 25)
            radio_int = radio_interior - (i * 12)
            
            dibujante.penup()
            dibujante.goto(centro[0], centro[1] + radio_ext)
            dibujante.setheading(-90)
            dibujante.color(mapa_info['color_asfalto'])
            dibujante.width(28)
            dibujante.pendown()
            
            # Dibujar estrella
            for _ in range(5):
                # Punto exterior a interior
                angle_to_inner = 180 - 36
                dibujante.right(angle_to_inner)
                distance = math.sqrt(radio_ext**2 + radio_int**2 - 2*radio_ext*radio_int*math.cos(math.radians(72)))
                dibujante.forward(distance)
                
                # Punto interior a exterior
                dibujante.right(180 - 72)
                dibujante.forward(distance)
            
            # Líneas amarillas simplificadas (solo primer carril)
            if i == 0:
                dibujante.penup()
                dibujante.goto(centro[0], centro[1] + radio_ext)
                dibujante.color('#ffff00')
                dibujante.width(2)
                dibujante.pendown()
                
                for _ in range(5):
                    for _ in range(8):
                        dibujante.pendown()
                        dibujante.forward(12)
                        dibujante.penup()
                        dibujante.forward(12)
    
    def dibujar_pista_infinito(self, dibujante, mapa_info, num_tortugas):
        """Dibuja una pista en forma de símbolo infinito (∞)"""
        for i in range(num_tortugas):
            offset = i * 20
            dibujante.penup()
            dibujante.goto(-150 + offset, 0)
            dibujante.setheading(90)
            dibujante.color(mapa_info['color_asfalto'])
            dibujante.width(32)
            dibujante.pendown()
            
            # Círculo izquierdo (reducido)
            dibujante.circle(115 - offset, 360)
            
            # Moverse al círculo derecho
            dibujante.penup()
            dibujante.goto(150 - offset, 0)
            dibujante.setheading(90)
            dibujante.pendown()
            
            # Círculo derecho (en sentido contrario, reducido)
            dibujante.circle(-(115 - offset), 360)
            
            # Líneas amarillas simplificadas (solo primer carril)
            if i == 0:
                dibujante.penup()
                dibujante.goto(-150 + offset, 0)
                dibujante.color('#ffff00')
                dibujante.width(2)
                dibujante.pendown()
                
                for angle in range(0, 360, 30):
                    dibujante.setheading(90)
                    dibujante.circle(115 - offset, 10)
                    dibujante.penup()
                    dibujante.circle(115 - offset, 20)
                    dibujante.pendown()
    
    def dibujar_pista_montaniarusa(self, dibujante, mapa_info, num_tortugas):
        """Dibuja una pista con efecto de montaña rusa (perspectiva 3D)"""
        ancho_carril = 55
        
        for i in range(num_tortugas):
            y_base = 190 - (i * ancho_carril)
            dibujante.penup()
            dibujante.goto(-450, y_base)
            dibujante.color(mapa_info['color_asfalto'])
            dibujante.width(ancho_carril - 10)
            dibujante.pendown()
            
            # Crear efecto de subidas y bajadas (reducido)
            for x in range(-450, 450, 8):
                # Combinación de ondas para efecto 3D
                y = y_base + 40 * math.sin((x + 450) * 0.015) + 25 * math.cos((x + 450) * 0.03)
                # Efecto de escala (perspectiva)
                escala = 0.7 + 0.3 * (math.sin((x + 450) * 0.01) + 1) / 2
                dibujante.goto(x, y)
                dibujante.width((ancho_carril - 10) * escala)
            
            # Divisor de carril (línea blanca con perspectiva entre carriles)
            if i < num_tortugas - 1:
                dibujante.penup()
                dibujante.color('#ffffff')
                for x in range(-450, 450, 20):
                    y = (y_base - ancho_carril/2) + 40 * math.sin((x + 450) * 0.015) + 25 * math.cos((x + 450) * 0.03)
                    dibujante.goto(x, y)
                    if x % 40 == 0:
                        dibujante.pendown()
                        dibujante.dot(3)
                        dibujante.penup()
            
            # Líneas amarillas con perspectiva (solo primer carril)
            if i == 0:
                dibujante.penup()
                dibujante.goto(-450, y_base)
                dibujante.color('#ffff00')
                
                for x in range(-450, 450, 40):
                    y = y_base + 40 * math.sin((x + 450) * 0.015) + 25 * math.cos((x + 450) * 0.03)
                    dibujante.penup()
                    dibujante.goto(x, y)
                    dibujante.pendown()
                    dibujante.dot(5)
    
    def dibujar_pista_hexagono(self, dibujante, mapa_info, num_tortugas):
        """Dibuja una pista en forma de hexágono perfecto"""
        lado = 155
        
        for i in range(num_tortugas):
            offset = i * 28
            dibujante.penup()
            dibujante.goto(-(lado - offset) / 2, -(lado - offset) * math.sqrt(3) / 2)
            dibujante.setheading(0)
            dibujante.color(mapa_info['color_asfalto'])
            dibujante.width(32)
            dibujante.pendown()
            
            # Dibujar hexágono (reducido)
            for _ in range(6):
                dibujante.forward(lado - offset)
                dibujante.left(60)
            
            # Líneas amarillas simplificadas (solo primer carril)
            if i == 0:
                dibujante.penup()
                dibujante.goto(-(lado - offset) / 2, -(lado - offset) * math.sqrt(3) / 2)
                dibujante.setheading(0)
                dibujante.color('#ffff00')
                dibujante.width(3)
                
                for _ in range(6):
                    for _ in range(int((lado - offset) / 35)):
                        dibujante.pendown()
                        dibujante.forward(15)
                        dibujante.penup()
                        dibujante.forward(20)
                    dibujante.left(60)
    
    def dibujar_linea_meta(self, dibujante):
        """Dibuja una línea de meta con patrón de cuadros"""
        dibujante.penup()
        dibujante.goto(600, 350)
        
        cuadro_altura = 650 / 13
        for i in range(13):
            y = 350 - (i * cuadro_altura)
            dibujante.goto(600, y)
            dibujante.pendown()
            dibujante.color('#ff0000' if i % 2 == 0 else '#ffffff')
            dibujante.begin_fill()
            for _ in range(2):
                dibujante.forward(10)
                dibujante.right(90)
                dibujante.forward(cuadro_altura)
                dibujante.right(90)
            dibujante.end_fill()
            dibujante.penup()
    
    def dibujar_fondo_mapa_forma(self, dibujante, mapa_info):
        """Dibuja elementos de fondo específicos del mapa según su forma"""
        forma = mapa_info['forma']
        
        # Estrellas de fondo para todas las formas (reducido para velocidad)
        dibujante.color('#ffffff')
        for _ in range(40):
            x = random.randint(-490, 490)
            y = random.randint(-340, 340)
            dibujante.penup()
            dibujante.goto(x, y)
            dibujante.dot(random.randint(1, 3))
        
        # Decoraciones específicas según la forma (simplificadas para velocidad)
        if forma == "circular":
            # Tribunas alrededor
            for angle in range(0, 360, 60):
                x = 300 * math.cos(math.radians(angle))
                y = 300 * math.sin(math.radians(angle))
                dibujante.penup()
                dibujante.goto(x, y)
                dibujante.dot(25, '#3d3d3d')
        
        elif forma == "espiral":
            # Galaxia de fondo
            for i in range(0, 25):
                angle = i * 14.4
                radio = 280 - i * 8
                x = radio * math.cos(math.radians(angle))
                y = radio * math.sin(math.radians(angle))
                dibujante.penup()
                dibujante.goto(x, y)
                dibujante.dot(random.randint(8, 12), '#4a4a9a')
        
        elif forma == "zigzag":
            # Llamas de fondo
            for x in range(-450, 450, 150):
                for y in [-300, 300]:
                    dibujante.penup()
                    dibujante.goto(x, y)
                    dibujante.dot(random.randint(15, 25), random.choice(['#ff4500', '#ff6347']))
        
        elif forma == "onda":
            # Olas en el fondo
            for y in [-300, 300]:
                for x in range(-450, 450, 100):
                    dibujante.penup()
                    dibujante.goto(x, y)
                    dibujante.color('#4a7a8a')
                    dibujante.dot(20)
        
        elif forma == "tunel3d" or forma == "montaniarusa":
            # Grid 3D simplificado
            dibujante.color('#2d2d2d')
            dibujante.width(1)
            for x in range(-450, 450, 100):
                dibujante.penup()
                dibujante.goto(x, -300)
                dibujante.pendown()
                dibujante.goto(x, 300)
            for y in range(-300, 300, 100):
                dibujante.penup()
                dibujante.goto(-450, y)
                dibujante.pendown()
                dibujante.goto(450, y)
        
        elif forma == "estrella":
            # Constelaciones
            for _ in range(12):
                x = random.randint(-450, 450)
                y = random.randint(-280, 280)
                dibujante.penup()
                dibujante.goto(x, y)
                dibujante.color('#ffd93d')
                dibujante.dot(random.randint(6, 10))
        
        elif forma == "infinito":
            # Partículas flotantes
            for _ in range(20):
                x = random.randint(-400, 400)
                y = random.randint(-250, 250)
                dibujante.penup()
                dibujante.goto(x, y)
                dibujante.dot(random.randint(5, 10), '#9a4a9a')
        
        dibujante.width(1)
        dibujante.setheading(0)
    
    def dibujar_decoraciones_mapa(self, dibujante):
        """Añade decoraciones adicionales según el mapa"""
        # Indicadores de distancia
        dibujante.penup()
        dibujante.color('#ffffff')
        for i, x in enumerate(range(-400, 500, 200)):
            dibujante.goto(x, -370)
            dibujante.write(f"{i*200}m", align="center", font=("Arial", 12, "bold"))
    
    def crear_tortugas_participantes(self):
        """Crea las tortugas participantes con nombres flotantes"""
        self.tortugas = []
        self.nombres_tortugas = []
        self.labels_nombres = []
        self.tortuga_indices = []  # Índice de posición en la ruta para cada tortuga
        
        num_tortugas = int(self.num_tortugas_var.get())
        
        # Obtener forma del mapa
        forma = self.mapas_disponibles[self.mapa_seleccionado]['forma']
        
        for i in range(num_tortugas):
            # Crear tortuga
            tortuga = turtle.Turtle()
            tortuga.shape("turtle")
            tortuga.color(self.color_vars[i].get())
            tortuga.penup()
            tortuga.speed(0)
            
            # Posición inicial según la forma del mapa (todas en el mismo carril/anillo)
            if forma == "circular":
                # Todas en el mismo radio, distribuidas alrededor del círculo
                radio = 200  # Mismo radio para todas
                angulo_separacion = 360 / num_tortugas
                angulo = i * angulo_separacion
                x = radio * math.cos(math.radians(angulo))
                y = radio * math.sin(math.radians(angulo))
                tortuga.goto(x, y)
                tortuga.setheading(angulo + 90)  # Perpendicular al radio
            elif forma == "espiral":
                # Distribuidas en la línea de salida
                espacio = 50
                offset_x = -380
                offset_y = -(num_tortugas - 1) * espacio / 2
                tortuga.goto(offset_x, offset_y + i * espacio)
                tortuga.setheading(0)
            elif forma == "cuadrado" or forma == "hexagono":
                # Distribuidas en la línea de salida del cuadrado/hexágono
                lado = 380 if forma == "cuadrado" else 155
                espacio = 40
                offset = -(num_tortugas - 1) * espacio / 2
                tortuga.goto(-lado/2, -lado/2 + offset + i * espacio)
                tortuga.setheading(0)
            elif forma == "estrella":
                # Distribuidas alrededor del círculo exterior de la estrella
                radio = 210  # Mismo radio para todas
                angulo_separacion = 360 / num_tortugas
                angulo = i * angulo_separacion
                x = radio * math.cos(math.radians(angulo - 90))
                y = radio * math.sin(math.radians(angulo - 90))
                tortuga.goto(x, y)
                tortuga.setheading(angulo)
            elif forma == "infinito":
                # Distribuidas en el círculo izquierdo del infinito
                radio = 115
                angulo_separacion = 360 / num_tortugas
                angulo = 90 + i * angulo_separacion
                x = -150 + radio * math.cos(math.radians(angulo))
                y = radio * math.sin(math.radians(angulo))
                tortuga.goto(x, y)
                tortuga.setheading(angulo + 90)
            else:
                # Por defecto (zigzag, onda, montañarusa, túnel3d) - distribuidas en línea de salida
                espacio = 50
                offset_y = -(num_tortugas - 1) * espacio / 2
                tortuga.goto(-450, offset_y + i * espacio)
                tortuga.setheading(0)
            
            self.tortugas.append(tortuga)
            self.tortuga_indices.append(0)  # Empezar en el índice 0 de la ruta
            
            # Nombre de la tortuga
            nombre = self.tortuga_entries[i].get()
            self.nombres_tortugas.append(nombre)
            
            # Crear label para el nombre (flotante)
            label = turtle.Turtle()
            label.hideturtle()
            label.penup()
            label.color('#ffffff')
            x, y = tortuga.position()
            label.goto(x, y + 30)
            label.write(nombre, align="center", font=("Arial", 10, "bold"))
            self.labels_nombres.append(label)
    
    def actualizar_nombres_flotantes(self):
        """Actualiza la posición de los nombres flotantes"""
        for i, (tortuga, label, nombre) in enumerate(zip(self.tortugas, self.labels_nombres, self.nombres_tortugas)):
            label.clear()
            x, y = tortuga.position()
            label.goto(x, y + 30)
            label.write(nombre, align="center", font=("Arial", 10, "bold"))
    
    def simular_carrera(self):
        """Simula la carrera con efectos visuales modernos"""
        # Verificar si la ventana de turtle fue cerrada
        try:
            self.screen.update()
        except:
            # La ventana fue cerrada, cancelar carrera sin guardar
            self.cancelar_carrera_sin_guardar()
            return
        
        if not hasattr(self, 'tiempo_inicio_carrera'):
            self.carrera_en_progreso = True
            self.tiempo_inicio_carrera = time.time()
            self.ganador_carrera = None
        
        # Procesar un frame de la carrera
        if self.carrera_en_progreso:
            for i, tortuga in enumerate(self.tortugas):
                if not self.carrera_en_progreso:
                    break
                
                # Obtener puntos totales para esta tortuga específica
                total_puntos = len(self.puntos_ruta[i])
                
                # Movimiento aleatorio más realista
                velocidad_base = random.randint(3, 10)
                factor_aleatorio = random.uniform(0.5, 1.5)
                pasos = int(velocidad_base * factor_aleatorio)
                
                # Efectos especiales ocasionales (Turbo boost)
                if random.random() < 0.1:  # 10% de probabilidad
                    pasos *= 2
                
                # Mover tortuga siguiendo la ruta
                for _ in range(pasos):
                    if not self.carrera_en_progreso:
                        break
                    
                    # Avanzar en la ruta
                    if self.tortuga_indices[i] < total_puntos - 1:
                        self.tortuga_indices[i] += 1
                        punto_actual = self.puntos_ruta[i][self.tortuga_indices[i]]
                        
                        # Calcular ángulo hacia el siguiente punto
                        x_actual, y_actual = tortuga.position()
                        x_objetivo, y_objetivo = punto_actual
                        
                        if x_objetivo != x_actual or y_objetivo != y_actual:
                            angulo = math.degrees(math.atan2(y_objetivo - y_actual, x_objetivo - x_actual))
                            tortuga.setheading(angulo)
                        
                        # Mover hacia el punto
                        tortuga.goto(x_objetivo, y_objetivo)
                        
                        if self.tortuga_indices[i] % 10 == 0:  # Actualizar nombres periódicamente
                            self.actualizar_nombres_flotantes()
                    else:
                        # Tortuga completó la ruta
                        self.ganador_carrera = i
                        self.carrera_en_progreso = False
                        break
                
                # Verificar progreso (prevenir carreras infinitas)
                if self.tortuga_indices[i] >= total_puntos * 0.95:  # 95% del recorrido
                    self.ganador_carrera = i
                    self.carrera_en_progreso = False
                    break
            
            # Actualizar pantalla
            self.screen.update()
            
            # Continuar la carrera si no ha terminado
            if self.carrera_en_progreso:
                self.root.after(10, self.simular_carrera)
            else:
                # Carrera terminada
                tiempo_final = time.time() - self.tiempo_inicio_carrera
                
                if self.ganador_carrera is not None:
                    self.mostrar_resultado_ganador(self.ganador_carrera, tiempo_final)
                    self.guardar_resultado_carrera(self.ganador_carrera, tiempo_final)
                else:
                    # Si no hay ganador, encontrar el más adelantado
                    ganador = max(range(len(self.tortugas)), key=lambda i: self.tortuga_indices[i])
                    self.mostrar_resultado_ganador(ganador, tiempo_final)
                    self.guardar_resultado_carrera(ganador, tiempo_final)
                
                # Mostrar botón de finalizar carrera
                self.btn_finalizar.pack(side="left", padx=(0, 10), after=self.btn_finalizar.master.winfo_children()[0])
                
                # Limpiar variables temporales
                delattr(self, 'tiempo_inicio_carrera')
                if hasattr(self, 'ganador_carrera'):
                    delattr(self, 'ganador_carrera')
    
    def mostrar_resultado_ganador(self, ganador, tiempo_carrera):
        """Muestra el resultado con efectos visuales"""
        nombre_ganador = self.nombres_tortugas[ganador]
        color_ganador = self.color_vars[ganador].get()
        
        # Efectos visuales de victoria
        tortuga_ganadora = self.tortugas[ganador]
        for _ in range(5):
            tortuga_ganadora.shapesize(2)
            self.screen.update()
            time.sleep(0.2)
            tortuga_ganadora.shapesize(1)
            self.screen.update()
            time.sleep(0.2)
        
        # Mensaje de victoria en pantalla
        victoria_turtle = turtle.Turtle()
        victoria_turtle.hideturtle()
        victoria_turtle.penup()
        victoria_turtle.goto(0, 0)
        victoria_turtle.color('#ffff00')
        
        # Fondo para el texto
        victoria_turtle.goto(-300, -50)
        victoria_turtle.pendown()
        victoria_turtle.fillcolor('#000000')
        victoria_turtle.begin_fill()
        for _ in range(2):
            victoria_turtle.forward(600)
            victoria_turtle.left(90)
            victoria_turtle.forward(100)
            victoria_turtle.left(90)
        victoria_turtle.end_fill()
        victoria_turtle.penup()
        
        # Texto de victoria
        victoria_turtle.goto(0, 0)
        victoria_turtle.write(f"🏆 ¡{nombre_ganador} GANA! 🏆", 
                            align="center", font=("Arial", 28, "bold"))
        
        victoria_turtle.goto(0, -30)
        victoria_turtle.color('#00d4ff')
        victoria_turtle.write(f"Tiempo: {tiempo_carrera:.2f}s | Mapa: {self.mapa_seleccionado}", 
                            align="center", font=("Arial", 14, "bold"))
        
        # Instrucción para cerrar
        victoria_turtle.goto(0, -280)
        victoria_turtle.color('#ffaa00')
        victoria_turtle.write("Presiona el botón 'Finalizar Carrera' para volver al menú", 
                            align="center", font=("Arial", 12, "bold"))
        
        # Mensaje de confirmación (sin bloquear)
        self.root.after(100, lambda: messagebox.showinfo("🏆 ¡Victoria!", 
                           f"🎉 ¡Felicidades!\n\n🏆 Ganador: {nombre_ganador}\n🎨 Color: {color_ganador}\n⏱️ Tiempo: {tiempo_carrera:.2f}s\n🗺️ Mapa: {self.mapa_seleccionado}"))
    
    def guardar_resultado_carrera(self, ganador, tiempo_carrera):
        """Guarda el resultado en el archivo de historial"""
        try:
            fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nombre_ganador = self.nombres_tortugas[ganador]
            color_ganador = self.color_vars[ganador].get()
            
            # Crear datos de la carrera
            resultado = {
                "fecha_hora": fecha_hora,
                "mapa": self.mapa_seleccionado,
                "participantes": [],
                "ganador": {
                    "nombre": nombre_ganador,
                    "color": color_ganador,
                    "posicion": ganador + 1
                },
                "tiempo_carrera": round(tiempo_carrera, 2),
                "num_participantes": len(self.tortugas)
            }
            
            # Añadir información de participantes
            for i, (nombre, color) in enumerate(zip(self.nombres_tortugas, self.color_vars)):
                resultado["participantes"].append({
                    "nombre": nombre.get() if hasattr(nombre, 'get') else nombre,
                    "color": color.get() if hasattr(color, 'get') else color,
                    "posicion": i + 1
                })
            
            # Leer historial existente
            historial = []
            if os.path.exists(self.archivo_historial):
                try:
                    with open(self.archivo_historial, 'r', encoding='utf-8') as f:
                        contenido = f.read().strip()
                        if contenido:
                            historial = json.loads(contenido)
                except (json.JSONDecodeError, FileNotFoundError):
                    historial = []
            
            # Añadir nuevo resultado
            historial.append(resultado)
            
            # Guardar historial actualizado
            with open(self.archivo_historial, 'w', encoding='utf-8') as f:
                json.dump(historial, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el resultado:\n{str(e)}")
    
    def mostrar_historial(self):
        """Muestra el historial de carreras en una ventana moderna"""
        try:
            if not os.path.exists(self.archivo_historial):
                messagebox.showinfo("📊 Historial", "No hay carreras registradas aún.")
                return
            
            with open(self.archivo_historial, 'r', encoding='utf-8') as f:
                contenido = f.read().strip()
                if not contenido:
                    messagebox.showinfo("📊 Historial", "No hay carreras registradas aún.")
                    return
                
                historial = json.loads(contenido)
            
            # Crear ventana de historial
            import tkinter as tk
            ventana_historial = ctk.CTkToplevel(self.root)
            ventana_historial.title("📊 Historial de Carreras")
            ventana_historial.geometry("900x700")
            
            # Frame principal
            main_frame = ctk.CTkFrame(ventana_historial, corner_radius=15)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Título
            ctk.CTkLabel(
                main_frame,
                text="📊 HISTORIAL DE CARRERAS",
                font=("Segoe UI", 24, "bold")
            ).pack(pady=(10, 20))
            
            # Área de texto con scroll usando CTkTextbox
            text_historial = ctk.CTkTextbox(
                main_frame,
                width=850,
                height=500,
                font=("Consolas", 11),
                wrap="word"
            )
            text_historial.pack(fill="both", expand=True, padx=10, pady=(0, 15))
            
            # Mostrar historial
            text_historial.insert("1.0", "🏁 HISTORIAL COMPLETO DE CARRERAS 🏁\n")
            text_historial.insert("end", "="*60 + "\n\n")
            
            for i, carrera in enumerate(reversed(historial), 1):
                text_historial.insert("end", f"🏆 CARRERA #{len(historial) - i + 1}\n")
                text_historial.insert("end", f"📅 Fecha: {carrera['fecha_hora']}\n")
                text_historial.insert("end", f"🗺️  Mapa: {carrera.get('mapa', 'N/A')}\n")
                text_historial.insert("end", f"⏱️  Duración: {carrera['tiempo_carrera']} segundos\n")
                text_historial.insert("end", f"👥 Participantes: {carrera['num_participantes']}\n\n")
                
                text_historial.insert("end", "🏆 GANADOR:\n")
                text_historial.insert("end", f"   🐢 {carrera['ganador']['nombre']}\n")
                text_historial.insert("end", f"   🎨 Color: {carrera['ganador']['color']}\n\n")
                
                text_historial.insert("end", "👥 TODOS LOS PARTICIPANTES:\n")
                for j, participante in enumerate(carrera['participantes'], 1):
                    text_historial.insert("end", f"   {j}. 🐢 {participante['nombre']} - {participante['color']}\n")
                
                text_historial.insert("end", "\n" + "-"*50 + "\n\n")
            
            # Estadísticas
            text_historial.insert("end", "📈 ESTADÍSTICAS GENERALES:\n")
            text_historial.insert("end", f"• Total de carreras: {len(historial)}\n")
            
            if historial:
                tiempo_promedio = sum(c['tiempo_carrera'] for c in historial) / len(historial)
                text_historial.insert("end", f"• Tiempo promedio: {tiempo_promedio:.2f} segundos\n")
                
                # Ganador más frecuente
                ganadores = {}
                for carrera in historial:
                    nombre = carrera['ganador']['nombre']
                    ganadores[nombre] = ganadores.get(nombre, 0) + 1
                
                if ganadores:
                    mejor_corredor = max(ganadores.items(), key=lambda x: x[1])
                    text_historial.insert("end", f"• Mejor corredor: {mejor_corredor[0]} ({mejor_corredor[1]} victorias)\n")
            
            # Deshabilitar edición
            text_historial.configure(state="disabled")
            
            # Botón cerrar
            ctk.CTkButton(
                main_frame,
                text="❌ Cerrar",
                command=ventana_historial.destroy,
                width=120,
                height=35,
                fg_color="#ff0000"
            ).pack(pady=(10, 10))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar historial:\n{str(e)}")
    
    def limpiar_historial(self):
        """Limpia el historial de carreras"""
        respuesta = messagebox.askyesno("🗑️ Limpiar Historial", 
                                       "¿Estás seguro de que quieres eliminar todo el historial de carreras?\n\nEsta acción no se puede deshacer.")
        if respuesta:
            try:
                if os.path.exists(self.archivo_historial):
                    os.remove(self.archivo_historial)
                messagebox.showinfo("✅ Éxito", "Historial limpiado correctamente.")
            except Exception as e:
                messagebox.showerror("❌ Error", f"No se pudo limpiar el historial:\n{str(e)}")
    
    def cancelar_carrera_sin_guardar(self):
        """Cancela la carrera en progreso sin guardar datos"""
        # Detener la carrera PRIMERO (esto evita el mensaje de "carrera en progreso")
        self.carrera_en_progreso = False
        
        # Limpiar variables temporales sin guardar
        if hasattr(self, 'tiempo_inicio_carrera'):
            delattr(self, 'tiempo_inicio_carrera')
        if hasattr(self, 'ganador_carrera'):
            delattr(self, 'ganador_carrera')
        
        # Limpiar tortugas y labels
        if hasattr(self, 'tortugas'):
            for tortuga in self.tortugas:
                try:
                    tortuga.hideturtle()
                except:
                    pass
            self.tortugas = []
        
        if hasattr(self, 'labels_nombres'):
            for label in self.labels_nombres:
                try:
                    label.clear()
                    label.hideturtle()
                except:
                    pass
            self.labels_nombres = []
        
        # Cerrar ventana de turtle
        try:
            if self.screen:
                self.screen.bye()
                self.screen = None
        except:
            pass
        
        # Ocultar botón de finalizar
        try:
            self.btn_finalizar.pack_forget()
        except:
            pass
        
        # Resetear estado completamente
        self.pista_creada = False
        self.nombres_tortugas = []
        self.tortuga_indices = []
        self.puntos_ruta = []
    
    def finalizar_carrera(self):
        """Finaliza la carrera y limpia la pantalla de turtle"""
        self.carrera_en_progreso = False
        
        # Limpiar la pantalla de turtle
        self.screen.clear()
        self.screen.bgcolor('#1a1a2e')
        
        # Limpiar tortugas y labels
        if hasattr(self, 'tortugas'):
            for tortuga in self.tortugas:
                tortuga.hideturtle()
            self.tortugas = []
        
        if hasattr(self, 'labels_nombres'):
            for label in self.labels_nombres:
                label.clear()
                label.hideturtle()
            self.labels_nombres = []
        
        # Ocultar botón de finalizar
        self.btn_finalizar.pack_forget()
        
        # Resetear estado
        self.pista_creada = False
        self.nombres_tortugas = []
        self.tortuga_indices = []
        
        messagebox.showinfo("✅ Carrera Finalizada", "La carrera ha sido finalizada. Puedes iniciar una nueva carrera.")
    
    def iniciar_carrera(self):
        """Inicia una nueva carrera"""
        # Verificar si hay carrera en progreso
        if self.carrera_en_progreso:
            messagebox.showwarning("⚠️ Carrera en Progreso", "Ya hay una carrera en progreso. Espera a que termine o cierra la ventana de la carrera.")
            return
        
        try:
            # Validar configuración
            num_tortugas = int(self.num_tortugas_var.get())
            if not (2 <= num_tortugas <= 6):
                messagebox.showerror("❌ Error", "El número de tortugas debe estar entre 2 y 6.")
                return
            
            # Validar nombres únicos
            nombres = [entry.get().strip() for entry in self.tortuga_entries]
            if len(set(nombres)) != len(nombres):
                messagebox.showerror("❌ Error", "Todos los nombres de las tortugas deben ser únicos.")
                return
            
            if any(not nombre for nombre in nombres):
                messagebox.showerror("❌ Error", "Todos los nombres de las tortugas deben estar completos.")
                return
            
            # Cerrar ventana anterior si existe
            try:
                if self.screen:
                    self.screen.bye()
                    self.screen = None
            except:
                self.screen = None
            
            # Crear nueva ventana de turtle
            self.screen = turtle.Screen()
            self.screen.tracer(0)
            
            # Configurar evento de cierre ANTES de crear la pista
            def on_closing():
                """Maneja el cierre de la ventana de turtle sin guardar"""
                try:
                    # Cancelar carrera sin guardar datos
                    self.carrera_en_progreso = False
                    
                    # Limpiar variables
                    if hasattr(self, 'tiempo_inicio_carrera'):
                        delattr(self, 'tiempo_inicio_carrera')
                    if hasattr(self, 'ganador_carrera'):
                        delattr(self, 'ganador_carrera')
                    
                    # Resetear estado
                    self.pista_creada = False
                    self.nombres_tortugas = []
                    self.tortuga_indices = []
                    self.tortugas = []
                    self.labels_nombres = []
                    
                    # Ocultar botón finalizar
                    try:
                        self.btn_finalizar.pack_forget()
                    except:
                        pass
                    
                    # Cerrar ventana
                    try:
                        self.screen.bye()
                    except:
                        pass
                    
                    self.screen = None
                except:
                    pass
            
            # Registrar el evento de cierre
            try:
                canvas = self.screen.getcanvas()
                root_window = canvas.winfo_toplevel()
                root_window.protocol("WM_DELETE_WINDOW", on_closing)
            except Exception as e:
                print(f"No se pudo registrar el evento de cierre: {e}")
            
            # Crear pista y tortugas
            self.crear_pista_compleja()
            self.crear_tortugas_participantes()
            
            self.screen.update()
            
            # Iniciar carrera
            self.root.after(100, self.simular_carrera)
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al iniciar carrera:\n{str(e)}")
            self.carrera_en_progreso = False
            try:
                if self.screen:
                    self.screen.bye()
                    self.screen = None
            except:
                pass

def main():
    """Función principal"""
    print("🏁 Iniciando Simulador de Carreras de Tortugas - Versión Pro")
    print("=" * 60)
    print("🐢 Características:")
    print("• Interfaz moderna con colores metálicos")
    print("• Mapas complejos de carretera")
    print("• Nombres flotantes personalizables")
    print("• Sistema de historial avanzado")
    print("• Animaciones fluidas")
    print("=" * 60)
    
    try:
        carrera = CarreraModerna()
        carrera.crear_interfaz_principal()
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        messagebox.showerror("Error Crítico", f"No se pudo iniciar la aplicación:\n{str(e)}")

if __name__ == "__main__":
    main()