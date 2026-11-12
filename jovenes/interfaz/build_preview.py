#!/usr/bin/env python3
"""Inyecta tokens CSS y los 30 días reales en la plantilla y genera preview-jovenes.html (autocontenido)."""
import json, pathlib
A = pathlib.Path(__file__).parent
t = (A / "plantilla_preview.html").read_text(encoding="utf-8")
css = (A / "jovenes-estaciones.css").read_text(encoding="utf-8")
datos = json.load(open(A / "../contenido/dic2026_jovenes.json", encoding="utf-8"))
t = t.replace("/*TOKENS*/", css).replace("/*DATOS*/", json.dumps(datos, ensure_ascii=False)).replace("/*MESES*/", "{}")
(A / "preview-jovenes.html").write_text(t, encoding="utf-8")
print("preview-jovenes.html", len(t) // 1024, "KB")
