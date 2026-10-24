import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import calendar


NEGRO = "#100D16"
MORADO_OSCURO = "#1B1426"
MORADO = "#7928CA"
MORADO_CLARO = "#A855F7"
BLANCO = "#F5F0FF"
GRIS = "#C4B8D8"
ROJO = "#D9365B"


class EstructuraDatosAfiliado:
    def __init__(
        self, tipo_id, numero_id, nombre, ingresos,
        servicio, modalidad, tarifa, fecha
    ):
        self.tipo_id = tipo_id
        self.numero_id = numero_id
        self.nombre = nombre
        self.ingresos = ingresos
        self.servicio = servicio
        self.modalidad = modalidad
        self.tarifa = tarifa
        self.fecha = fecha

    def obtener_datos(self):
        return (
            self.tipo_id,
            self.numero_id,
            self.nombre,
            f"${self.ingresos:,.0f}",
            self.servicio,
            self.modalidad,
            f"${self.tarifa:,.0f}",
            self.fecha
        )

pila = []
cola = []
lista_afiliados = []

ventana = tk.Tk()
ventana.title("Compensándote - Inicio de sesión")
ventana.geometry("460x420")
ventana.resizable(False, False)
ventana.configure(bg=NEGRO)


def mostrar_about(parent):
    about = tk.Toplevel(parent)
    about.title("About")
    about.geometry("390x280")
    about.configure(bg=NEGRO)
    about.resizable(False, False)

    tk.Label(
        about,
        text="ACERCA DE COMPENSÁNDOTE",
        font=("Arial", 14, "bold"),
        bg=NEGRO,
        fg=MORADO_CLARO
    ).pack(pady=15)

    datos = [
        "Course: Data Structures — 301305",
        "Student: Andrea Redondo",
        "Collaborative Group: 301305A_2204",
        "UNAD · ECBTI · Systems Engineering",
        "October 2026"
    ]

    for dato in datos:
        tk.Label(
            about,
            text=dato,
            font=("Arial", 9),
            bg=NEGRO,
            fg=BLANCO,
            wraplength=360
        ).pack(pady=5)

    tk.Button(
        about,
        text="Aceptar",
        command=about.destroy,
        bg=MORADO,
        fg=BLANCO,
        activebackground=MORADO_CLARO,
        relief="flat"
    ).pack(pady=10)

