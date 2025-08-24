import tkinter as tk
from tkinter import messagebox
import random
import string
import json
import os

# ================== ARCHIVO DE USUARIOS ==================
ARCHIVO_USUARIOS = "usuarios.json"

def cargar_usuarios():
    if os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS, "r") as f:
            return json.load(f)
    return {}

def guardar_usuarios():
    with open(ARCHIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)

usuarios = cargar_usuarios()

# ================== GENERADOR DE CONTRASEÑAS ==================
def generar_contraseña(longitud):
    if longitud < 4:
        return None  # No válido

    mayusculas = string.ascii_uppercase
    minusculas = string.ascii_lowercase
    numeros = string.digits
    simbolos = string.punctuation

    # Asegurar al menos uno de cada tipo
    contraseña = [
        random.choice(mayusculas),
        random.choice(minusculas),
        random.choice(numeros),
        random.choice(simbolos)
    ]

    # Completar el resto
    todos = mayusculas + minusculas + numeros + simbolos
    contraseña += [random.choice(todos) for _ in range(longitud - 4)]
    random.shuffle(contraseña)
    return ''.join(contraseña)

# ================== INTERFAZ PRINCIPAL ==================
ventana = tk.Tk()
ventana.title("Gestor Seguro de Contraseñas")
ventana.geometry("500x400")
ventana.configure(bg="#fcefee")  # Color pastel rosado

# ================== FUNCIONES DE INTERFAZ ==================
def mostrar_menu():
    limpiar_ventana()

    titulo = tk.Label(ventana, text="Menú Principal", font=("Arial", 16, "bold"), bg="#fcefee", fg="#444")
    titulo.pack(pady=20)

    btn1 = tk.Button(ventana, text="1. Generar contraseña para un usuario", command=menu_usuario, bg="#a8dadc", fg="#000")
    btn1.pack(pady=10, ipadx=10, ipady=5)

    btn2 = tk.Button(ventana, text="2. Generar contraseña sin usuario", command=menu_sin_usuario, bg="#ffd6a5", fg="#000")
    btn2.pack(pady=10, ipadx=10, ipady=5)

    btn3 = tk.Button(ventana, text="3. Crear nuevo usuario", command=menu_crear_usuario, bg="#caffbf", fg="#000")
    btn3.pack(pady=10, ipadx=10, ipady=5)

def menu_usuario():
    limpiar_ventana()

    tk.Label(ventana, text="Nombre de usuario:", bg="#fcefee").pack()
    entry_user = tk.Entry(ventana)
    entry_user.pack()

    tk.Label(ventana, text="Contraseña de usuario:", bg="#fcefee").pack()
    entry_pass = tk.Entry(ventana, show="*")
    entry_pass.pack()

    def verificar_usuario():
        usuario = entry_user.get()
        password = entry_pass.get()

        if usuario in usuarios and usuarios[usuario]["password"] == password:
            generar_para_usuario(usuario)
        else:
            messagebox.showerror("Error", "Usuario no encontrado o contraseña incorrecta")

    tk.Button(ventana, text="Ingresar", command=verificar_usuario, bg="#a8dadc").pack(pady=10)
    tk.Button(ventana, text="Volver", command=mostrar_menu, bg="#ffd6a5").pack()

def generar_para_usuario(usuario):
    limpiar_ventana()

    tk.Label(ventana, text=f"Generar contraseña para {usuario}", bg="#fcefee").pack()

    tk.Label(ventana, text="Longitud:", bg="#fcefee").pack()
    entry_long = tk.Entry(ventana)
    entry_long.pack()

    resultado = tk.Text(ventana, height=2, width=30, wrap="word")
    resultado.pack(pady=5)

    def generar():
        try:
            longitud = int(entry_long.get())
            pwd = generar_contraseña(longitud)
            if not pwd:
                messagebox.showerror("Error", "La longitud mínima es 4")
                return
            resultado.delete("1.0", tk.END)
            resultado.insert(tk.END, pwd)
        except:
            messagebox.showerror("Error", "Ingrese un número válido")

    def guardar():
        pwd = resultado.get("1.0", tk.END).strip()
        if pwd:
            usuarios[usuario]["historial"].append(pwd)
            guardar_usuarios()
            messagebox.showinfo("Guardado", "Contraseña guardada exitosamente")
        else:
            messagebox.showwarning("Aviso", "No hay contraseña generada")

    tk.Button(ventana, text="Generar", command=generar, bg="#caffbf").pack(pady=5)
    tk.Button(ventana, text="Guardar", command=guardar, bg="#a8dadc").pack(pady=5)

    tk.Label(ventana, text="Historial:", bg="#fcefee").pack()
    historial = tk.Text(ventana, height=5, width=40)
    historial.pack()
    historial.insert(tk.END, "\n".join(usuarios[usuario]["historial"]))
    historial.config(state="disabled")

    tk.Button(ventana, text="Volver", command=mostrar_menu, bg="#ffd6a5").pack(pady=5)

def menu_sin_usuario():
    limpiar_ventana()

    tk.Label(ventana, text="Generar contraseña (sin usuario)", bg="#fcefee").pack()

    tk.Label(ventana, text="Longitud:", bg="#fcefee").pack()
    entry_long = tk.Entry(ventana)
    entry_long.pack()

    resultado = tk.Text(ventana, height=2, width=30, wrap="word")
    resultado.pack(pady=5)

    def generar():
        try:
            longitud = int(entry_long.get())
            pwd = generar_contraseña(longitud)
            if not pwd:
                messagebox.showerror("Error", "La longitud mínima es 4")
                return
            resultado.delete("1.0", tk.END)
            resultado.insert(tk.END, pwd)
        except:
            messagebox.showerror("Error", "Ingrese un número válido")

    tk.Button(ventana, text="Generar", command=generar, bg="#caffbf").pack(pady=5)
    tk.Button(ventana, text="Volver", command=mostrar_menu, bg="#ffd6a5").pack(pady=5)

def menu_crear_usuario():
    limpiar_ventana()

    tk.Label(ventana, text="Crear nuevo usuario", bg="#fcefee").pack()

    tk.Label(ventana, text="Nombre de usuario:", bg="#fcefee").pack()
    entry_user = tk.Entry(ventana)
    entry_user.pack()

    tk.Label(ventana, text="Contraseña:", bg="#fcefee").pack()
    entry_pass = tk.Entry(ventana, show="*")
    entry_pass.pack()

    def guardar_usuario():
        usuario = entry_user.get()
        password = entry_pass.get()

        if not usuario or not password:
            messagebox.showerror("Error", "Complete todos los campos")
            return

        if usuario in usuarios:
            messagebox.showerror("Error", "Ese usuario ya existe")
            return

        usuarios[usuario] = {"password": password, "historial": []}
        guardar_usuarios()
        messagebox.showinfo("Éxito", "Usuario creado correctamente")
        mostrar_menu()

    tk.Button(ventana, text="Guardar usuario", command=guardar_usuario, bg="#caffbf").pack(pady=10)
    tk.Button(ventana, text="Volver", command=mostrar_menu, bg="#ffd6a5").pack()

# ================== LIMPIAR VENTANA ==================
def limpiar_ventana():
    for widget in ventana.winfo_children():
        widget.destroy()

# ================== INICIO ==================
mostrar_menu()
ventana.mainloop()
