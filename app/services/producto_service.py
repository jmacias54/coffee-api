from app.models.producto import Producto
from app.repositories.producto_repo import ProductoRepo
from app.repositories.categoria_repo import CategoriaRepo


class ProductoService:

    def __init__(self):
        self.repo = ProductoRepo()
        self.categoria_repo = CategoriaRepo()

    def obtener_todos(self):
        return self.repo.obtener_todos()

    def obtener_por_id(self, id):
        producto = self.repo.obtener_por_id(id)
        if not producto:
            raise ValueError(f"Producto con id {id} no encontrado")
        return producto

    def crear(self, data):
        nombre = data.get("nombre")
        precio = data.get("precio")
        categoria_id = data.get("categoria_id")

        if not nombre:
            raise ValueError("El nombre es requerido")

        if precio is None or precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        if not categoria_id:
            raise ValueError("La categoría es requerida")

        categoria = self.categoria_repo.obtener_por_id(categoria_id)
        if not categoria:
            raise ValueError(f"Categoría con id {categoria_id} no encontrada")

        if self.repo.obtener_por_nombre_y_categoria(nombre, categoria_id):
            raise ValueError("Ya existe un producto con ese nombre en la categoría")

        producto = Producto(
            nombre=nombre,
            descripcion=data.get("descripcion"),
            precio=precio,
            stock=data.get("stock", 0),
            activo=data.get("activo", True),
            imagen_url=data.get("imagen_url"),
            categoria_id=categoria_id
        )

        return self.repo.crear(producto)

    def actualizar(self, id, data):
        producto = self.obtener_por_id(id)

        if "precio" in data and data["precio"] <= 0:
            raise ValueError("El precio debe ser mayor a 0")

        if "categoria_id" in data:
            categoria = self.categoria_repo.obtener_por_id(data["categoria_id"])
            if not categoria:
                raise ValueError("Categoría no encontrada")

        if "nombre" in data:
            existente = self.repo.obtener_por_nombre_y_categoria(
                data["nombre"],
                data.get("categoria_id", producto.categoria_id)
            )
            if existente and existente.id != id:
                raise ValueError("Ya existe un producto con ese nombre en la categoría")

        # aplicar cambios
        for campo in [
            "nombre", "descripcion", "precio",
            "stock", "activo", "imagen_url", "categoria_id"
        ]:
            if campo in data:
                setattr(producto, campo, data[campo])

        self.repo.actualizar()
        return producto

    def eliminar(self, id):
        producto = self.obtener_por_id(id)
        self.repo.eliminar(producto)
        return producto