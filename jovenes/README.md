# VMAD Jóvenes (14+) · Diciembre 2026 · 30 días

Empieza por `01-plan-version-jovenes.md`. Después `02-auditoria-matriz-diciembre.md`, `contenido/guia-registro-juvenil.md`, `interfaz/momentos-interfaz.md` y `costos/costos.md`.

Para ver el resultado: abrir `interfaz/preview-jovenes.html` en un navegador.

## Regenerar todo

```bash
python3 contenido/build.py          # valida reglas VMAD, registro juvenil y audio sin esperas. Genera json y md. Sale con error si algo falla
python3 interfaz/tokens.py          # tokens de color y verificación de contraste
python3 interfaz/build_preview.py   # prototipo autocontenido con los 30 días
python3 costos/build_costos.py      # modelo de costos (requiere LibreOffice para recalcular)
python3 costos/escribir_costos_md.py  # regenera costos.md con las cifras recalculadas
```

Los ajustes editoriales se hacen en `contenido/texto_*.txt`. Los scripts usan solo la biblioteca estándar de Python, salvo `build_costos.py`, que necesita `openpyxl`.
