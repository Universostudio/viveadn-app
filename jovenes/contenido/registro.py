"""Medición de legibilidad para el registro juvenil (español).
Fernández-Huerta (adaptación de Flesch al español) y longitud de frase.
Sin dependencias externas. Usado por build.py y por la guía de registro."""
import re

VOC = "aeiouáéíóúü"
FUERTES = "aeoáéó"


def silabas(palabra):
    p = re.sub(r"[^a-záéíóúüñ]", "", palabra.lower())
    n, prev = 0, None
    for ch in p:
        if ch in VOC:
            if prev is None:
                n += 1
            else:
                hiato = (prev in FUERTES and ch in FUERTES) or ch in "íú" or prev in "íú"
                if hiato:
                    n += 1
            prev = ch
        else:
            prev = None
    return max(n, 1) if p else 0


def palabras(texto):
    return re.findall(r"[A-Za-záéíóúüñÁÉÍÓÚÜÑ]+", re.sub(r"\*", "", texto))


def frases(texto):
    t = re.sub(r"\*", "", texto)
    return [f.strip() for f in re.split(r"(?<=[.!?])\s+|\n+", t) if len(palabras(f)) >= 2]


def fernandez_huerta(texto):
    pal, fr = palabras(texto), frases(texto)
    if not pal or not fr:
        return None
    return 206.84 - 0.60 * (100 * sum(silabas(p) for p in pal) / len(pal)) - 1.02 * (len(pal) / len(fr))


def largas(texto, limite=30):
    return [(len(palabras(f)), f) for f in frases(texto) if len(palabras(f)) > limite]
