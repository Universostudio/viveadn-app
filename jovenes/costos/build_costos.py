#!/usr/bin/env python3
"""Modelo de costos de voces e idiomas · VMAD Jóvenes.
Genera costos.xlsx (supuestos editables + fórmulas), lo recalcula con LibreOffice,
verifica que no hay errores y escribe costos.md con los resultados recalculados.
Los volúmenes salen del contenido real (dic2026_jovenes.json). Los precios son supuestos
con nivel de confianza explícito: verificar en las páginas oficiales antes de contratar.
"""
import json, re, subprocess, shutil, pathlib, tempfile, sys
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

A = pathlib.Path(__file__).parent
dias = json.load(open(A / "../contenido/dic2026_jovenes.json", encoding="utf-8"))
clean = lambda s: re.sub(r"\*", "", s)

# ------------------------------------------------------------------ volumen real
audio = sum(len(x) for d in dias for x in [d["titulo"], d["raiz"]["verso"], d["raiz"]["ref"], *[clean(p) for p in d["tallo"]], d["hoja"], d["testimonio"], d["oracion"], d["fruto"]])
texto = audio + sum(len(d["plan_lectura"]["capitulo"]) + len(d["plan_lectura"]["complementarias"]) +
                    (len(d["palabra_original"]["termino"]) + len(d["palabra_original"]["sentido"]) if d["palabra_original"] else 0) for d in dias)
palabras = sum(len(re.findall(r"\w+", s)) for d in dias for s in [d["titulo"], d["raiz"]["verso"], *d["tallo"], d["hoja"], d["testimonio"], d["oracion"], d["fruto"], d["plan_lectura"]["complementarias"]])
NDIAS = len(dias)

IDIOMAS = [  # código, nombre, fase, multiplicador de revisión (0 = idioma fuente)
    ("es", "Español", 1, 0), ("en", "Inglés", 1, 1.0), ("pt", "Portugués", 1, 1.0),
    ("fr", "Francés", 2, 1.0), ("it", "Italiano", 2, 1.0), ("de", "Alemán", 2, 1.0), ("ro", "Rumano", 2, 1.0), ("pl", "Polaco", 2, 1.0),
    ("ru", "Ruso", 3, 1.3), ("uk", "Ucraniano", 3, 1.3), ("hi", "Hindi", 3, 1.3), ("ar", "Árabe", 3, 1.3),
    ("ko", "Coreano", 3, 1.5), ("zh", "Chino mandarín", 3, 1.5), ("ja", "Japonés", 3, 1.5),
    ("id", "Indonesio", 3, 1.0), ("tl", "Filipino", 3, 1.0),
]

wb = Workbook()
H = Font(bold=True, color="FFFFFF"); HF = PatternFill("solid", fgColor="1E3A2A"); INP = PatternFill("solid", fgColor="FFF4CC")
def cab(ws, fila, textos):
    for i, t in enumerate(textos, 1):
        c = ws.cell(fila, i, t); c.font = H; c.fill = HF; c.alignment = Alignment(wrap_text=True, vertical="center")

