# app/services/detalle_venta_service.py
from app.repositories.detalle_venta_repo import DetalleVentaRepo
from app.repositories.venta_repo import VentaRepo
from app.repositories.producto_repo import ProductoRepo

detalle_repo  = DetalleVentaRepo()
venta_repo    = VentaRepo()
producto_repo = ProductoRepo()

class DetalleVentaService:

    def obtener_por_venta(self, venta_id):
        # valida que la venta exista
        venta = venta_repo.obtener_por_id(venta_id)
        if not venta:
            raise ValueError(f"Venta con id {venta_id} no encontrada")
        return detalle_repo.obtener_por_venta(venta_id)

    def crear(self, data):
        # valida que la venta exista
        venta = venta_repo.obtener_por_id(data["venta_id"])
        if not venta:
            raise ValueError(f"Venta con id {data['venta_id']} no encontrada")

        if venta.estado == "cancelada":
            raise ValueError("No se pueden agregar productos a una venta cancelada")

        # valida que el producto exista
        producto = producto_repo.obtener_por_id(data["producto_id"])
        if not producto:
            raise ValueError(f"Producto con id {data['producto_id']} no encontrado")

        if not producto.activo:
            raise ValueError(f"El producto {producto.nombre} no está disponible")

        if data["cantidad"] <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")

        # toma el precio actual del producto
        data["precio_unit"] = float(producto.precio)

        return detalle_repo.crear(data)