def abrir_menu():
    ventana.withdraw()

    menu = tk.Toplevel(ventana)
    menu.title("Caja Compensándote - Control de Afiliados")
    menu.geometry("1200x760")
    menu.minsize(1000, 650)
    menu.configure(bg=NEGRO)

    menu.protocol("WM_DELETE_WINDOW", ventana.destroy)

    estilo = ttk.Style(menu)
    estilo.theme_use("clam")

    estilo.configure(
        "TCombobox",
        fieldbackground=MORADO_OSCURO,
        background=MORADO,
        foreground=BLANCO,
        arrowcolor=BLANCO
    )

    estilo.configure(
        "Treeview",
        background=MORADO_OSCURO,
        foreground=BLANCO,
        fieldbackground=MORADO_OSCURO,
        rowheight=28,
        font=("Arial", 9)
    )

    estilo.configure(
        "Treeview.Heading",
        background=MORADO,
        foreground=BLANCO,
        font=("Arial", 9, "bold")
    )

    estilo.map(
        "Treeview",
        background=[("selected", MORADO_CLARO)],
        foreground=[("selected", BLANCO)]
    )

    barra = tk.Frame(menu, bg=MORADO_OSCURO)
    barra.pack(fill="x")

    tk.Button(
        barra,
        text="About",
        command=lambda: mostrar_about(menu),
        bg=MORADO_OSCURO,
        fg=MORADO_CLARO,
        activebackground=MORADO,
        activeforeground=BLANCO,
        relief="flat",
        font=("Arial", 10, "bold")
    ).pack(side="left", padx=12, pady=8)

    tk.Label(
        menu,
        text="CAJA COMPENSÁNDOTE – CONTROL DE AFILIADOS",
        font=("Arial", 20, "bold"),
        bg=NEGRO,
        fg=MORADO_CLARO
    ).pack(pady=15)

    formulario = tk.LabelFrame(
        menu,
        text="Datos del afiliado",
        bg=NEGRO,
        fg=MORADO_CLARO,
        font=("Arial", 11, "bold"),
        padx=12,
        pady=10
    )
    formulario.pack(fill="x", padx=15, pady=5)

    formulario.columnconfigure(1, weight=1)
    formulario.columnconfigure(3, weight=1)

    def etiqueta(texto, fila, columna):
        tk.Label(
            formulario,
            text=texto,
            bg=NEGRO,
            fg=BLANCO,
            font=("Arial", 9)
        ).grid(
            row=fila,
            column=columna,
            sticky="w",
            padx=6,
            pady=5
        )

    def entrada_texto(fila, columna, ancho=24):
        campo = tk.Entry(
            formulario,
            width=ancho,
            bg=MORADO_OSCURO,
            fg=BLANCO,
            insertbackground=BLANCO,
            relief="flat"
        )
        campo.grid(
            row=fila,
            column=columna,
            sticky="ew",
            padx=6,
            pady=5
        )
        return campo

    etiqueta("Tipo de identificación:", 0, 0)

    tipo_id = ttk.Combobox(
        formulario,
        values=["CC", "CE", "NUIP", "PAS"],
        state="readonly",
        width=21
    )
    tipo_id.grid(row=0, column=1, sticky="ew", padx=6, pady=5)

    etiqueta("Número de identificación:", 0, 2)
    numero_id = entrada_texto(0, 3)

    etiqueta("Nombre completo:", 1, 0)
    nombre = entrada_texto(1, 1)

    etiqueta("Ingresos actuales ($):", 1, 2)
    ingresos = entrada_texto(1, 3)

    etiqueta("Servicio deseado:", 2, 0)

    servicios = [
        "Subsidio de desempleo",
        "Ingreso a parque",
        "Curso de formación",
        "Paquete de viaje",
        "Medicina preventiva"
    ]

    servicio = ttk.Combobox(
        formulario,
        values=servicios,
        state="readonly",
        width=21
    )
    servicio.grid(row=2, column=1, sticky="ew", padx=6, pady=5)

    etiqueta("Modalidad de empleo:", 2, 2)

    modalidad = tk.StringVar(value="Empleado")

    marco_radio = tk.Frame(formulario, bg=NEGRO)
    marco_radio.grid(row=2, column=3, sticky="w", padx=6)

    tk.Radiobutton(
        marco_radio,
        text="Empleado",
        variable=modalidad,
        value="Empleado",
        bg=NEGRO,
        fg=BLANCO,
        selectcolor=MORADO_OSCURO,
        activebackground=NEGRO,
        activeforeground=MORADO_CLARO
    ).pack(side="left")

    tk.Radiobutton(
        marco_radio,
        text="Independiente",
        variable=modalidad,
        value="Independiente",
        bg=NEGRO,
        fg=BLANCO,
        selectcolor=MORADO_OSCURO,
        activebackground=NEGRO,
        activeforeground=MORADO_CLARO
    ).pack(side="left")

    etiqueta("Tarifa de afiliación:", 3, 0)

    tarifa_var = tk.StringVar()

    campo_tarifa = tk.Entry(
        formulario,
        textvariable=tarifa_var,
        state="readonly",
        readonlybackground=MORADO_OSCURO,
        fg=MORADO_CLARO,
        relief="flat"
    )
    campo_tarifa.grid(
        row=3, column=1, sticky="ew", padx=6, pady=5
    )

    etiqueta("Fecha de afiliación:", 3, 2)

    marco_fecha = tk.Frame(formulario, bg=NEGRO)
    marco_fecha.grid(row=3, column=3, sticky="w", padx=6)

    hoy = date.today()

    dia_var = tk.StringVar(value=f"{hoy.day:02d}")
    mes_var = tk.StringVar(value=f"{hoy.month:02d}")
    anio_var = tk.StringVar(value=str(hoy.year))

    tk.Spinbox(
        marco_fecha, from_=1, to=31, width=3,
        textvariable=dia_var, format="%02.0f",
        bg=MORADO_OSCURO, fg=BLANCO,
        buttonbackground=MORADO
    ).pack(side="left")

    tk.Label(
        marco_fecha, text="/",
        bg=NEGRO, fg=BLANCO
    ).pack(side="left")

    tk.Spinbox(
        marco_fecha, from_=1, to=12, width=3,
        textvariable=mes_var, format="%02.0f",
        bg=MORADO_OSCURO, fg=BLANCO,
        buttonbackground=MORADO
    ).pack(side="left")

    tk.Label(
        marco_fecha, text="/",
        bg=NEGRO, fg=BLANCO
    ).pack(side="left")

    tk.Spinbox(
        marco_fecha, from_=1900, to=2100, width=5,
        textvariable=anio_var,
        bg=MORADO_OSCURO, fg=BLANCO,
        buttonbackground=MORADO
    ).pack(side="left")

    def validar_numero(nuevo):
        return nuevo.isdigit() or nuevo == ""

    def validar_nombre(nuevo):
        return (
            all(caracter.isalpha() or caracter.isspace()
                for caracter in nuevo)
            or nuevo == ""
        )

    validar_num = (
        menu.register(validar_numero), "%P"
    )
    validar_nom = (
        menu.register(validar_nombre), "%P"
    )

    numero_id.configure(validate="key", validatecommand=validar_num)
    ingresos.configure(validate="key", validatecommand=validar_num)
    nombre.configure(validate="key", validatecommand=validar_nom)


    def calcular_tarifa(*args):
        tarifa_var.set("")

        texto_ingresos = ingresos.get()

        if not texto_ingresos.isdigit():
            return

        valor = int(texto_ingresos)

        if valor < 1_000_000:
            return

        if modalidad.get() == "Empleado":
            tarifas = [45000, 60000, 75000, 90000, 150000]
        else:
            tarifas = [10000, 20000, 30000, 40000, 80000]

        if valor <= 2_000_000:
            base = tarifas[0]
        elif valor <= 3_000_000:
            base = tarifas[1]
        elif valor <= 4_000_000:
            base = tarifas[2]
        elif valor <= 5_000_000:
            base = tarifas[3]
        else:
            base = tarifas[4]

        servicio_elegido = servicio.get()

        if servicio_elegido == "Ingreso a parque":
            base += 2500

        elif servicio_elegido == "Curso de formación":
            base += 7500

        elif servicio_elegido == "Paquete de viaje":
            base += 10000

        elif servicio_elegido == "Medicina preventiva":
            base += valor * 0.10

        tarifa_var.set(f"${base:,.0f}")

    ingresos.bind("<KeyRelease>", calcular_tarifa)
    servicio.bind("<<ComboboxSelected>>", calcular_tarifa)


    etiqueta("Ver estructura:", 4, 0)

    estructura = ttk.Combobox(
        formulario,
        values=["Pila", "Cola", "Lista"],
        state="readonly",
        width=21
    )
    estructura.grid(row=4, column=1, sticky="ew", padx=6, pady=5)
    estructura.set("Pila")

    etiqueta("Reporte:", 4, 2)

    reporte_var = tk.StringVar(value="Sin registros")

    campo_reporte = tk.Entry(
        formulario,
        textvariable=reporte_var,
        state="readonly",
        readonlybackground=MORADO_OSCURO,
        fg=MORADO_CLARO,
        relief="flat"
    )
    campo_reporte.grid(
        row=4, column=3, sticky="ew", padx=6, pady=5
    )


    marco_tabla = tk.Frame(menu, bg=NEGRO)
    marco_tabla.pack(fill="both", expand=True, padx=15, pady=10)

    columnas = (
        "tipo", "identificacion", "nombre", "ingresos",
        "servicio", "modalidad", "tarifa", "fecha"
    )

    tabla = ttk.Treeview(
        marco_tabla,
        columns=columnas,
        show="headings",
        height=9
    )

    encabezados = {
        "tipo": "Tipo ID",
        "identificacion": "Identificación",
        "nombre": "Nombre completo",
        "ingresos": "Ingresos",
        "servicio": "Servicio",
        "modalidad": "Modalidad",
        "tarifa": "Tarifa",
        "fecha": "Fecha"
    }

    anchos = {
        "tipo": 65,
        "identificacion": 105,
        "nombre": 150,
        "ingresos": 100,
        "servicio": 170,
        "modalidad": 105,
        "tarifa": 90,
        "fecha": 95
    }

    for columna in columnas:
        tabla.heading(columna, text=encabezados[columna])
        tabla.column(
            columna,
            width=anchos[columna],
            minwidth=60,
            anchor="center"
        )

    scroll_y = ttk.Scrollbar(
        marco_tabla, orient="vertical", command=tabla.yview
    )
    tabla.configure(yscrollcommand=scroll_y.set)

    tabla.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")


    def obtener_estructura():
        if estructura.get() == "Pila":
            return pila
        elif estructura.get() == "Cola":
            return cola
        return lista_afiliados

    def actualizar_tabla(*args):
        tabla.delete(*tabla.get_children())

        for afiliado in obtener_estructura():
            tabla.insert("", "end", values=afiliado.obtener_datos())

        actualizar_reporte()

    def actualizar_reporte():
        registros = obtener_estructura()

        if estructura.get() == "Pila":
            total = sum(a.tarifa for a in registros)
            reporte_var.set(f"Suma de tarifas: ${total:,.0f}")

        elif estructura.get() == "Cola":
            reporte_var.set(f"Cantidad de registros: {len(registros)}")

        else:
            if registros:
                promedio = sum(a.ingresos for a in registros) / len(registros)
                reporte_var.set(f"Promedio de ingresos: ${promedio:,.0f}")
            else:
                reporte_var.set("Promedio de ingresos: $0")

    estructura.bind("<<ComboboxSelected>>", actualizar_tabla)


    def registrar():
        tipo = tipo_id.get()
        identificacion = numero_id.get().strip()
        nombre_completo = nombre.get().strip()
        texto_ingresos = ingresos.get().strip()
        servicio_elegido = servicio.get()
        modalidad_elegida = modalidad.get()

        if not all([
            tipo, identificacion, nombre_completo,
            texto_ingresos, servicio_elegido
        ]):
            messagebox.showwarning(
                "Campos requeridos",
                "Diligencia todos los campos antes de registrar.",
                parent=menu
            )
            return

        valor_ingresos = int(texto_ingresos)

        if valor_ingresos < 1_000_000:
            messagebox.showwarning(
                "Ingresos inválidos",
                "Los ingresos deben ser de al menos $1.000.000.",
                parent=menu
            )
            return

        try:
            fecha = date(
                int(anio_var.get()),
                int(mes_var.get()),
                int(dia_var.get())
            )
        except ValueError:
            messagebox.showerror(
                "Fecha inválida",
                "Selecciona una fecha válida.",
                parent=menu
            )
            return

        calcular_tarifa()

        if not tarifa_var.get():
            messagebox.showwarning(
                "Tarifa pendiente",
                "No fue posible calcular la tarifa.",
                parent=menu
            )
            return

        valor_tarifa = float(
            tarifa_var.get().replace("$", "").replace(",", "")
        )

        afiliado = EstructuraDatosAfiliado(
            tipo,
            identificacion,
            nombre_completo,
            valor_ingresos,
            servicio_elegido,
            modalidad_elegida,
            valor_tarifa,
            fecha.strftime("%d/%m/%Y")
        )

        registros = obtener_estructura()
        registros.append(afiliado)

        actualizar_tabla()
        limpiar_campos()

        messagebox.showinfo(
            "Registro exitoso",
            "El afiliado fue registrado correctamente.",
            parent=menu
        )

    def limpiar_campos():
        tipo_id.set("")
        numero_id.delete(0, tk.END)
        nombre.delete(0, tk.END)
        ingresos.delete(0, tk.END)
        servicio.set("")
        modalidad.set("Empleado")
        tarifa_var.set("")

        hoy = date.today()
        dia_var.set(f"{hoy.day:02d}")
        mes_var.set(f"{hoy.month:02d}")
        anio_var.set(str(hoy.year))

    def mostrar_reporte():
        actualizar_reporte()
        messagebox.showinfo(
            "Reporte - " + estructura.get(),
            reporte_var.get(),
            parent=menu
        )


    def eliminar():
        registros = obtener_estructura()

        if not registros:
            messagebox.showwarning(
                "Sin registros",
                "No hay afiliados para eliminar en esta estructura.",
                parent=menu
            )
            return

        if estructura.get() == "Pila":
            afiliado = registros[-1]
            mensaje = (
                f"¿Deseas desapilar al último afiliado?\n"
                f"{afiliado.nombre} - {afiliado.numero_id}"
            )

            if messagebox.askyesno("Confirmar", mensaje, parent=menu):
                registros.pop()

        elif estructura.get() == "Cola":
            afiliado = registros[0]
            mensaje = (
                f"¿Deseas desencolar al primer afiliado?\n"
                f"{afiliado.nombre} - {afiliado.numero_id}"
            )

            if messagebox.askyesno("Confirmar", mensaje, parent=menu):
                registros.pop(0)

        else:
            identificacion = tk.simpledialog.askstring(
                "Eliminar afiliado",
                "Escribe el número de identificación:",
                parent=menu
            )

            if identificacion is None:
                return

            afiliado_encontrado = next(
                (
                    a for a in registros
                    if a.numero_id == identificacion.strip()
                ),
                None
            )

            if afiliado_encontrado is None:
                messagebox.showerror(
                    "No encontrado",
                    "No existe un afiliado con esa identificación.",
                    parent=menu
                )
                return

            confirmar = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Eliminar a {afiliado_encontrado.nombre}?",
                parent=menu
            )

            if confirmar:
                registros.remove(afiliado_encontrado)

        actualizar_tabla()

    marco_botones = tk.Frame(menu, bg=NEGRO)
    marco_botones.pack(pady=(0, 12))

    def boton_accion(texto, comando, color=MORADO):
        return tk.Button(
            marco_botones,
            text=texto,
            command=comando,
            width=13,
            font=("Arial", 10, "bold"),
            bg=color,
            fg=BLANCO,
            activebackground=MORADO_CLARO,
            activeforeground=BLANCO,
            relief="flat",
            cursor="hand2"
        )

    boton_accion("Registrar", registrar).pack(side="left", padx=5)
    boton_accion("Limpiar", limpiar_campos).pack(side="left", padx=5)
    boton_accion("Reporte", mostrar_reporte).pack(side="left", padx=5)
    boton_accion("Eliminar", eliminar).pack(side="left", padx=5)
    boton_accion("Salir", ventana.destroy, ROJO).pack(side="left", padx=5)

    actualizar_tabla()

