#!/usr/bin/env python3
"""Genera tokens de color de la interfaz Jóvenes para las 4 temporadas (trimestres),
con verificación de contraste WCAG 2.x en modo claro y oscuro.

Entradas (fuentes del proyecto):
  - Base juvenil de los mockups app (VMAD_Bloque3_Familia_Jovenes): --jbg #F0F8F2, --jdiv #C8E6CA, --jtxt #1A2A1A, --jgreen #4CAF50
  - Paleta mensual "El Bosque" (Guía de Producción 2027-2029, sección 6.1)
Salidas: tokens-estaciones.json, jovenes-estaciones.css, contraste.md
"""
import json, pathlib

AQUI = pathlib.Path(__file__).parent

MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
# Paleta mensual. Año parametrizable: sustituir por la paleta del año (2026, 2028, 2029).
PALETA_MES = {
    2027: ["#1A3B2A", "#2A3A4A", "#4A6B4A", "#7A3A2A", "#C4622D", "#A07030",
           "#1A4A3A", "#5A3A2A", "#C9963A", "#5C1A2A", "#6A2A5A", "#0F3A1A"],
}
TEMPORADAS = [  # nombres de trabajo, pendientes de validar con diseño
    {"id": "brote", "nombre": "Brote", "meses": ["ene", "feb", "mar"], "tema": "Fundamentos e identidad"},
    {"id": "savia", "nombre": "Savia", "meses": ["abr", "may", "jun"], "tema": "Vida sobrenatural y autoridad"},
    {"id": "cosecha", "nombre": "Cosecha", "meses": ["jul", "ago", "sep"], "tema": "Don, llamado y testimonio"},
    {"id": "aguardo", "nombre": "Aguardo", "meses": ["oct", "nov", "dic"], "tema": "Perseverancia, mayordomía y esperanza"},
]
# Dos marcos de interfaz, porque el proyecto tiene dos paletas de marca distintas:
#  vmad     = mockups de la app VMAD (Bloque 3 Jóvenes): --jbg #F0F8F2, --jdiv #C8E6CA, --jtxt #1A2A1A
#  viveadn  = CRM ViveADN "ADN Vital": arena #F4F0E6, gris #2C3E50, verde #00523C, oro #F5A623
MARCOS = {
    "vmad": {
        "claro": {"bg": "#F0F8F2", "surface": "#FFFFFF", "border": "#C8E6CA", "text": "#1A2A1A", "text2": "#4A6A4C"},
        "oscuro": {"bg": "#0E1710", "surface": "#15231A", "border": "#274030", "text": "#E8F2EA", "text2": "#A9C4AE"},
        "oro": "#D4AA3A",
    },
    "viveadn": {
        "claro": {"bg": "#F4F0E6", "surface": "#FFFFFF", "border": "#DDD6C2", "text": "#1A2A1F", "text2": "#3D5166"},
        "oscuro": {"bg": "#0B1A14", "surface": "#12251C", "border": "#24392E", "text": "#EEF3EE", "text2": "#A9BDB1"},
        "oro": "#F5A623",
    },
}


def h2rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def rgb2h(r): return "#%02X%02X%02X" % tuple(max(0, min(255, round(c))) for c in r)
def mezcla(a, b, t): return rgb2h(tuple(x + (y - x) * t for x, y in zip(h2rgb(a), h2rgb(b))))


