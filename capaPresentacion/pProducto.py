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
        if 'producto_activo' not in st.session_state:
            st.session_state.producto_activo = None
            
        if 'confirmar_eliminar' not in st.session_state:
            st.session_state.confirmar_eliminar = False
        if 'id_eliminar' not in st.session_state:
            st.session_state.id_eliminar = None



        self.__construirInterfaz()

    def __construirInterfaz(self):
        st.title('REGISTRAR PRODUCTOS')
        
        st.markdown("""
        <style>

        /* BOTONES */
        div.stButton > button {
            background-color: #1f3a5f;
            color: white;
            border-radius: 6px;
            font-weight: bold;
            border: none;
            transition: 0.3s ease;
        }

        div.stButton > button:hover {
            background-color: #2563eb;
            box-shadow: 0 0 10px rgba(37, 99, 235, 0.6);
            transform: scale(1.03);
        }

        /* CHECKBOX COLOR */
        div[data-testid="stDataEditor"] input[type="checkbox"] {
            accent-color: #2563eb;
            transform: scale(1.2);
            cursor: pointer;
        }

        /* CHECKBOX HOVER */
        div[data-testid="stDataEditor"] input[type="checkbox"]:hover {
            accent-color: #1d4ed8;
            box-shadow: 0 0 6px rgba(37, 99, 235, 0.8);
        }

        /* CABECERA TABLA */
        div[data-testid="stDataEditor"] thead tr th {
            background-color: #1f3a5f !important;
            color: white !important;
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
        if st.session_state.confirmar_eliminar:
            self.eliminarProducto()


    def mostrarProducto(self):
        listaProducto = self.__lProducto.mostrarProducto()
        tabla = []

        for p in listaProducto:
            tabla.append( {
                "Seleccionar": False,
                "id_producto": p["id_producto"],
                "nombre": p["nombre"],
                "descripcion": p["descripcion"],
                "precio": p["precio"],
                "stock": p["stock"],
                "nombre_categoria": p["nombre_categoria"],
                "estado": p["estado"]
            })

        col1, col2 = st.columns([10, 2])

        with col1:
            edited = st.data_editor (
                tabla,
                use_container_width=True,
                hide_index=True,
                key="tabla_productos",
                column_config={
                    "Seleccionar": st.column_config.CheckboxColumn(default=False)
                }
        )


        seleccionados = [f for f in edited if f["Seleccionar"]]

        if len(seleccionados) == 1:
            producto_seleccionado = seleccionados[0]
            id_seleccionado = producto_seleccionado["id_producto"]
        else:
            producto_seleccionado = None
            id_seleccionado = None


        with col2:
             if producto_seleccionado is not None:
                st.info(f"Seleccionado:\n{producto_seleccionado['nombre']}")
                if st.button("Editar"):
                    st.session_state.producto_seleccionado = producto_seleccionado
                    st.session_state.id_producto_sesion = producto_seleccionado["id_producto"]
                    st.session_state.nombre_sesion = producto_seleccionado["nombre"]
                    st.session_state.descripcion_sesion = producto_seleccionado["descripcion"]
                    st.session_state.precio_sesion = float(producto_seleccionado["precio"])
                    st.session_state.stock_sesion = int(producto_seleccionado["stock"])
                    st.rerun()

                if st.button("Eliminar"):
                    st.session_state.confirmar_eliminar = True
                    st.session_state.id_eliminar = producto_seleccionado["id_producto"]
                    st.rerun()
        

    def nuevoProducto(self, producto):
        self.__lProducto.nuevoProducto(producto)
        st.success('Producto guardado correctamente')
        self.limpiar()

    def actualizarProducto(self, producto):
        self.__lProducto.actualizarProducto(producto)
        st.success('Producto actualizado correctamente')
        self.limpiar()

    def eliminarProducto(self):
        if not st.session_state.confirmar_eliminar:
            return

        st.warning("¿Está seguro de eliminar este producto?")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sí, eliminar", key="confirmar_eliminar_btn"):
                self.__lProducto.eliminarProducto(st.session_state.id_eliminar)
                st.success("Producto eliminado correctamente")
                self.limpiar()

        with col2:
            if st.button("Cancelar", key="cancelar_eliminar_btn"):
                st.session_state.confirmar_eliminar = False
                st.session_state.id_eliminar = None
                st.rerun()
        

    def limpiar(self):
        st.session_state.producto_seleccionado = None
        st.session_state.id_producto_sesion = ''
        st.session_state.nombre_sesion = ''
        st.session_state.descripcion_sesion = ''
        st.session_state.precio_sesion = 0.0
        st.session_state.stock_sesion = 0
        st.session_state.confirmar_eliminar = False
        st.session_state.id_eliminar = None
        st.rerun()
