# models_analisis.py
from datetime import date, timedelta, datetime
from libreria_cafe_edd_db import crear_sesion, Factura
from sqlalchemy import func, extract, and_

def analizar_ventas_por_hora(periodo="mes"):
    
    session = crear_sesion()
    try:
        hoy = date.today()
        if periodo == "mes":
            fecha_inicio = hoy - timedelta(days=30)
        elif periodo == "año":
            fecha_inicio = hoy - timedelta(days=365)
        else: 
            fecha_inicio = date(2000, 1, 1)
            
        if session.bind.dialect.name == 'sqlite':
            resultados = session.query(
                func.strftime('%H', Factura.fecha).label('hora'),
                func.count(Factura.id).label('total_ventas'),
                func.sum(Factura.monto_total).label('total_ingresos')
            ).filter(Factura.fecha >= fecha_inicio
            ).group_by('hora'
            ).order_by('hora').all()
        
        ventas_por_hora = []
        mejor_hora = None
        max_ventas = 0
        max_ingresos = 0
        total_ventas_general = 0
        total_ingresos_general = 0
        
        for r in resultados:
            hora = int(r.hora)
            ventas = r.total_ventas or 0
            ingresos = float(r.total_ingresos or 0)
            
            ventas_por_hora.append({
                "hora": hora,
                "hora_texto": f"{hora:02d}:00 - {hora+1:02d}:00",
                "total_ventas": ventas,
                "total_ingresos": ingresos
            })
            
            total_ventas_general += ventas
            total_ingresos_general += ingresos
            
            if ventas > max_ventas:
                max_ventas = ventas
                max_ingresos = ingresos
                mejor_hora = hora
        
        # Calcular promedio
        horas_con_datos = len(ventas_por_hora)
        promedio_ventas = total_ventas_general / horas_con_datos if horas_con_datos > 0 else 0
        
        # Formatear texto de la mejor hora
        mejor_hora_texto = f"{mejor_hora:02d}:00 - {mejor_hora+1:02d}:00" if mejor_hora is not None else "Sin datos"
        
        return {
            "mejor_hora": mejor_hora,
            "mejor_hora_texto": mejor_hora_texto,
            "total_ventas_mejor_hora": max_ventas,
            "total_ingresos_mejor_hora": max_ingresos,
            "ventas_por_hora": ventas_por_hora,
            "promedio_ventas_por_hora": promedio_ventas,
            "total_general": {
                "total_ventas": total_ventas_general,
                "total_ingresos": total_ingresos_general
            },
            "periodo": periodo,
            "fecha_inicio": fecha_inicio.strftime("%d/%m/%Y"),
            "fecha_fin": hoy.strftime("%d/%m/%Y")
        }
    finally:
        session.close()

def analizar_ventas_por_dia_semana(periodo="mes"):
    
    session = crear_sesion()
    try:
        hoy = date.today()
        if periodo == "mes":
            fecha_inicio = hoy - timedelta(days=30)
        elif periodo == "año":
            fecha_inicio = hoy - timedelta(days=365)
        else:
            fecha_inicio = date(2000, 1, 1)
        
        
        if session.bind.dialect.name == 'sqlite':
            resultados = session.query(
                func.strftime('%w', Factura.fecha).label('dia_semana'),
                func.count(Factura.id).label('total_ventas'),
                func.sum(Factura.monto_total).label('total_ingresos')
            ).filter(Factura.fecha >= fecha_inicio
            ).group_by('dia_semana'
            ).order_by('dia_semana').all()
        else:
            resultados = session.query(
                extract('dow', Factura.fecha).label('dia_semana'),
                func.count(Factura.id).label('total_ventas'),
                func.sum(Factura.monto_total).label('total_ingresos')
            ).filter(Factura.fecha >= fecha_inicio
            ).group_by('dia_semana'
            ).order_by('dia_semana').all()
        
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        ventas_por_dia = []
        mejor_dia = None
        max_ventas = 0
        
        for r in resultados:
            dia_idx = int(r.dia_semana)
            
            if session.bind.dialect.name == 'sqlite':
                dia_idx = (dia_idx + 6) % 7
            
            ventas = r.total_ventas or 0
            ingresos = float(r.total_ingresos or 0)
            
            ventas_por_dia.append({
                "dia": dia_idx,
                "dia_nombre": dias[dia_idx],
                "total_ventas": ventas,
                "total_ingresos": ingresos
            })
            
            if ventas > max_ventas:
                max_ventas = ventas
                mejor_dia = dia_idx
        
        return {
            "mejor_dia": mejor_dia,
            "mejor_dia_nombre": dias[mejor_dia] if mejor_dia is not None else "Sin datos",
            "total_ventas_mejor_dia": max_ventas,
            "ventas_por_dia": ventas_por_dia,
            "periodo": periodo
        }
    finally:
        session.close()

def analizar_tendencia_ventas(dias=30):
    session = crear_sesion()
    try:
        fecha_inicio = date.today() - timedelta(days=dias)
        
        resultados = session.query(
            Factura.fecha,
            func.count(Factura.id).label('total_ventas'),
            func.sum(Factura.monto_total).label('total_ingresos')
        ).filter(Factura.fecha >= fecha_inicio
        ).group_by(Factura.fecha
        ).order_by(Factura.fecha).all()
        
        tendencia = []
        for r in resultados:
            tendencia.append({
                "fecha": r.fecha.strftime("%d/%m/%Y"),
                "total_ventas": r.total_ventas or 0,
                "total_ingresos": float(r.total_ingresos or 0)
            })
        
        return tendencia
    finally:
        session.close()