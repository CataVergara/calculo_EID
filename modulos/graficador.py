# -*- coding: utf-8 -*-

from modulos.utilidades import raiz_cuadrada


def generar_puntos_conica(params: dict, num_puntos: int = 400, rango: float = 15) -> list[dict]:
    tipo = params.get("tipo", "")
    h = params.get("h", 0.0)
    k = params.get("k", 0.0)
    puntos: list[dict] = []

    if tipo == "Circunferencia":
        r = params.get("radio", 1.0)
        if r <= 0:
            return []
        paso = (2.0 * r) / num_puntos
        for i in range(num_puntos + 1):
            xv = h - r + i * paso
            if xv < h - r - 1e-12 or xv > h + r + 1e-12:
                continue
            rad = r**2 - (xv - h)**2
            if rad < 0:
                continue
            raiz = raiz_cuadrada(rad)
            if raiz is None:
                continue
            puntos.append({"x": round(xv, 6), "y": round(k + raiz, 6)})
        for i in range(num_puntos, -1, -1):
            xv = h - r + i * paso
            if xv < h - r - 1e-12 or xv > h + r + 1e-12:
                continue
            rad = r**2 - (xv - h)**2
            if rad < 0:
                continue
            raiz = raiz_cuadrada(rad)
            if raiz is None:
                continue
            puntos.append({"x": round(xv, 6), "y": round(k - raiz, 6)})

    elif tipo == "Elipse":
        if params.get("imaginaria", False):
            return []
        a = params.get("a", 1.0)
        b = params.get("b", 1.0)
        if a <= 0 or b <= 0:
            return []
        paso = (2.0 * a) / num_puntos
        for i in range(num_puntos + 1):
            xv = h - a + i * paso
            diff = (xv - h) / a
            rad = 1.0 - diff * diff
            if rad < 0:
                continue
            raiz = raiz_cuadrada(rad)
            if raiz is None:
                continue
            yv = k + b * raiz
            puntos.append({"x": round(xv, 6), "y": round(yv, 6)})
        for i in range(num_puntos, -1, -1):
            xv = h - a + i * paso
            diff = (xv - h) / a
            rad = 1.0 - diff * diff
            if rad < 0:
                continue
            raiz = raiz_cuadrada(rad)
            if raiz is None:
                continue
            yv = k - b * raiz
            puntos.append({"x": round(xv, 6), "y": round(yv, 6)})

    elif tipo == "Hiperbola":
        a = params.get("a", 1.0)
        b = params.get("b", 1.0)
        orientacion = params.get("orientacion", "horizontal")
        if a <= 0 or b <= 0:
            return []
        if orientacion == "horizontal":
            for signo in [1, -1]:
                pts_rama: list[dict] = []
                for i in range(num_puntos // 2 + 1):
                    t = (i / (num_puntos // 2)) * rango + 0.01
                    xv = h + signo * a * (1.0 + t)
                    diff = ((xv - h) / a)
                    rad = diff * diff - 1.0
                    if rad < 0:
                        continue
                    raiz = raiz_cuadrada(rad)
                    if raiz is None:
                        continue
                    pts_rama.append({"x": round(xv, 6), "y": round(k + b * raiz, 6)})
                puntos.extend(pts_rama)
                pts_inf: list[dict] = []
                for i in range(num_puntos // 2 + 1):
                    t = (i / (num_puntos // 2)) * rango + 0.01
                    xv = h + signo * a * (1.0 + t)
                    diff = ((xv - h) / a)
                    rad = diff * diff - 1.0
                    if rad < 0:
                        continue
                    raiz = raiz_cuadrada(rad)
                    if raiz is None:
                        continue
                    pts_inf.append({"x": round(xv, 6), "y": round(k - b * raiz, 6)})
                puntos.extend(pts_inf)
        else:
            for signo in [1, -1]:
                pts_rama = []
                for i in range(num_puntos // 2 + 1):
                    t = (i / (num_puntos // 2)) * rango + 0.01
                    yv = k + signo * a * (1.0 + t)
                    diff = ((yv - k) / a)
                    rad = diff * diff - 1.0
                    if rad < 0:
                        continue
                    raiz = raiz_cuadrada(rad)
                    if raiz is None:
                        continue
                    pts_rama.append({"x": round(h + b * raiz, 6), "y": round(yv, 6)})
                puntos.extend(pts_rama)
                pts_inf = []
                for i in range(num_puntos // 2 + 1):
                    t = (i / (num_puntos // 2)) * rango + 0.01
                    yv = k + signo * a * (1.0 + t)
                    diff = ((yv - k) / a)
                    rad = diff * diff - 1.0
                    if rad < 0:
                        continue
                    raiz = raiz_cuadrada(rad)
                    if raiz is None:
                        continue
                    pts_inf.append({"x": round(h - b * raiz, 6), "y": round(yv, 6)})
                puntos.extend(pts_inf)

    elif tipo == "Parabola":
        pv = params.get("p", 1.0)
        eje = params.get("eje", "vertical")
        if abs(pv) < 1e-12:
            h_d = params.get("h", 0.0)
            k_d = params.get("k", 0.0)
            if eje == "vertical":
                for i in range(num_puntos + 1):
                    yv = k_d - rango / 2.0 + (i / num_puntos) * rango
                    puntos.append({"x": round(h_d, 6), "y": round(yv, 6)})
            else:
                for i in range(num_puntos + 1):
                    xv = h_d - rango / 2.0 + (i / num_puntos) * rango
                    puntos.append({"x": round(xv, 6), "y": round(k_d, 6)})
            return puntos
        if eje == "vertical":
            for i in range(num_puntos + 1):
                xv = h - rango / 2.0 + (i / num_puntos) * rango
                yv = k + ((xv - h)**2) / (4.0 * pv)
                if abs(yv) > 100:
                    continue
                puntos.append({"x": round(xv, 6), "y": round(yv, 6)})
        else:
            for i in range(num_puntos + 1):
                yv = k - rango / 2.0 + (i / num_puntos) * rango
                xv = h + ((yv - k)**2) / (4.0 * pv)
                if abs(xv) > 100:
                    continue
                puntos.append({"x": round(xv, 6), "y": round(yv, 6)})

    return puntos


def generar_puntos_asintotas(params: dict, num_puntos: int = 50, rango: float = 15) -> list[dict]:
    puntos: list[dict] = []
    asintotas = params.get("asintotas", [])
    h = params.get("h", 0.0)
    for m, intercepto in asintotas:
        for i in range(num_puntos + 1):
            xv = h - rango / 2.0 + (i / num_puntos) * rango
            yv = m * xv + intercepto
            if abs(yv) > 100:
                continue
            puntos.append({"x": round(xv, 6), "y": round(yv, 6), "tipo": "asintota"})
    return puntos


def generar_puntos_elementos(params: dict) -> list[dict]:
    puntos: list[dict] = []

    centro = params.get("centro")
    if centro:
        puntos.append({
            "x": round(centro[0], 4),
            "y": round(centro[1], 4),
            "tipo": "centro",
            "label": "Centro"
        })

    focos = params.get("focos", [])
    for f in focos:
        puntos.append({
            "x": round(f[0], 4),
            "y": round(f[1], 4),
            "tipo": "foco",
            "label": "Foco"
        })

    vertices = params.get("vertices", [])
    for v in vertices:
        puntos.append({
            "x": round(v[0], 4),
            "y": round(v[1], 4),
            "tipo": "vertice",
            "label": "Vertice"
        })

    return puntos


def generar_puntos_ejes(rango: float = 15) -> list[dict]:
    return [
        {"x": -rango, "y": 0, "tipo": "eje", "label": "eje_x"},
        {"x": rango, "y": 0, "tipo": "eje", "label": "eje_x"},
        {"x": 0, "y": -rango, "tipo": "eje", "label": "eje_y"},
        {"x": 0, "y": rango, "tipo": "eje", "label": "eje_y"},
    ]


def crear_datos_grafico(tipo: str, params: dict) -> dict:
    curva = generar_puntos_conica(params)
    asint_pts = generar_puntos_asintotas(params) if tipo == "Hiperbola" else []
    elementos = generar_puntos_elementos(params)
    ejes = generar_puntos_ejes()
    return {
        "curva": curva,
        "asintotas": asint_pts,
        "elementos": elementos,
        "ejes": ejes
    }
