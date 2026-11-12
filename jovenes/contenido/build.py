#!/usr/bin/env python3
"""Construye la edición Jóvenes (14+) de Diciembre 2026 a partir de:
  - texto_*.txt            (redacción nueva para jóvenes)
  - fuente/dic2026_adultos_extraido.json  (matriz de adultos: versículo, referencia, plan)
Salidas:
  - dic2026_jovenes.json   (datos para app, audio y maquetación)
  - dic2026_jovenes.md     (lectura editorial)
  - validacion.txt         (informe de reglas VMAD)
Uso: python3 build.py
"""
import json, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import registro

AQUI = pathlib.Path(__file__).parent
ADULTOS = json.load(open(AQUI / "fuente/dic2026_adultos_extraido.json", encoding="utf-8"))

# ---------------------------------------------------------------- correcciones a la matriz
# Cada override documenta un defecto de la matriz de adultos (ver docs 02-auditoria).
OVERRIDES = {
    25: {  # el texto de adultos mezcla Mt 1:25 con Lc 2:7; se usa el texto exacto de Lc 2:21 (RVR1960)
        "verso": "«Cumplidos los ocho días para circuncidar al niño, le pusieron por nombre JESÚS, el cual le había sido puesto por el ángel antes que fuese concebido.»",
        "cap": "Lucas 2:1-21",
        "comp": "Mateo 1:21 · Juan 3:16-17",
        "nota": "Texto del versículo corregido respecto a la matriz de adultos. Verificar contra la edición RVR1960 impresa.",
    },
    27: {  # campos desplazados en la matriz: el plan de lectura apuntaba a otro pasaje
        "cap": "Lucas 2:25-35",
        "comp": "Salmo 4:8 · Filipenses 4:7",
        "nota": "Plan de lectura reconstruido. En la matriz de adultos los campos del día 27 están desplazados.",
    },
}
# El día 30 de jóvenes fusiona los días 30 y 31 de la matriz (versículo del 31, gratitud del 30).
FUSION_30 = {
    "n": 30,
    "titulo": "El Árbol que Sabe Quién Es",
    "dia": "Miércoles",
    "fecha": "Miércoles 30 y jueves 31 de diciembre",
    "ref": "Salmo 1:3",
    "verso": ADULTOS[30]["verso"],
    "cap": "Salmo 1:1-6",
    "comp": "1 Pedro 1:3-9 · Jeremías 17:7-8",
    "nota": "Fusiona los días 30 y 31 de la matriz de adultos. El 31 de diciembre se reserva para el momento de cierre del año en la interfaz.",
}

DIM = {"Personal": "P", "Relacional": "R", "Social": "S"}
CAMPOS = ["dim", "palabra", "tallo", "hoja", "test", "oracion", "fruto"]


def parse_texto(path):
    dias, cur, campo = {}, None, None
    for linea in open(path, encoding="utf-8").read().splitlines():
        m = re.match(r"=== (\d+) ===", linea)
        if m:
            cur = int(m.group(1)); dias[cur] = {k: "" for k in CAMPOS}; campo = None
            continue
        if cur is None:
            continue
        m = re.match(r"(dim|palabra|tallo|hoja|test|oracion|fruto):\s?(.*)$", linea)
        if m:
            campo = m.group(1); dias[cur][campo] = m.group(2)
            continue
        if campo == "tallo":
            dias[cur]["tallo"] += ("\n" + linea) if dias[cur]["tallo"] else linea
    for d in dias.values():
        d["tallo"] = d["tallo"].strip()
    return dias


