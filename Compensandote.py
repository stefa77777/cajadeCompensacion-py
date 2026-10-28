
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from collections import deque
from datetime import date
from tkcalendar import DateEntry


class EstructuraDatosAfiliado:
    def __init__(
        self,
        tipo_id,
        numero_id,
        nombre,
        ingresos,
        servicio,
        modalidad,
        tarifa,
        fecha
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
cola = deque()
lista_afiliados = []


FONDO = "#11111B"
PANEL = "#1E1E2E"
MORADO = "#8B5CF6"
MORADO_CLARO = "#A78BFA"
BLANCO = "#F8FAFC"
GRIS = "#CBD5E1"
VERDE = "#22C55E"
ROJO = "#EF4444"

ventana = tk.Tk()
ventana.title("Compensándote | Acceso")
ventana.geometry("440x360")
ventana.configure(bg=FONDO)
ventana.resizable(False, False)


def configurar_estilos():
    estilo = ttk.Style()
    estilo.theme_use("clam")

    estilo.configure(
        "Treeview",
        background=PANEL,
        foreground=BLANCO,
        fieldbackground=PANEL,
        rowheight=30,
        borderwidth=0,
        font=("Segoe UI", 9)
    )

    estilo.configure(
        "Treeview.Heading",
        background=MORADO,
        foreground="white",
        font=("Segoe UI", 9, "bold"),
        padding=8
    )

    estilo.map(
        "Treeview",
        background=[("selected", MORADO)],
        foreground=[("selected", "white")]
    )

    estilo.configure(
        "TCombobox",
        fieldbackground="white",
        background="white",
        foreground="#111827",
        padding=5
    )

    estilo.configure(
        "TSpinbox",
        padding=4
    )


def boton_padre(parent, texto, comando, color=MORADO, ancho=15):
    return tk.Button(
        parent,
        text=texto,
        command=comando,
        bg=color,
        fg="white",
        activebackground=MORADO_CLARO,
        activeforeground="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        cursor="hand2",
        width=ancho,
        padx=8,
        pady=8
    )


def mostrar_about(parent):
    ventana_about = tk.Toplevel(parent)
    ventana_about.title("Acerca de Compensándote")
    ventana_about.geometry("420x330")
    ventana_about.configure(bg=FONDO)
    ventana_about.resizable(False, False)
    ventana_about.transient(parent)

    tk.Label(
        ventana_about,
        text="COMPENSÁNDOTE",
        font=("Segoe UI", 20, "bold"),
        fg=MORADO_CLARO,
        bg=FONDO
    ).pack(pady=(25, 12))

    informacion = (
        "Proyecto académico\n"
        "Curso: Estructuras de Datos - 301305\n\n"
        "Estudiante: Andrea Redondo\n"
        "Grupo: 301305A_2204\n\n"
        "UNAD · ECBTI · Ingeniería de Sistemas\n"
        "Octubre de 2026"
    )

    tk.Label(
        ventana_about,
        text=informacion,
        font=("Segoe UI", 11),
        fg=BLANCO,
        bg=FONDO,
        justify="center"
    ).pack(pady=8)

    boton_padre(
        ventana_about,
        "Cerrar",
        ventana_about.destroy,
        color=MORADO
    ).pack(pady=12)


def abrir_menu():
    ventana.withdraw()

    app = tk.Toplevel(ventana)
    app.title("Compensándote | Gestión de afiliados")
    app.geometry("1450x850")
    app.minsize(1150, 700)
    app.configure(bg=FONDO)

    configurar_estilos()

    # ---------------- Variables del formulario ----------------

    tipo_id_var = tk.StringVar(value="CC")
    numero_id_var = tk.StringVar()
    nombre_var = tk.StringVar()
    ingresos_var = tk.StringVar()
    servicio_var = tk.StringVar(
        value="Subsidio de desempleo"
    )
    modalidad_var = tk.StringVar(value="Empleado")
    tarifa_var = tk.StringVar(value="$0")
    estructura_var = tk.StringVar(value="Pila")
    reporte_var = tk.StringVar(value="Sin consultar")

    dia_var = tk.StringVar()
    mes_var = tk.StringVar()
    anio_var = tk.StringVar()

    # Control para evitar ciclos al sincronizar fechas
    sincronizando_fecha = {"activo": False}


    encabezado = tk.Frame(app, bg=FONDO)
    encabezado.pack(fill="x", padx=25, pady=(18, 10))

    tk.Label(
        encabezado,
        text="COMPENSÁNDOTE",
        font=("Segoe UI", 24, "bold"),
        fg=MORADO_CLARO,
        bg=FONDO
    ).pack(side="left")

    tk.Label(
        encabezado,
        text="Sistema de gestión de afiliados",
        font=("Segoe UI", 12),
        fg=GRIS,
        bg=FONDO
    ).pack(side="left", padx=18, pady=(8, 0))

    boton_padre(
        encabezado,
        "Acerca de",
        lambda: mostrar_about(app),
        color="#374151",
        ancho=12
    ).pack(side="right")


    panel = tk.Frame(app, bg=PANEL)
    panel.pack(fill="x", padx=25, pady=8)

    tk.Label(
        panel,
        text="Registro de afiliados",
        font=("Segoe UI", 15, "bold"),
        fg=BLANCO,
        bg=PANEL
    ).grid(
        row=0, column=0, columnspan=6,
        sticky="w", padx=18, pady=(15, 12)
    )

    def crear_etiqueta(texto, fila, columna):
        tk.Label(
            panel,
            text=texto,
            font=("Segoe UI", 10, "bold"),
            fg=GRIS,
            bg=PANEL
        ).grid(
            row=fila,
            column=columna,
            sticky="w",
            padx=12,
            pady=5
        )

    def crear_entrada(variable, fila, columna, ancho=24):
        entrada = tk.Entry(
            panel,
            textvariable=variable,
            width=ancho,
            font=("Segoe UI", 10),
            relief="flat",
            bg="#FFFFFF",
            fg="#111827",
            insertbackground="#111827"
        )
        entrada.grid(
            row=fila,
            column=columna,
            sticky="ew",
            padx=12,
            pady=5,
            ipady=5
        )
        return entrada

    crear_etiqueta("Tipo de identificación", 1, 0)

    combo_tipo = ttk.Combobox(
        panel,
        textvariable=tipo_id_var,
        values=["CC", "CE", "NUIP", "PAS"],
        state="readonly",
        width=21
    )
    combo_tipo.grid(
        row=1, column=1, sticky="ew",
        padx=12, pady=5
    )

    crear_etiqueta("Número de identificación", 1, 2)
    entrada_id = crear_entrada(
        numero_id_var, 1, 3, ancho=25
    )

    crear_etiqueta("Nombre completo", 2, 0)
    entrada_nombre = crear_entrada(
        nombre_var, 2, 1, ancho=25
    )

    crear_etiqueta("Ingresos mensuales ($)", 2, 2)
    entrada_ingresos = crear_entrada(
        ingresos_var, 2, 3, ancho=25
    )

    crear_etiqueta("Servicio", 3, 0)

    combo_servicio = ttk.Combobox(
        panel,
        textvariable=servicio_var,
        values=[
            "Subsidio de desempleo",
            "Ingreso a parque",
            "Curso de formación",
            "Paquete de viaje",
            "Medicina preventiva"
        ],
        state="readonly",
        width=27
    )
    combo_servicio.grid(
        row=3, column=1, sticky="ew",
        padx=12, pady=5
    )

    crear_etiqueta("Modalidad laboral", 3, 2)

    marco_modalidad = tk.Frame(panel, bg=PANEL)
    marco_modalidad.grid(
        row=3, column=3, sticky="w",
        padx=12, pady=5
    )

    tk.Radiobutton(
        marco_modalidad,
        text="Empleado",
        variable=modalidad_var,
        value="Empleado",
        bg=PANEL,
        fg=BLANCO,
        selectcolor=FONDO,
        activebackground=PANEL,
        activeforeground=BLANCO,
        font=("Segoe UI", 10)
    ).pack(side="left", padx=(0, 12))

    tk.Radiobutton(
        marco_modalidad,
        text="Independiente",
        variable=modalidad_var,
        value="Independiente",
        bg=PANEL,
        fg=BLANCO,
        selectcolor=FONDO,
        activebackground=PANEL,
        activeforeground=BLANCO,
        font=("Segoe UI", 10)
    ).pack(side="left")

    crear_etiqueta("Fecha de registro", 4, 0)

    marco_fecha = tk.Frame(panel, bg=PANEL)
    marco_fecha.grid(
        row=4, column=1, sticky="w",
        padx=12, pady=5
    )

    hoy = date.today()
    dia_var.set(str(hoy.day))
    mes_var.set(str(hoy.month))
    anio_var.set(str(hoy.year))

    # Selector de fecha
    selector_fecha = DateEntry(
        marco_fecha,
        date_pattern="dd/mm/yyyy",
        width=12,
        background=MORADO,
        foreground="white",
        borderwidth=2,
        maxdate=hoy
    )
    selector_fecha.set_date(hoy)
    selector_fecha.pack(side="left", padx=(0, 10))

    # Spinboxes solicitados
    spin_dia = tk.Spinbox(
        marco_fecha,
        from_=1, to=31,
        textvariable=dia_var,
        width=3,
        state="readonly"
    )
    spin_dia.pack(side="left", padx=2)

    spin_mes = tk.Spinbox(
        marco_fecha,
        from_=1, to=12,
        textvariable=mes_var,
        width=3,
        state="readonly"
    )
    spin_mes.pack(side="left", padx=2)

    spin_anio = tk.Spinbox(
        marco_fecha,
        from_=1900, to=hoy.year,
        textvariable=anio_var,
        width=5,
        state="readonly"
    )
    spin_anio.pack(side="left", padx=2)

    # Tarifa calculada
    crear_etiqueta("Tarifa calculada", 4, 2)

    tk.Label(
        panel,
        textvariable=tarifa_var,
        font=("Segoe UI", 12, "bold"),
        fg=VERDE,
        bg=PANEL
    ).grid(
        row=4, column=3, sticky="w",
        padx=12, pady=5
    )

    crear_etiqueta("Estructura de datos", 5, 0)

    combo_estructura = ttk.Combobox(
        panel,
        textvariable=estructura_var,
        values=["Pila", "Cola", "Lista"],
        state="readonly",
        width=21
    )
    combo_estructura.grid(
        row=5, column=1, sticky="ew",
        padx=12, pady=5
    )

    crear_etiqueta("Reporte", 5, 2)

    tk.Label(
        panel,
        textvariable=reporte_var,
        font=("Segoe UI", 10, "bold"),
        fg=MORADO_CLARO,
        bg=PANEL,
        anchor="w"
    ).grid(
        row=5, column=3, sticky="ew",
        padx=12, pady=5
    )

    for columna in (1, 3):
        panel.grid_columnconfigure(columna, weight=1)


    def actualizar_spinboxes_desde_selector(event=None):
        if sincronizando_fecha["activo"]:
            return

        sincronizando_fecha["activo"] = True
        try:
            fecha = selector_fecha.get_date()
            dia_var.set(str(fecha.day))
            mes_var.set(str(fecha.month))
            anio_var.set(str(fecha.year))
        finally:
            sincronizando_fecha["activo"] = False

    def actualizar_selector_desde_spinboxes(*args):
        if sincronizando_fecha["activo"]:
            return

        try:
            dia = int(dia_var.get())
            mes = int(mes_var.get())
            anio = int(anio_var.get())

            fecha = date(anio, mes, dia)

            if fecha > hoy:
                return

            sincronizando_fecha["activo"] = True
            selector_fecha.set_date(fecha)

        except (ValueError, tk.TclError):
            return
        finally:
            sincronizando_fecha["activo"] = False

    selector_fecha.bind(
        "<<DateEntrySelected>>",
        actualizar_spinboxes_desde_selector
    )

    dia_var.trace_add("write", actualizar_selector_desde_spinboxes)
    mes_var.trace_add("write", actualizar_selector_desde_spinboxes)
    anio_var.trace_add("write", actualizar_selector_desde_spinboxes)

    def calcular_tarifa(mostrar_error=False):
        texto_ingresos = ingresos_var.get().strip()

        if not texto_ingresos:
            tarifa_var.set("$0")
            return 0

        try:
            ingresos = float(texto_ingresos)

            if ingresos < 0:
                raise ValueError

        except ValueError:
            tarifa_var.set("$0")

            if mostrar_error:
                messagebox.showerror(
                    "Ingresos inválidos",
                    "Ingresa un valor numérico válido y no negativo.",
                    parent=app
                )

            return None

        modalidad = modalidad_var.get()

        if 1_000_000 <= ingresos < 2_000_000:
            tarifa = 45000 if modalidad == "Empleado" else 10000
        elif 2_000_000 <= ingresos < 3_000_000:
            tarifa = 60000 if modalidad == "Empleado" else 20000
        elif 3_000_000 <= ingresos < 4_000_000:
            tarifa = 75000 if modalidad == "Empleado" else 30000
        elif 4_000_000 <= ingresos <= 5_000_000:
            tarifa = 90000 if modalidad == "Empleado" else 40000
        elif ingresos > 5_000_000:
            tarifa = 150000 if modalidad == "Empleado" else 80000
        else:
            tarifa = 0

        servicio = servicio_var.get()

        if servicio == "Ingreso a parque":
            tarifa += 2500
        elif servicio == "Curso de formación":
            tarifa += 7500
        elif servicio == "Paquete de viaje":
            tarifa += 10000
        elif servicio == "Medicina preventiva":
            tarifa += ingresos * 0.10

        tarifa = round(tarifa)
        tarifa_var.set(f"${tarifa:,.0f}")
        return tarifa

    def recalcular_tarifa(*args):
        calcular_tarifa()

    ingresos_var.trace_add("write", recalcular_tarifa)
    modalidad_var.trace_add("write", recalcular_tarifa)
    servicio_var.trace_add("write", recalcular_tarifa)

    def obtener_estructura():
        seleccion = estructura_var.get()

        if seleccion == "Pila":
            return pila
        elif seleccion == "Cola":
            return cola
        return lista_afiliados

    def obtener_nombre_estructura():
        return estructura_var.get()

    panel_tabla = tk.Frame(app, bg=PANEL)
    panel_tabla.pack(
        fill="both", expand=True,
        padx=25, pady=(8, 10)
    )

    tk.Label(
        panel_tabla,
        text="Afiliados registrados",
        font=("Segoe UI", 14, "bold"),
        fg=BLANCO,
        bg=PANEL
    ).pack(anchor="w", padx=15, pady=12)

    columnas = (
        "tipo_id",
        "numero_id",
        "nombre",
        "ingresos",
        "servicio",
        "modalidad",
        "tarifa",
        "fecha"
    )

    contenedor_tabla = tk.Frame(panel_tabla, bg=PANEL)
    contenedor_tabla.pack(
        fill="both", expand=True,
        padx=12, pady=(0, 12)
    )

    tabla = ttk.Treeview(
        contenedor_tabla,
        columns=columnas,
        show="headings",
        selectmode="browse"
    )

    encabezados = {
        "tipo_id": "Tipo ID",
        "numero_id": "Identificación",
        "nombre": "Nombre completo",
        "ingresos": "Ingresos",
        "servicio": "Servicio",
        "modalidad": "Modalidad",
        "tarifa": "Tarifa",
        "fecha": "Fecha"
    }

    anchos = {
        "tipo_id": 75,
        "numero_id": 120,
        "nombre": 180,
        "ingresos": 115,
        "servicio": 205,
        "modalidad": 115,
        "tarifa": 115,
        "fecha": 105
    }

    for columna in columnas:
        tabla.heading(columna, text=encabezados[columna])
        tabla.column(
            columna,
            width=anchos[columna],
            minwidth=70,
            anchor="center"
        )

    scrollbar_y = ttk.Scrollbar(
        contenedor_tabla,
        orient="vertical",
        command=tabla.yview
    )

    scrollbar_x = ttk.Scrollbar(
        contenedor_tabla,
        orient="horizontal",
        command=tabla.xview
    )

    tabla.configure(
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )

    tabla.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    contenedor_tabla.grid_rowconfigure(0, weight=1)
    contenedor_tabla.grid_columnconfigure(0, weight=1)

    def actualizar_tabla():
        for elemento in tabla.get_children():
            tabla.delete(elemento)

        for indice, afiliado in enumerate(obtener_estructura()):
            tabla.insert(
                "",
                "end",
                iid=str(indice),
                values=afiliado.obtener_datos()
            )

    def validar_formulario():
        tipo_id = tipo_id_var.get().strip()
        numero_id = numero_id_var.get().strip()
        nombre = nombre_var.get().strip()
        texto_ingresos = ingresos_var.get().strip()
        servicio = servicio_var.get().strip()
        modalidad = modalidad_var.get().strip()

        if not tipo_id:
            messagebox.showwarning(
                "Campo requerido",
                "Selecciona el tipo de identificación.",
                parent=app
            )
            return None

        if not numero_id or not numero_id.isdigit():
            messagebox.showwarning(
                "Identificación inválida",
                "El número de identificación debe contener solo dígitos.",
                parent=app
            )
            entrada_id.focus_set()
            return None

        if not nombre:
            messagebox.showwarning(
                "Campo requerido",
                "Ingresa el nombre completo.",
                parent=app
            )
            entrada_nombre.focus_set()
            return None

        if not all(
            caracter.isalpha() or caracter.isspace()
            for caracter in nombre
        ):
            messagebox.showwarning(
                "Nombre inválido",
                "El nombre debe contener solamente letras y espacios.",
                parent=app
            )
            entrada_nombre.focus_set()
            return None

        if not texto_ingresos:
            messagebox.showwarning(
                "Campo requerido",
                "Ingresa los ingresos mensuales.",
                parent=app
            )
            entrada_ingresos.focus_set()
            return None

        try:
            ingresos = float(texto_ingresos)

            if ingresos < 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Ingresos inválidos",
                "Los ingresos deben ser un número igual o mayor que cero.",
                parent=app
            )
            entrada_ingresos.focus_set()
            return None

        if not servicio or not modalidad:
            messagebox.showwarning(
                "Campo requerido",
                "Selecciona el servicio y la modalidad laboral.",
                parent=app
            )
            return None

        try:
            fecha = selector_fecha.get_date()

            if fecha > hoy:
                messagebox.showwarning(
                    "Fecha inválida",
                    "La fecha no puede ser posterior a hoy.",
                    parent=app
                )
                return None

        except (ValueError, tk.TclError):
            messagebox.showwarning(
                "Fecha inválida",
                "Selecciona una fecha válida.",
                parent=app
            )
            return None

        return {
            "tipo_id": tipo_id,
            "numero_id": numero_id,
            "nombre": nombre,
            "ingresos": ingresos,
            "servicio": servicio,
            "modalidad": modalidad,
            "fecha": fecha.strftime("%d/%m/%Y")
        }

    def registrar():
        datos = validar_formulario()

        if datos is None:
            return

        todos = list(pila) + list(cola) + list(lista_afiliados)

        duplicado = any(
            afiliado.tipo_id == datos["tipo_id"]
            and afiliado.numero_id == datos["numero_id"]
            for afiliado in todos
        )

        if duplicado:
            messagebox.showwarning(
                "Registro duplicado",
                "Ya existe un afiliado con ese tipo y número de identificación.",
                parent=app
            )
            return

        tarifa = calcular_tarifa(mostrar_error=True)

        if tarifa is None:
            return

        afiliado = EstructuraDatosAfiliado(
            tipo_id=datos["tipo_id"],
            numero_id=datos["numero_id"],
            nombre=datos["nombre"],
            ingresos=datos["ingresos"],
            servicio=datos["servicio"],
            modalidad=datos["modalidad"],
            tarifa=tarifa,
            fecha=datos["fecha"]
        )

        estructura = obtener_estructura()

        estructura.append(afiliado)

        actualizar_tabla()
        actualizar_reporte()

        messagebox.showinfo(
            "Registro exitoso",
            f"El afiliado se registró correctamente en {estructura_var.get()}.",
            parent=app
        )

        limpiar_campos(mostrar_mensaje=False)

    def limpiar_campos(mostrar_mensaje=True):
        tipo_id_var.set("CC")
        numero_id_var.set("")
        nombre_var.set("")
        ingresos_var.set("")
        servicio_var.set("Subsidio de desempleo")
        modalidad_var.set("Empleado")
        tarifa_var.set("$0")

        fecha_actual = date.today()
        selector_fecha.set_date(fecha_actual)

        dia_var.set(str(fecha_actual.day))
        mes_var.set(str(fecha_actual.month))
        anio_var.set(str(fecha_actual.year))

        estructura_var.set("Pila")
        reporte_var.set("Sin consultar")

        tabla.selection_remove(tabla.selection())
        actualizar_tabla()

        if mostrar_mensaje:
            messagebox.showinfo(
                "Formulario limpio",
                "Se limpiaron los campos. Los registros guardados no se eliminaron.",
                parent=app
            )

    def actualizar_reporte():
        registros = obtener_estructura()
        cantidad = len(registros)

        if cantidad == 0:
            reporte_var.set("Sin registros")
            return

        if estructura_var.get() == "Pila":
            total = sum(afiliado.tarifa for afiliado in registros)
            reporte_var.set(
                f"Total tarifas: ${total:,.0f}"
            )

        elif estructura_var.get() == "Cola":
            reporte_var.set(
                f"Afiliados registrados: {cantidad}"
            )

        else:
            promedio = (
                sum(afiliado.ingresos for afiliado in registros)
                / cantidad
            )
            reporte_var.set(
                f"Promedio ingresos: ${promedio:,.0f}"
            )

    def mostrar_reporte():
        registros = obtener_estructura()
        cantidad = len(registros)
        nombre_estructura = obtener_nombre_estructura()

        if cantidad == 0:
            reporte_var.set("Sin registros")
            messagebox.showinfo(
                "Reporte",
                f"No hay afiliados registrados en la {nombre_estructura.lower()}.",
                parent=app
            )
            return

        if nombre_estructura == "Pila":
            total = sum(afiliado.tarifa for afiliado in registros)

            detalle = (
                f"Estructura: Pila\n"
                f"Cantidad de afiliados: {cantidad}\n"
                f"Suma total de tarifas: ${total:,.0f}"
            )

        elif nombre_estructura == "Cola":
            detalle = (
                f"Estructura: Cola\n"
                f"Cantidad de afiliados: {cantidad}"
            )

        else:
            promedio = (
                sum(afiliado.ingresos for afiliado in registros)
                / cantidad
            )

            detalle = (
                f"Estructura: Lista\n"
                f"Cantidad de afiliados: {cantidad}\n"
                f"Promedio de ingresos: ${promedio:,.0f}"
            )

        reporte_var.set(detalle.replace("\n", " | "))

        messagebox.showinfo(
            f"Reporte de {nombre_estructura}",
            detalle,
            parent=app
        )

    def eliminar():
        estructura = obtener_estructura()
        nombre_estructura = obtener_nombre_estructura()

        if not estructura:
            messagebox.showinfo(
                "Sin registros",
                f"No hay afiliados en la {nombre_estructura.lower()} para eliminar.",
                parent=app
            )
            return

        if nombre_estructura == "Pila":
            afiliado = estructura[-1]

            confirmar = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Deseas retirar el último afiliado de la pila?\n\n"
                f"{afiliado.nombre} - {afiliado.numero_id}",
                parent=app
            )

            if confirmar:
                estructura.pop()

        elif nombre_estructura == "Cola":
            afiliado = estructura[0]

            confirmar = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Deseas retirar el primer afiliado de la cola?\n\n"
                f"{afiliado.nombre} - {afiliado.numero_id}",
                parent=app
            )

            if confirmar:
                # deque permite eliminar el primer elemento con popleft()
                estructura.popleft()

        else:
            identificacion = simpledialog.askstring(
                "Eliminar de la lista",
                "Escribe el número de identificación del afiliado:",
                parent=app
            )

            if identificacion is None:
                return

            identificacion = identificacion.strip()

            if not identificacion:
                messagebox.showwarning(
                    "Dato requerido",
                    "Debes ingresar una identificación.",
                    parent=app
                )
                return

            afiliado = next(
                (
                    elemento
                    for elemento in estructura
                    if elemento.numero_id == identificacion
                ),
                None
            )

            if afiliado is None:
                messagebox.showwarning(
                    "No encontrado",
                    "No se encontró un afiliado con esa identificación en la lista.",
                    parent=app
                )
                return

            confirmar = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Deseas eliminar este afiliado de la lista?\n\n"
                f"{afiliado.nombre} - {afiliado.numero_id}",
                parent=app
            )

            if confirmar:
                estructura.remove(afiliado)

        actualizar_tabla()
        actualizar_reporte()

    def cambiar_estructura(event=None):
        actualizar_tabla()
        actualizar_reporte()

    combo_estructura.bind(
        "<<ComboboxSelected>>",
        cambiar_estructura
    )

    panel_botones = tk.Frame(app, bg=FONDO)
    panel_botones.pack(fill="x", padx=25, pady=(0, 18))

    boton_padre(
        panel_botones,
        "Registrar",
        registrar,
        color=VERDE,
        ancho=14
    ).pack(side="left", padx=(0, 10))

    boton_padre(
        panel_botones,
        "Limpiar",
        limpiar_campos,
        color="#475569",
        ancho=14
    ).pack(side="left", padx=10)

    boton_padre(
        panel_botones,
        "Reporte",
        mostrar_reporte,
        color=MORADO,
        ancho=14
    ).pack(side="left", padx=10)

    boton_padre(
        panel_botones,
        "Eliminar",
        eliminar,
        color=ROJO,
        ancho=14
    ).pack(side="left", padx=10)

    def salir_aplicacion():
        confirmar = messagebox.askyesno(
            "Salir",
            "¿Deseas cerrar Compensándote?",
            parent=app
        )

        if confirmar:
            app.destroy()
            ventana.destroy()

    boton_padre(
        panel_botones,
        "Salir",
        salir_aplicacion,
        color="#374151",
        ancho=14
    ).pack(side="right")

    actualizar_tabla()
    actualizar_reporte()

    def cerrar_menu():
        app.destroy()
        ventana.deiconify()

    app.protocol("WM_DELETE_WINDOW", cerrar_menu)

