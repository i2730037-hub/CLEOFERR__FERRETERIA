from conexion import ConexionDB

class DProducto:
    def __init__(self):
        self.__db = ConexionDB().conexionSupabase()
        self.__nombreTabla = 'productos'
        self.__tablaCategoria = 'categorias'

    def __ejecutarConsultas(self, consulta, tipoConsulta=None):
        try:
            if tipoConsulta == 'SELECT':
                return consulta.execute().data
            else:
                return consulta.execute()
        except Exception as e:
            raise e

    def mostrarProducto(self):
        consulta = (
        self.__db
        .table(self.__nombreTabla)
        .select('*')
        .order('estado', desc=True)  
    )
        return self.__ejecutarConsultas(consulta, 'SELECT')

    def obtenerCategorias(self):
        consulta = self.__db.table(self.__tablaCategoria).select('nombre')
        return consulta.execute().data

    def nuevoProducto(self, producto: dict):
        return self.__ejecutarConsultas(
            self.__db.table(self.__nombreTabla).insert(producto)
        )

    def actualizarProducto(self, producto: dict):
        return self.__ejecutarConsultas(
            self.__db
            .table(self.__nombreTabla)
            .update(producto)
            .eq('id_producto', producto['id_producto'])
        )

    def eliminarProducto(self, id_producto):
        return self.__ejecutarConsultas(
            self.__db
            .table(self.__nombreTabla)
            .update({'estado': 'inactivo'})
            .eq('id_producto', id_producto)
        )