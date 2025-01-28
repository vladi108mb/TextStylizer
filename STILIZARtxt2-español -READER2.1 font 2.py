import spacy
import tkinter as tk
from tkinter import filedialog, scrolledtext
from tkinter import messagebox
import tkinter.font as tkFont

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Text Stylizer - Estilizador de texto (Español)")
ventana.geometry("1180x600")  # Ajustar para que sea más horizontal
ventana.configure(bg="#f0f0f0")

# Cargar modelo de spaCy en español
nlp = spacy.load("es_core_news_sm")

# Estilos universales
style_rules = {
    "ADJ": {"color": "#32CD32", "font_size": 18, "font_family": "Open Sans SemiBold"},
    "ADP": {"color": "#1E90FF", "font_size": 18, "font_family": "Open Sans SemiBold"},
    "ADV": {"color": "#0000FF", "font_size": 18, "font_family": "Open Sans SemiBold"},
    "VERB": {"color": "#FF00FF", "font_size": 18, "font_family": "Open Sans SemiBold"},
    "CCONJ": {"color": "#000000", "font_size": 18, "font_family": "Open Sans SemiBold"},
    "PART": {"color": "#666666", "font_size": 18, "font_family": "Open Sans SemiBold"},
    "DET": {"color": "#777777", "font_size": 18, "font_family": "Open Sans SemiBold"},
    "AUX": {"color": "#888888", "font_size": 18, "font_family": "Open Sans SemiBold"},
    "NOUN": {"color": "#00BFFF", "font_size": 18, "font_family": "Open Sans SemiBold"},
    "PUNCT": {"color": "#000000", "font_size": 18, "font_family": "Open Sans SemiBold"},
    "NUM": {"color": "#00BFFF", "font_size": 18, "font_family": "Open Sans SemiBold"},
    "SCONJ": {"color": "#777777", "font_size": 18, "font_family": "Open Sans SemiBold"},
    "PRON": {"color": "#888888", "font_size": 18, "font_family": "Open Sans SemiBold"},
    "PROPN": {"color": "#FF4500", "font_size": 20, "font_family": "Open Sans SemiBold"},
}

# Variable para almacenar qué reglas se seleccionan
selected_rules = {}

# Funciones

def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, "r", encoding="utf-8") as file:
            texto = file.read()
            entrada_texto.delete("1.0", tk.END)
            entrada_texto.insert(tk.END, texto)

def procesar_texto():
    texto = entrada_texto.get("1.0", tk.END)
    if not texto.strip():
        messagebox.showwarning("Advertencia", "Por favor, carga un archivo o ingresa texto.")
        return

    # Actualizar las reglas seleccionadas antes de procesar
    reglas_activas = {key: var.get() for key, var in selected_rules.items()}

    doc_spacy = nlp(texto)
    salida_texto.delete("1.0", tk.END)

    for token in doc_spacy:
        if reglas_activas.get(token.pos_, False):
            style = style_rules.get(token.pos_, {})
            color = style.get("color", "#000000")
            font_size = style.get("font_size", 18)
            font_family = style.get("font_family", "Open Sans SemiBold")

            salida_texto.tag_configure(
                token.pos_, foreground=color, font=(font_family, font_size)
            )
            salida_texto.insert(tk.END, token.text + " ", token.pos_)
        else:
            salida_texto.insert(tk.END, token.text + " ")

    messagebox.showinfo("Proceso completado", "El texto ha sido procesado y estilizado.")

def crear_checkboxes():
    posiciones = list(style_rules.keys())
    primera_fila = posiciones[:7]  # Primera fila con 7 checkboxes
    segunda_fila = posiciones[7:]  # Segunda fila con el resto

    for col, pos_tag in enumerate(primera_fila):
        var = tk.BooleanVar(value=True)
        selected_rules[pos_tag] = var
        checkbox = tk.Checkbutton(
            reglas_frame,
            text=pos_tag,
            variable=var,
            bg="#f0f0f0",
            font=("Arial", 12),
        )
        checkbox.grid(row=0, column=col, sticky="w", padx=2, pady=2)

    for col, pos_tag in enumerate(segunda_fila):
        var = tk.BooleanVar(value=True)
        selected_rules[pos_tag] = var
        checkbox = tk.Checkbutton(
            reglas_frame,
            text=pos_tag,
            variable=var,
            bg="#f0f0f0",
            font=("Arial", 12),
        )
        checkbox.grid(row=1, column=col, sticky="w", padx=2, pady=2)

# Diseño de la interfaz

# Frame para la columna izquierda (texto original)
frame_izquierda = tk.Frame(ventana, bg="#f0f0f0")
frame_izquierda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Texto original
entrada_texto = scrolledtext.ScrolledText(
    frame_izquierda,
    wrap=tk.WORD,
    width=50,
    height=18,
    font=("Arial", 12),
    bg="#ffffff"
)
entrada_texto.pack(fill=tk.BOTH, expand=True)

# Botones en la parte inferior de la columna izquierda
botones_frame = tk.Frame(frame_izquierda, bg="#f0f0f0")
botones_frame.pack(fill=tk.X, pady=5)

boton_cargar = tk.Button(
    botones_frame,
    text="Cargar archivo",
    command=cargar_archivo,
    font=("Arial", 12),
    bg="#4CAF50",
    fg="white",
    padx=10,
    pady=5,
)
boton_cargar.pack(side=tk.LEFT, padx=5)

boton_procesar = tk.Button(
    botones_frame,
    text="Procesar texto",
    command=procesar_texto,
    font=("Arial", 12),
    bg="#2196F3",
    fg="white",
    padx=10,
    pady=5,
)
boton_procesar.pack(side=tk.RIGHT, padx=5)

# Frame para checkboxes
reglas_frame = tk.LabelFrame(frame_izquierda, text="Seleccionar reglas de estilo", bg="#f0f0f0", font=("Arial", 12))
reglas_frame.pack(fill=tk.X, padx=5, pady=10)
crear_checkboxes()

# Frame para la columna derecha (texto procesado)
frame_derecha = tk.Frame(ventana, bg="#f0f0f0")
frame_derecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Texto procesado
salida_texto = scrolledtext.ScrolledText(
    frame_derecha,
    wrap=tk.WORD,
    width=50,
    height=18,
    font=("Open Sans SemiBold", 12),
    bg="#ffffff"
)
salida_texto.pack(fill=tk.BOTH, expand=True)

ventana.mainloop()