# ------------------------------------------------------------------ Supuestos
S = wb.active; S.title = "Supuestos"
S["A1"] = "Supuestos de costo · VMAD Jóvenes (celdas amarillas editables)"; S["A1"].font = Font(bold=True, size=13)
cab(S, 3, ["Concepto", "Bajo", "Medio", "Alto", "Unidad", "Fuente y confianza"])
SUP = [
    ("Precio de voz (TTS) por 1.000 caracteres", 0.08, 0.17, 0.22, "USD", "Derivado de planes: Creator ≈0,18 a 0,22; Pro ≈0,17 a 0,20; Scale ≈0,165 por 1.000 créditos. Bajo = modelos Flash (medio crédito por carácter). CONFIANZA MEDIA: fuentes de terceros discrepan; página oficial no accesible desde esta sesión."),
    ("Factor de regeneración (repeticiones por error de pronunciación)", 1.2, 1.5, 2.0, "x", "Supuesto propio. Los nombres bíblicos y términos hebreos y griegos obligan a repetir tomas. CONFIANZA BAJA."),
    ("DeepL por 1.000.000 de caracteres", 25, 25, 27.5, "USD", "Terceros: 25 USD (API Pro clásica) y 27,5 USD de exceso en el plan Growth. CONFIANZA MEDIA."),
    ("DeepL cuota fija mensual", 5.49, 5.49, 32.5, "USD", "Terceros: 5,49 USD (Pro clásica) o 32,5 USD (Growth, 1 M caracteres). CONFIANZA MEDIA."),
    ("Revisión nativa y teológica por 1.000 palabras", 15, 30, 50, "EUR", "Supuesto propio de mercado para posedición más lectura pastoral. CONFIANZA BAJA: pedir cotización."),
    ("QA de audio por idioma y mes (escucha nativa)", 30, 60, 120, "EUR", "1, 2 o 4 horas a 30 EUR. Supuesto propio. CONFIANZA BAJA."),
    ("Canción e instrumental por mes (independiente del idioma)", 0, 30, 150, "EUR", "Bajo = biblioteca con licencia ya pagada. Supuesto propio."),
    ("Almacenamiento y entrega por GB al mes", 0.015, 0.015, 0.03, "USD", "Orden de magnitud de almacenamiento de objetos con salida gratuita. CONFIANZA BAJA, impacto mínimo."),
    ("Tipo de cambio EUR por 1 USD", 0.92, 0.92, 0.92, "EUR/USD", "Supuesto. Actualizar."),
    ("Megabytes de audio por día y canal de voz", 1.9, 1.9, 1.9, "MB", "Dos minutos a 128 kbps."),
]
for i, fila in enumerate(SUP):
    r = 4 + i
    for j, v in enumerate(fila, 1):
        c = S.cell(r, j, v)
        if j in (2, 3, 4): c.fill = INP
        if j == 6: c.alignment = Alignment(wrap_text=True, vertical="top")
FILA = {"tts": 4, "retake": 5, "deepl": 6, "deepl_fija": 7, "rev": 8, "qa": 9, "musica": 10, "gb": 11, "fx": 12, "mb": 13}
S["A16"] = "Planes de ElevenLabs para cubrir el consumo mensual (cifras prudentes de fuentes discrepantes)"; S["A16"].font = Font(bold=True)
cab(S, 17, ["Plan", "Créditos al mes", "Precio USD al mes"])
PLANES = [("Creator", 100000, 22), ("Pro", 500000, 99), ("Scale", 1800000, 299)]
for i, p in enumerate(PLANES):
    for j, v in enumerate(p, 1):
        c = S.cell(18 + i, j, v)
        if j > 1: c.fill = INP
S["A22"] = "Un crédito equivale a un carácter en los modelos estándar. Con modelos Flash es medio crédito."
for col, w in zip("ABCDEF", (62, 11, 11, 11, 10, 110)): S.column_dimensions[col].width = w

# ------------------------------------------------------------------ Volumen
V = wb.create_sheet("Volumen")
V["A1"] = "Volumen real del contenido (perfil Jóvenes, diciembre 2026)"; V["A1"].font = Font(bold=True, size=13)
cab(V, 3, ["Concepto", "Valor", "Nota"])
filas = [
    ("Días de contenido", NDIAS, "Edición de 30 días"),
    ("Caracteres narrados en 30 días", audio, "Título, versículo, reflexión, reto, pregunta, oración y fruto. Sin plan de lectura."),
    ("Caracteres a traducir en 30 días", texto, "Narrado más plan de lectura y palabra original"),
    ("Palabras a revisar en 30 días", palabras, "Base para la revisión humana"),
    ("Días del año", 365, "Escala de 30 días a un año con el mismo ritmo de texto"),
    ("Factor de escala a un año", "=B8/B4", ""),
    ("Caracteres narrados por año y idioma", "=B5*B9", ""),
    ("Caracteres a traducir por año y idioma", "=B6*B9", ""),
    ("Palabras a revisar por año y idioma", "=B7*B9", ""),
    ("Minutos de audio por día (aprox. 950 caracteres por minuto)", "=B5/B4/950", "Referencia de duración"),
]
for i, (a, b, c) in enumerate(filas):
    V.cell(4 + i, 1, a); V.cell(4 + i, 2, b); V.cell(4 + i, 3, c)
