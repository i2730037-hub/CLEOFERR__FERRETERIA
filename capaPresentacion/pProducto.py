from capaLogica.lProducto import LProducto
import streamlit as st


class PProducto:
    def __init__(self):
        self.__lProducto = LProducto()

        if 'producto_seleccionado' not in st.session_state:
            st.session_state.producto_seleccionado = None
        if 'id_producto_sesion' not in st.session_state:
            st.session_state.id_producto_sesion = ''
        if 'nombre_sesion' not in st.session_state:
            st.session_state.nombre_sesion = ''
        if 'descripcion_sesion' not in st.session_state:
            st.session_state.descripcion_sesion = ''
        if 'precio_sesion' not in st.session_state:
            st.session_state.precio_sesion = 0.0
        if 'stock_sesion' not in st.session_state:
            st.session_state.stock_sesion = 0

        self.__construirInterfaz()

    def __construirInterfaz(self):
        st.title('REGISTRAR PRODUCTOS')

       
        st.markdown("""
        <style>
        /* Fondo general */
        .stApp {
            background-color: #F1F3F5;
        }

        /* Inputs */
        input, textarea, select {
            background-color: #FFFFFF !important;
            border: 1px solid #B0BEC5 !important;
            border-radius: 6px !important;
        }

        /* Botón principal (Guardar / Actualizar) */
        div.stButton > button {
            background-color: #1F3A5F !important;
            color: white !important;
            font-weight: 700;
            border-radius: 8px;
            border: none;
        }

        div.stButton > button:hover {
            background-color: #162B45 !important;
        }

        /* Botón Editar */
        div.stButton button:has(span:contains("Editar")) {
            background-color: #274C77 !important;
        }

        div.stButton button:has(span:contains("Editar")):hover {
            background-color: #1C3A5A !important;
        }

        /* Botón Eliminar */
        div.stButton button:has(span:contains("Eliminar")) {
            background-color: #7A1F1F !important;
        }

        div.stButton button:has(span:contains("Eliminar")):hover {
            background-color: #5E1717 !important;
        }

        /* Tabla */
        div[data-testid="stDataFrame"] {
            border: 1px solid #B0BEC5;
            border-radius: 8px;
        }
        </style>
        """, unsafe_allow_html=True)

        
        if st.session_state.producto_seleccionado:
            st.text_input(
                'ID Producto',
                st.session_state.id_producto_sesion,
                disabled=True
            )

        txtNombre = st.text_input('Nombre', st.session_state.nombre_sesion)
        txtDescripcion = st.text_input('Descripción', st.session_state.descripcion_sesion)
        txtPrecio = st.number_input('Precio', min_value=0.0, value=float(st.session_state.precio_sesion))
        txtStock = st.number_input('Stock', min_value=0, step=1, value=int(st.session_state.stock_sesion))

        categorias = self.__lProducto.obtenerCategorias()
        nombre_categoria = st.selectbox(
            'Categoría',
            options=[c['nombre'] for c in categorias]
        )

        if st.session_state.producto_seleccionado:
            if st.button('Actualizar'):
                if not txtNombre or not txtDescripcion:
                    st.error("Debe completar todos los campos obligatorios")
            return

            try:
                producto = {
                    'id_producto': st.session_state.id_producto_sesion,
                    'nombre': txtNombre,
                    'descripcion': txtDescripcion,
                    'precio': txtPrecio,
                    'stock': txtStock,
                    'nombre_categoria': nombre_categoria
                }                
                self.actualizarProducto(producto)
            except ValueError as e:
                st.error(str(e))
        else:
            if st.button('Guardar'):
                if not txtNombre or not txtDescripcion:
                    st.error("Debe completar todos los campos obligatorios")
            return

            try:
                producto = {
                    'nombre': txtNombre,
                    'descripcion': txtDescripcion,
                    'precio': txtPrecio,
                    'stock': txtStock,
                    'nombre_categoria': nombre_categoria
                }
                self.nuevoProducto(producto)
            except ValueError as e:
                st.error(str(e))

        self.mostrarProducto()

    
    def mostrarProducto(self):
        listaProducto = self.__lProducto.mostrarProducto()
        tabla = []

        for p in listaProducto:
            if "Seleccionar" not in p:
                p["Seleccionar"] = False

            fila = {}
            fila["Seleccionar"] = p["Seleccionar"]
            fila["id_producto"] = p["id_producto"]

            for k, v in p.items():
                if k not in ["Seleccionar", "id_producto"]:
                    fila[k] = v

            tabla.append(fila)

        col1, col2 = st.columns([10, 2])

        with col1:
            edited = st.data_editor(
                tabla,
                use_container_width=True,
                hide_index=True,
                key="tabla_productos"
            )

        with col2:
            seleccionado = None
            for fila in edited:
                if fila.get("Seleccionar"):
                    seleccionado = fila
                    break

            if seleccionado:
                if st.button("Editar"):
                    st.session_state.producto_seleccionado = seleccionado
                    st.session_state.id_producto_sesion = seleccionado["id_producto"]
                    st.session_state.nombre_sesion = seleccionado["nombre"]
                    st.session_state.descripcion_sesion = seleccionado["descripcion"]
                    st.session_state.precio_sesion = float(seleccionado["precio"])
                    st.session_state.stock_sesion = int(seleccionado["stock"])
                    st.rerun()

                if st.button("Eliminar"):
                    self.eliminarProducto(seleccionado["id_producto"])
                    st.rerun()

   
    def nuevoProducto(self, producto):
        self.__lProducto.nuevoProducto(producto)
        st.toast('Producto guardado correctamente')
        self.limpiar()

    def actualizarProducto(self, producto):
        self.__lProducto.actualizarProducto(producto)
        st.toast('Producto actualizado correctamente')
        self.limpiar()

    def eliminarProducto(self, id_producto):
        self.__lProducto.eliminarProducto(id_producto)
        st.toast('Producto eliminado correctamente')
        self.limpiar()

    def limpiar(self):
        st.session_state.producto_seleccionado = None
        st.session_state.id_producto_sesion = ''
        st.session_state.nombre_sesion = ''
        st.session_state.descripcion_sesion = ''
        st.session_state.precio_sesion = 0.0
        st.session_state.stock_sesion = 0
        st.rerun()
