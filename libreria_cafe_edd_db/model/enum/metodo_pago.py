from enum import Enum

class MetodoPago(Enum):
    EFECTIVO = "Efectivo"
    DIVISAS = "Divisas"
    PUNTO = "Punto"
    BIOPAGO = "Biopago"
    PAGO_MOVIL = "PagoMovil"
    TRANSFERENCIA = "Transferencia"