V.column_dimensions["A"].width = 58; V.column_dimensions["B"].width = 16; V.column_dimensions["C"].width = 80

# ------------------------------------------------------------------ Idiomas
I = wb.create_sheet("Idiomas")
I["A1"] = "Hoja de ruta de 17 idiomas (propuesta de trabajo: confirmar con Harold y Yina)"; I["A1"].font = Font(bold=True, size=13)
cab(I, 3, ["Código", "Idioma", "Fase", "Multiplicador de revisión", "Se traduce (1/0)", "Con voz (1/0)"])
for i, (cod, nom, fase, mult) in enumerate(IDIOMAS):
    r = 4 + i
    for j, v in enumerate([cod, nom, fase, mult, 0 if cod == "es" else 1, 1], 1):
        c = I.cell(r, j, v)
        if j in (3, 4): c.fill = INP
UL = 3 + len(IDIOMAS)
I.cell(UL + 2, 1, "Multiplicador: 1,0 escritura latina, 1,3 cirílico, hindi y árabe (derecha a izquierda), 1,5 chino, japonés y coreano. Supuesto propio.")
for col, w in zip("ABCDEF", (9, 18, 7, 24, 16, 14)): I.column_dimensions[col].width = w

# ------------------------------------------------------------------ Resumen
R = wb.create_sheet("Resumen")
R["A1"] = "Costo anual por fase y escenario · perfil Jóvenes (EUR)"; R["A1"].font = Font(bold=True, size=13)
R["A2"] = "Cada fase incluye los idiomas de las fases anteriores. Costos recurrentes de producción de un año de contenido de 365 días."
rng = lambda col: f"Idiomas!${col}$4:${col}${UL}"
fases = [(1, "Fase 1 · ES, EN, PT"), (2, "Fase 2 · +FR, IT, DE, RO, PL (8 idiomas)"), (3, "Fase 3 · +9 idiomas (17 idiomas)")]
fila = 4
resumen_pos = {}
for f, nom in fases:
    R.cell(fila, 1, nom).font = Font(bold=True, size=12)
    cab(R, fila + 1, ["Concepto", "Bajo", "Medio", "Alto"])
    lineas = [
        ("Idiomas con voz", lambda c: f'=SUMIFS({rng("F")},{rng("C")},"<="&{f})'),
        ("Idiomas a traducir", lambda c: f'=SUMIFS({rng("E")},{rng("C")},"<="&{f})'),
        ("Suma de multiplicadores de revisión", lambda c: f'=SUMIFS({rng("D")},{rng("C")},"<="&{f})'),
        ("Voz (ElevenLabs, EUR)", lambda c: f'={c}{{r0}}*Volumen!$B$10*Supuestos!{c}${FILA["retake"]}/1000*Supuestos!{c}${FILA["tts"]}*Supuestos!{c}${FILA["fx"]}'),
        ("Traducción automática (DeepL, EUR)", lambda c: f'=({c}{{r1}}*Volumen!$B$11/1000000*Supuestos!{c}${FILA["deepl"]}+12*Supuestos!{c}${FILA["deepl_fija"]})*Supuestos!{c}${FILA["fx"]}'),
        ("Revisión nativa y teológica (EUR)", lambda c: f'={c}{{r2}}*Volumen!$B$12/1000*Supuestos!{c}${FILA["rev"]}'),
        ("QA de audio (EUR)", lambda c: f'={c}{{r0}}*12*Supuestos!{c}${FILA["qa"]}'),
        ("Canción e instrumental (EUR)", lambda c: f'=12*Supuestos!{c}${FILA["musica"]}'),
        ("Almacenamiento y entrega (EUR)", lambda c: f'={c}{{r0}}*{NDIAS and 365}*Supuestos!{c}${FILA["mb"]}/1024*12*Supuestos!{c}${FILA["gb"]}*Supuestos!{c}${FILA["fx"]}'),
        ("TOTAL anual (EUR)", None),
        ("Revisión humana como % del total", None),
        ("Créditos ElevenLabs necesarios al mes (perfil Jóvenes)", lambda c: f'={c}{{r0}}*Volumen!$B$5*Supuestos!{c}${FILA["retake"]}'),
        ("Plan mínimo que cubre ese consumo", None),
    ]
    r0 = fila + 2; r1 = r0 + 1; r2 = r0 + 2
    rows = {}
    for k, (nombre, fn) in enumerate(lineas):
        r = r0 + k; rows[nombre] = r
        R.cell(r, 1, nombre)
        for ci, col in enumerate("BCD", 2):
            sc = col  # misma letra de columna en Supuestos (B,C,D = bajo, medio, alto)
            if nombre == "TOTAL anual (EUR)":
                v = f"=SUM({col}{r0+3}:{col}{r0+8})"
            elif nombre == "Revisión humana como % del total":
                v = f"={col}{r0+5}/{col}{rows['TOTAL anual (EUR)']}"
            elif nombre == "Plan mínimo que cubre ese consumo":
                cr = rows["Créditos ElevenLabs necesarios al mes (perfil Jóvenes)"]
                v = (f'=IF({col}{cr}<=Supuestos!$B$18,"Creator",IF({col}{cr}<=Supuestos!$B$19,"Pro",'
                     f'IF({col}{cr}<=Supuestos!$B$20,"Scale","Scale x"&ROUNDUP({col}{cr}/Supuestos!$B$20,0))))')
            else:
                v = fn(sc).replace("{r0}", str(r0)).replace("{r1}", str(r1)).replace("{r2}", str(r2))
            c = R.cell(r, ci, v)
            if nombre.endswith("(EUR)") or nombre.startswith("TOTAL"): c.number_format = '#,##0'
            if "%" in nombre: c.number_format = "0%"
            if "Créditos" in nombre: c.number_format = '#,##0'
            if nombre.startswith("TOTAL"): c.font = Font(bold=True)
        if nombre.startswith("TOTAL"): R.cell(r, 1).font = Font(bold=True)
    resumen_pos[f] = rows
    fila = r0 + len(lineas) + 2