def cargar():
    nuevos = {}
    for f in sorted(AQUI.glob("texto_*.txt")):
        nuevos.update(parse_texto(f))
    out = []
    for n in range(1, 31):
        base = FUSION_30.copy() if n == 30 else dict(ADULTOS[n - 1])
        base.update(OVERRIDES.get(n, {}))
        base.setdefault("fecha", f"{base['dia']} {n} de diciembre")
        t = nuevos[n]
        pal = [x.strip() for x in t["palabra"].split("|")] if t["palabra"].strip() else []
        out.append({
            "dia_n": n,
            "fecha": base["fecha"],
            "titulo": base["titulo"],
            "dimension": t["dim"],
            "raiz": {"verso": base["verso"], "ref": base["ref"] + ", RVR1960"},
            "tallo": t["tallo"].split("\n\n"),
            "palabra_original": {"termino": pal[0], "sentido": pal[1] if len(pal) > 1 else ""} if pal else None,
            "hoja": t["hoja"],
            "testimonio": t["test"],
            "oracion": t["oracion"],
            "fruto": t["fruto"],
            "plan_lectura": {"capitulo": base["cap"], "complementarias": base["comp"]},
            "nota_editorial": base.get("nota", ""),
            "libro": {"pagina_escritura": True, "pregunta": t["test"], "lineas_sugeridas": 6},
        })
        out[-1]["audio"] = guion_audio(out[-1])
    return out


# ---------------------------------------------------------------- validación
BANNED = [(r"cotidian", "palabra prohibida 'cotidiano'"), (r"—", "raya larga (em dash)"), (r"–", "raya media"),
          (r" - ", "guion parentético"), (r"\b(podés|escuchás|tenés|sos|querés|vos)\b", "voseo"),
          (r"devocional", "autorreferencia al devocional")]
CIERRE = "En el nombre de Jesús, amén."
TALLO_MIN, TALLO_MAX = 165, 230
# Registro juvenil (ver guia-registro-juvenil.md). Pensado para pantalla y para escucha.
FRASE_MAX_DURA = 32     # ninguna frase del TALLO, la HOJA o el TESTIMONIO supera esto (fallo)
FRASE_MAX_AVISO = 28    # a partir de aquí se avisa
FH_MIN = 70             # Fernández-Huerta mínimo por día en el TALLO (aviso). La matriz de Adultos promedia 70
PAL_FRASE_DIA_MAX = 18.0     # palabras por frase en el TALLO, por día (aviso)
PAL_FRASE_MES_MAX = 16.5     # promedio del mes (aviso). La matriz de Adultos promedia 17,2 con la misma medida
# Guion de audio: la pregunta se anuncia y el día continúa. Ninguna pausa puede dejar al oyente esperando.
PAUSA_MAX_MS = 3000
PAUSA_TOTAL_MAX_MS = 12000
CPS = 950 / 60          # caracteres narrados por segundo


def guion_audio(d):
    """Guion de audio continuo. La pregunta del testimonio es un segmento 'anunciado': se lee, suena un
    puente instrumental corto y el día sigue con la oración. Nunca espera la respuesta del oyente: la
    respuesta escrita pertenece al libro."""
    clean = lambda t: re.sub(r"\*", "", t)
    seg = [
        {"id": "titulo", "texto": f"{d['titulo']}. {d['fecha']}.", "pausa_despues_ms": 700},
        {"id": "raiz", "texto": f"{clean(d['raiz']['verso'])} {d['raiz']['ref']}.", "pausa_despues_ms": 900},
    ]
    for i, p in enumerate(d["tallo"], 1):
        seg.append({"id": f"tallo_{i}", "texto": clean(p), "pausa_despues_ms": 500})
    seg += [
        {"id": "hoja", "texto": d["hoja"], "pausa_despues_ms": 700},
        {"id": "testimonio", "modo": "anunciada", "texto": d["testimonio"], "pausa_despues_ms": 1200,
         "puente_instrumental_ms": 2500, "espera_usuario": False},
        {"id": "oracion", "texto": d["oracion"], "pausa_despues_ms": 1000},
        {"id": "fruto", "texto": d["fruto"], "pausa_despues_ms": 0},
    ]
    chars = sum(len(x["texto"]) for x in seg)
    pausas = sum(x["pausa_despues_ms"] + x.get("puente_instrumental_ms", 0) for x in seg)
    return {"segmentos": seg, "caracteres": chars, "pausas_ms": pausas,
            "duracion_estimada_s": round(chars / CPS + pausas / 1000)}


