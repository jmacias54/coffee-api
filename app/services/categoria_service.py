from app.repositories.categoria_repo import CategoriaRepo

repo = CategoriaRepo()

class CategoriaService:

    def obtener_todos(self):
        return repo.obtener_todos()

    def obtener_por_id(self, id):
        categoria = repo.obtener_por_id(id)
        if not categoria:
            raise ValueError(f"Categoría con id {id} no encontrada")
        return categoria

    def crear(self, data):
        nombre = data.get("nombre")
        if not nombre:
            raise ValueError("El nombre es requerido")

        if repo.obtener_por_nombre(nombre):
            raise ValueError(f"Ya existe una categoría con el nombre {nombre}")

        return repo.crear(data)

    def actualizar(self, id, data):
        categoria = self.obtener_por_id(id)

        if "nombre" in data:
            existente = repo.obtener_por_nombre(data["nombre"])
            if existente and existente.id != id:
                raise ValueError("Ya existe una categoría con ese nombre")

        return repo.actualizar(id, data)

    def eliminar(self, id):
        self.obtener_por_id(id)
        return repo.eliminar(id)