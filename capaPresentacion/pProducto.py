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


        if st.session_state.producto_seleccionado:
            st.text_input(
                'ID Producto',
                st.session_state.id_producto_sesion,
                disabled=True
            )

        txtNombre = st.text_input('Nombre', st.session_state.nombre_sesion)
        txtDescripcion = st.text_input('Descripción', st.session_state.descripcion_sesion)
        txtPrecio = st.number_input(
            'Precio',
            min_value=0.0,
            value=float(st.session_state.precio_sesion)
        )
        txtStock = st.number_input(
            'Stock',
            min_value=0,
            step=1,
            value=int(st.session_state.stock_sesion)
        )

        categorias = self.__lProducto.obtenerCategorias()
        nombre_categoria = st.selectbox(
            'Categoría',
            options=[c['nombre'] for c in categorias] if categorias else []
        )

        # ===== BOTONES =====
        if st.session_state.producto_seleccionado:
            if st.button('Actualizar'):
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
                except Exception as e:
                    st.error(str(e))
        else:
            if st.button('Guardar'):
                try:
                    producto = {
                        'nombre': txtNombre,
                        'descripcion': txtDescripcion,
                        'precio': txtPrecio,
                        'stock': txtStock,
                        'nombre_categoria': nombre_categoria
                    }
                    self.nuevoProducto(producto)
                except Exception as e:
                    st.error(str(e))

        st.divider()

        self.mostrarProducto()

    def mostrarProducto(self):
        listaProducto = self.__lProducto.mostrarProducto()
        tabla = []

        for p in listaProducto:
            fila = {
                "Seleccionar": False,
                "id_producto": p["id_producto"],
                "nombre": p["nombre"],
                "descripcion": p["descripcion"],
                "precio": p["precio"],
                "stock": p["stock"],
                "nombre_categoria": p["nombre_categoria"]
            }
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
                if fila["Seleccionar"]:
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

    def nuevoProducto(self, producto):
        self.__lProducto.nuevoProducto(producto)
        st.success('Producto guardado correctamente')
        self.limpiar()

    def actualizarProducto(self, producto):
        self.__lProducto.actualizarProducto(producto)
        st.success('Producto actualizado correctamente')
        self.limpiar()

    def eliminarProducto(self, id_producto):
        self.__lProducto.eliminarProducto(id_producto)
        st.success('Producto eliminado correctamente')
        self.limpiar()

    def limpiar(self):
        st.session_state.producto_seleccionado = None
        st.session_state.id_producto_sesion = ''
        st.session_state.nombre_sesion = ''
        st.session_state.descripcion_sesion = ''
        st.session_state.precio_sesion = 0.0
        st.session_state.stock_sesion = 0
        st.rerun()