def palabras(s):
    return len(re.findall(r"[\wáéíóúüñÁÉÍÓÚÜÑ]+", re.sub(r"\*", "", s)))


def validar(dias):
    fallos, avisos, filas = [], [], []
    for d in dias:
        n = d["dia_n"]
        cuerpo = " ".join(d["tallo"] + [d["hoja"], d["testimonio"], d["oracion"], d["fruto"], d["titulo"]])
        for rx, msg in BANNED:
            if re.search(rx, cuerpo, re.I):
                fallos.append(f"Día {n}: {msg}")
        wc = palabras(" ".join(d["tallo"]))
        # Rango Jóvenes 14+: banda 13 a 17 de la Guía (150 a 220) ampliada a 230 por la banda 18 a 30 (200 a 280).
        if not TALLO_MIN <= wc <= TALLO_MAX:
            avisos.append(f"Día {n}: TALLO {wc} palabras (objetivo {TALLO_MIN} a {TALLO_MAX})")
        if len(d["tallo"]) != 3:
            fallos.append(f"Día {n}: TALLO tiene {len(d['tallo'])} párrafos (esperados 3)")
        fl = len(d["fruto"])
        if not 100 <= fl <= 150:
            fallos.append(f"Día {n}: FRUTO {fl} caracteres (rango 100 a 150)")
        if "porque" not in d["fruto"].lower():
            fallos.append(f"Día {n}: FRUTO sin 'porque' teológico")
        if d["testimonio"].count("?") != 1 or not d["testimonio"].endswith("?"):
            fallos.append(f"Día {n}: TESTIMONIO debe ser una sola pregunta")
        if "?" in d["hoja"]:
            fallos.append(f"Día {n}: HOJA contiene pregunta")
        if not d["oracion"].endswith(CIERRE):
            fallos.append(f"Día {n}: ORACIÓN no cierra con '{CIERRE}'")
        if d["dimension"] not in DIM:
            fallos.append(f"Día {n}: dimensión inválida")
        pal = d["palabra_original"]
        if pal and f"*{pal['termino'].split(' | ')[0].split()[0]}" not in " ".join(d["tallo"]) and pal["termino"] not in " ".join(d["tallo"]):
            avisos.append(f"Día {n}: el término '{pal['termino']}' no aparece en cursiva en el TALLO")
        # --- registro juvenil
        texto_lectura = " ".join(d["tallo"])
        for campo, txt in (("TALLO", texto_lectura), ("HOJA", d["hoja"]), ("TESTIMONIO", d["testimonio"])):
            for k, f in registro.largas(txt, FRASE_MAX_AVISO):
                (fallos if k > FRASE_MAX_DURA else avisos).append(f"Día {n}: {campo} frase de {k} palabras: {f[:70]}...")
        fh = registro.fernandez_huerta(texto_lectura)
        if fh < FH_MIN:
            avisos.append(f"Día {n}: Fernández-Huerta {fh:.0f} < {FH_MIN} en el TALLO")
        pf = len(registro.palabras(texto_lectura)) / len(registro.frases(texto_lectura))
        if pf > PAL_FRASE_DIA_MAX:
            avisos.append(f"Día {n}: {pf:.1f} palabras por frase en el TALLO (máx {PAL_FRASE_DIA_MAX})")
        # --- audio sin esperas
        a = d["audio"]
        for sg in a["segmentos"]:
            if sg["pausa_despues_ms"] > PAUSA_MAX_MS or sg.get("espera_usuario"):
                fallos.append(f"Día {n}: segmento '{sg['id']}' deja esperando al oyente")
        if a["pausas_ms"] > PAUSA_TOTAL_MAX_MS:
            fallos.append(f"Día {n}: pausas totales {a['pausas_ms']} ms (máx {PAUSA_TOTAL_MAX_MS})")
        if [x for x in a["segmentos"] if x["id"] == "testimonio"][0].get("modo") != "anunciada":
            fallos.append(f"Día {n}: el testimonio debe ser 'anunciada' en el audio")
        filas.append((n, d["dimension"][0], wc, fl, palabras(d["oracion"]), fh, pf, a["duracion_estimada_s"]))
    for a, b in zip(dias, dias[1:]):
        if a["dimension"] == b["dimension"]:
            fallos.append(f"Días {a['dia_n']} y {b['dia_n']}: misma dimensión consecutiva ({a['dimension']})")
    media_mes = sum(f[6] for f in filas) / len(filas)
    if media_mes > PAL_FRASE_MES_MAX:
        avisos.append(f"Promedio del mes {media_mes:.1f} palabras por frase en el TALLO (máx {PAL_FRASE_MES_MAX})")
    cuentas = {k: sum(1 for d in dias if d["dimension"] == k) for k in DIM}
    return fallos, avisos, filas, cuentas