R.column_dimensions["A"].width = 58
for col in "BCD": R.column_dimensions[col].width = 16

wb.save(A / "costos.xlsx")

# ------------------------------------------------------------------ recálculo y verificación
tmp = pathlib.Path(tempfile.mkdtemp())
subprocess.run(["soffice", "--headless", "--convert-to", "xlsx", "--outdir", str(tmp), str(A / "costos.xlsx")], check=True, capture_output=True, timeout=180)
calc = load_workbook(tmp / "costos.xlsx", data_only=True)
errores = []
for ws in calc.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith("#"): errores.append(f"{ws.title}!{c.coordinate} {c.value}")
            if c.value is None and False: pass
if errores:
    print("ERRORES DE FÓRMULA:", errores); sys.exit(1)
shutil.copy(tmp / "costos.xlsx", A / "costos.xlsx")  # versión con valores en caché
RC = calc["Resumen"]
res = {}
for f, rows in resumen_pos.items():
    res[f] = {n: [RC.cell(r, c).value for c in (2, 3, 4)] for n, r in rows.items()}
json.dump(res, open(A / "resumen_costos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({f: {k: res[f][k] for k in ("TOTAL anual (EUR)", "Plan mínimo que cubre ese consumo")} for f in res}, ensure_ascii=False, indent=1))
print("volumen:", dict(dias=NDIAS, caracteres_audio=audio, caracteres_texto=texto, palabras=palabras))
