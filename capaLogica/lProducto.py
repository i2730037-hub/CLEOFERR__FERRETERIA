from capaDatos.dProducto import DProducto

class LProducto:
    def __init__(self):
        self.__dProducto = DProducto()

    def mostrarProducto(self):
        return self.__dProducto.mostrarProducto()

    def obtenerCategorias(self):
        return self.__dProducto.obtenerCategorias()

    def __validarProducto(self, producto: dict):
        if not producto.get('nombre'):
            raise ValueError("El nombre es obligatorio")
        if not producto.get('descripcion'):
            raise ValueError("La descripción es obligatoria")
        if producto.get('precio') is None or producto['precio'] <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if producto.get('stock') is None or producto['stock'] < 0:
            raise ValueError("El stock no puede ser negativo")
        if not producto.get('nombre_categoria'):
            raise ValueError("Debe seleccionar una categoría")

    def nuevoProducto(self, producto: dict):
        self.__validarProducto(producto)
        producto['estado'] = 'Activo'
        return self.__dProducto.nuevoProducto(producto)

    def actualizarProducto(self, producto: dict):
        self.__validarProducto(producto)
        return self.__dProducto.actualizarProducto(producto)

    def eliminarProducto(self, id_producto):
        return self.__dProducto.eliminarProducto(id_producto)