def md(dias):
    L = ["# Vida Más Allá del Domingo · Diciembre 2026 · Edición Jóvenes (14+)", "",
         "*Esperanza Eterna · Adviento · El árbol que aguarda.* Treinta días. Mismo versículo, mismo plan de lectura y mismo narrador (Simeón) que la edición de Adultos.", "",
         "> Sobre MI TESTIMONIO: en el libro cada pregunta tiene su página para escribir la respuesta. En el audio y en la app la pregunta se anuncia y el día continúa sin pausa de espera.", ""]
    for d in dias:
        L += [f"## Día {d['dia_n']} · {d['titulo']}", f"*{d['fecha']} · dimensión {d['dimension']}*", ""]
        L += [f"**RAÍZ**", f"{d['raiz']['verso']}", f"{d['raiz']['ref']}", "", "**TALLO**"]
        L += [p + "\n" for p in d["tallo"]]
        if d["palabra_original"]:
            p = d["palabra_original"]
            L += [f"*Palabra original:* {p['termino']}. {p['sentido']}", ""]
        L += [f"**HOJA** ({d['dimension']}) {d['hoja']}", "", f"**MI TESTIMONIO** ({d['dimension']}) {d['testimonio']}", "",
              f"**ORACIÓN** {d['oracion']}", "", f"**FRUTO** {d['fruto']}", "",
              f"**PLAN DE LECTURA** Capítulo del día: {d['plan_lectura']['capitulo']}. Lecturas complementarias: {d['plan_lectura']['complementarias']}", ""]
        if d["nota_editorial"]:
            L += [f"> Nota editorial: {d['nota_editorial']}", ""]
    return "\n".join(L)


def main():
    dias = cargar()
    fallos, avisos, filas, cuentas = validar(dias)
    json.dump(dias, open(AQUI / "dic2026_jovenes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(AQUI / "dic2026_jovenes.md", "w", encoding="utf-8").write(md(dias))
    tw = [f[2] for f in filas]; fl = [f[3] for f in filas]
    rep = ["VALIDACIÓN · VMAD Diciembre 2026 · Jóvenes", "",
           f"Días: {len(dias)}   Dimensiones: {cuentas}",
           f"TALLO palabras: mín {min(tw)} · media {sum(tw)/len(tw):.0f} · máx {max(tw)}",
           f"FRUTO caracteres: mín {min(fl)} · media {sum(fl)/len(fl):.0f} · máx {max(fl)}",
           f"Fernández-Huerta (TALLO): mín {min(f[5] for f in filas):.0f} · media {sum(f[5] for f in filas)/len(filas):.0f}",
           f"Palabras por frase (TALLO): media {sum(f[6] for f in filas)/len(filas):.1f} · máx por día {max(f[6] for f in filas):.1f}",
           f"Duración de audio por día: mín {min(f[7] for f in filas)} s · media {sum(f[7] for f in filas)/len(filas):.0f} s · máx {max(f[7] for f in filas)} s", "",
           f"FALLOS ({len(fallos)})"] + [" - " + f for f in fallos] + ["", f"AVISOS ({len(avisos)})"] + [" - " + a for a in avisos]
    open(AQUI / "validacion.txt", "w", encoding="utf-8").write("\n".join(rep) + "\n")
    print("\n".join(rep))
    sys.exit(1 if fallos else 0)


if __name__ == "__main__":
    main()