def lum(h):
    def f(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = h2rgb(h)
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def ajusta(color, fondo, minimo, hacia):
    """Mueve `color` hacia `hacia` (#000 o #FFF) hasta alcanzar `minimo` de contraste contra `fondo`."""
    for i in range(0, 101):
        c = mezcla(color, hacia, i / 100)
        if ratio(c, fondo) >= minimo:
            return c
    return hacia


def oro_ui(oro, superficie, claro):
    """Oro de interfaz con >= 3:1 sobre la superficie (elementos gráficos)."""
    return ajusta(oro, superficie, 3.0, "#000000" if claro else "#FFFFFF")


def tokens_mes(hexmes, modo, marco):
    n = MARCOS[marco][modo]
    claro = modo == "claro"
    # color para texto de acento (etiquetas, enlaces) sobre superficie y fondo: >= 4.5
    peor_fondo = min((n["bg"], n["surface"]), key=lambda f: ratio(hexmes, f))
    # claro: AA (4.5). oscuro: 7.0, porque los acentos de mes son muy oscuros y al mínimo se ven apagados sobre fondo oscuro.
    acento_texto = ajusta(hexmes, peor_fondo, 4.5 if claro else 7.0, "#000000" if claro else "#FFFFFF")
    # botón primario: fondo de acento, texto blanco o casi negro con >= 4.5
    boton_bg = hexmes if claro else ajusta(hexmes, n["surface"], 3.0, "#FFFFFF")
    sobre = "#FFFFFF" if ratio("#FFFFFF", boton_bg) >= 4.5 else "#101810"
    if ratio(sobre, boton_bg) < 4.5:  # color intermedio: oscurecer el botón hasta cumplir con blanco
        boton_bg = ajusta(boton_bg, "#FFFFFF", 4.5, "#000000"); sobre = "#FFFFFF"
    # cabecera de temporada: degradado oscuro con texto blanco >= 4.5 en ambos extremos
    h_from = ajusta(hexmes, "#FFFFFF", 4.5, "#000000")
    h_to = mezcla(h_from, "#000000", 0.28)
    return {
        "bg": n["bg"], "surface": n["surface"], "border": n["border"], "text": n["text"], "text2": n["text2"],
        "tinte": mezcla(n["bg"], hexmes, 0.10 if claro else 0.18),
        "acento": hexmes, "acento_texto": acento_texto,
        "boton_bg": boton_bg, "boton_texto": sobre,
        "hero_desde": h_from, "hero_hasta": h_to, "hero_texto": "#FFFFFF",
        "oro": oro_ui(MARCOS[marco]["oro"], n["surface"], claro),
    }


def main(anio=2027):
    pal = dict(zip(MESES, PALETA_MES[anio]))
    out = {"anio_paleta": anio, "temporadas": TEMPORADAS, "marcos": {}}
    css = ["/* Jóvenes · 4 temporadas. Generado por tokens.py (paleta mensual %d). No editar a mano. */" % anio,
           "/* Uso: <html data-marco=\"vmad|viveadn\" data-tema=\"claro|oscuro\" data-mes=\"ene..dic\" data-temporada=\"brote|savia|cosecha|aguardo\"> */", ""]
    md = ["# Informe de contraste · Jóvenes · 4 temporadas", "",
          f"Paleta mensual: El Bosque {anio}. Criterio: WCAG 2.2 AA (texto normal 4.5, elementos de interfaz y texto grande 3.0). En modo oscuro el texto de acento se lleva a 7.0.", ""]
    fallos = []
    for marco in MARCOS:
        out["marcos"][marco] = {"meses": {}}
        md += [f"## Marco {marco}", "",
               "| Temporada | Mes | Acento | Texto acento / fondo | Texto acento / superficie | Botón (texto / fondo) | Hero blanco / desde | Hero blanco / hasta | Modo |",
               "|---|---|---|---|---|---|---|---|---|"]
        for t in TEMPORADAS:
            for m in t["meses"]:
                out["marcos"][marco]["meses"][m] = {"temporada": t["id"]}
                for modo in ("claro", "oscuro"):
                    k = tokens_mes(pal[m], modo, marco)
                    out["marcos"][marco]["meses"][m][modo] = k
                    r_bg, r_sf = ratio(k["acento_texto"], k["bg"]), ratio(k["acento_texto"], k["surface"])
                    r_bt = ratio(k["boton_texto"], k["boton_bg"])
                    r_h1, r_h2 = ratio(k["hero_texto"], k["hero_desde"]), ratio(k["hero_texto"], k["hero_hasta"])
                    r_tx, r_t2 = ratio(k["text"], k["bg"]), ratio(k["text2"], k["surface"])
                    r_t2b = ratio(k["text2"], k["bg"])
                    r_oro = ratio(k["oro"], k["surface"])
                    minimo_acento = 4.5 if modo == "claro" else 7.0
                    for nombre, v, minimo in (("acento/fondo", r_bg, minimo_acento), ("acento/superficie", r_sf, minimo_acento), ("botón", r_bt, 4.5),
                                              ("hero desde", r_h1, 4.5), ("hero hasta", r_h2, 4.5), ("texto", r_tx, 4.5),
                                              ("texto2/superficie", r_t2, 4.5), ("texto2/fondo", r_t2b, 4.5), ("oro/superficie", r_oro, 3.0)):
                        if v < minimo:
                            fallos.append(f"{marco} {m} {modo}: {nombre} {v:.2f} < {minimo}")
                    md.append(f"| {t['nombre']} | {m} | `{pal[m]}` | {r_bg:.1f} | {r_sf:.1f} | {r_bt:.1f} | {r_h1:.1f} | {r_h2:.1f} | {modo} |")
                    css.append(f":root[data-marco=\"{marco}\"][data-tema=\"{modo}\"][data-mes=\"{m}\"] {{")
                    for nombre, valor in k.items():
                        css.append(f"  --j-{nombre.replace('_', '-')}: {valor};")
                    css.append("}")
        md += ["", f"Neutros del marco {marco}:", "", "| Par | Claro | Oscuro |", "|---|---|---|"]
        for a, b in (("text", "bg"), ("text2", "bg"), ("text2", "surface")):
            md.append(f"| {a} sobre {b} | {ratio(MARCOS[marco]['claro'][a], MARCOS[marco]['claro'][b]):.1f} | {ratio(MARCOS[marco]['oscuro'][a], MARCOS[marco]['oscuro'][b]):.1f} |")
        md.append("")
    md += ["## Colores heredados que no deben usarse como texto", "",
           f"- `#4CAF50` (--jgreen del mockup) sobre `#F0F8F2`: {ratio('#4CAF50', '#F0F8F2'):.1f}:1. Solo decorativo o relleno de progreso.",
           f"- `#D4AA3A` (oro del mockup) sobre `#FFFFFF`: {ratio('#D4AA3A', '#FFFFFF'):.1f}:1. El oro de interfaz se ajusta por marco y modo hasta 3:1.",
           f"- `#F5A623` (oro ViveADN) sobre `#FFFFFF`: {ratio('#F5A623', '#FFFFFF'):.1f}:1. Mismo tratamiento.",
           f"- `#8AAA8C` (--txt3 del mockup) sobre `#F8F4EE`: {ratio('#8AAA8C', '#F8F4EE'):.1f}:1. No usar para texto de lectura.", ""]
    md += ["## Resultado", "", "Todos los pares evaluados cumplen." if not fallos else "Fallos:\n" + "\n".join("- " + f for f in fallos)]
    json.dump(out, open(AQUI / "tokens-estaciones.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(AQUI / "jovenes-estaciones.css", "w", encoding="utf-8").write("\n".join(css) + "\n")
    open(AQUI / "contraste.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"{len(MARCOS)} marcos x 12 meses x 2 modos. Fallos de contraste: {len(fallos)}")
    for f in fallos: print(" -", f)
    return len(fallos)


if __name__ == "__main__":
    raise SystemExit(1 if main() else 0)