tk.Label(
    ventana,
    text="COMPENSÁNDOTE",
    font=("Segoe UI", 23, "bold"),
    fg=MORADO_CLARO,
    bg=FONDO
).pack(pady=(32, 8))

tk.Label(
    ventana,
    text="Sistema de gestión de afiliados",
    font=("Segoe UI", 11),
    fg=GRIS,
    bg=FONDO
).pack(pady=(0, 22))

tk.Label(
    ventana,
    text="Contraseña de acceso",
    font=("Segoe UI", 11, "bold"),
    fg=BLANCO,
    bg=FONDO
).pack(pady=(0, 8))

contrasena_var = tk.StringVar()

entrada_contrasena = tk.Entry(
    ventana,
    textvariable=contrasena_var,
    show="*",
    font=("Segoe UI", 12),
    width=25,
    relief="flat",
    bg="white",
    fg="#111827",
    justify="center"
)
entrada_contrasena.pack(ipady=8, pady=(0, 18))


def iniciar_sesion(event=None):
    if contrasena_var.get() == "Caja":
        contrasena_var.set("")
        abrir_menu()
    else:
        messagebox.showerror(
            "Acceso denegado",
            "La contraseña ingresada es incorrecta.",
            parent=ventana
        )
        entrada_contrasena.focus_set()


boton_padre(
    ventana,
    "Ingresar",
    iniciar_sesion,
    color=MORADO,
    ancho=20
).pack(pady=4)

boton_padre(
    ventana,
    "Acerca de",
    lambda: mostrar_about(ventana),
    color="#374151",
    ancho=20
).pack(pady=8)

entrada_contrasena.bind("<Return>", iniciar_sesion)
entrada_contrasena.focus_set()

ventana.mainloop()
