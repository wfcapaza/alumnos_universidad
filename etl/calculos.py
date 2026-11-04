def calcular_estado_academico(promedio):

    if promedio >= 16.0:
        return "Destacado"

    elif promedio >= 10.5:
        return "Regular"

    else:
        return "Riesgo Académico"


def calcular_condicion_beca(promedio, creditos):

    if promedio >= 17.0 and creditos >= 18:
        return "Beca Completa"

    elif promedio >= 15.5:
        return "Media Beca"

    else:
        return "Sin Beneficio"