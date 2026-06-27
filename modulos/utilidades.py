
# Se creo archivo para tener funciones de utilidad que se puedan usar en varios modulos

def raiz_cuadrada(x: float) -> float | None:
    if x < 0:
        return None
    if x == 0:
        return 0.0
    r = x / 2.0
    for _ in range(30):
        nr = (r + x / r) / 2.0
        if abs(nr - r) < 1e-14:
            return nr
        r = nr
    return r