tk.Label(
    ventana,
    text="◆",
    font=("Arial", 35, "bold"),
    bg=NEGRO,
    fg=MORADO_CLARO
).pack(pady=(20, 0))

tk.Label(
    ventana,
    text="COMPENSÁNDOTE",
    font=("Arial", 24, "bold"),
    bg=NEGRO,
    fg=MORADO_CLARO
).pack(pady=5)

tk.Label(
    ventana,
    text="Sistema de gestión de afiliados",
    font=("Arial", 11),
    bg=NEGRO,
    fg=GRIS
).pack(pady=(0, 25))

tk.Label(
    ventana,
    text="Ingrese la contraseña para continuar",
    font=("Arial", 10),
    bg=NEGRO,
    fg=BLANCO
).pack(pady=5)

entrada_contrasena = tk.Entry(
    ventana,
    show="*",
    width=28,
    font=("Arial", 12),
    bg=MORADO_OSCURO,
    fg=BLANCO,
    insertbackground=BLANCO,
    relief="flat",
    justify="center"
)
entrada_contrasena.pack(ipady=8, pady=10)


def iniciar_sesion():
    if entrada_contrasena.get() == "Caja":
        abrir_menu()
    else:
        messagebox.showerror(
            "Acceso denegado",
            "La contraseña es incorrecta.",
            parent=ventana
        )


entrada_contrasena.bind(
    "<Return>",
    lambda evento: iniciar_sesion()
)

tk.Button(
    ventana,
    text="INGRESAR",
    command=iniciar_sesion,
    font=("Arial", 11, "bold"),
    bg=MORADO,
    fg=BLANCO,
    activebackground=MORADO_CLARO,
    activeforeground=BLANCO,
    relief="flat",
    cursor="hand2",
    width=23,
    height=2
).pack(pady=15)

tk.Label(
    ventana,
    text="UNAD · ECBTI · Systems Engineering",
    font=("Arial", 9),
    bg=NEGRO,
    fg="#76658D"
).pack(side="bottom", pady=15)

ventana.mainloop()
