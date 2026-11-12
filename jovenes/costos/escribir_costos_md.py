#!/usr/bin/env python3
"""Genera costos.md desde resumen_costos.json y el contenido, para que las cifras nunca queden desfasadas."""
import json, pathlib, re
A = pathlib.Path(__file__).parent
r = json.load(open(A / "resumen_costos.json", encoding="utf-8"))
d = json.load(open(A / "../contenido/dic2026_jovenes.json", encoding="utf-8"))
n = lambda x: f"{round(x):,}".replace(",", ".")
m = lambda k, f, i=1: r[str(f)][k][i]
rg = r["registro"]
audio = sum(x["audio"]["caracteres"] for x in d)
from openpyxl import load_workbook
V = load_workbook(A / "costos.xlsx", data_only=True)["Volumen"]
texto, pal, anual_c, anual_p, anual_a = V["B6"].value, V["B7"].value, V["B11"].value, V["B12"].value, V["B15"].value
anuales_audio = V["B10"].value
cr = [m("Créditos ElevenLabs necesarios al mes (perfil Jóvenes)", f) for f in (1, 2, 3)]
plan = [r[str(f)]["Plan mínimo que cubre ese consumo"][1] for f in (1, 2, 3)]
dur = sum(x["audio"]["duracion_estimada_s"] for x in d) / len(d)
L = lambda k, f: f"{n(m(k, f, 0))} a {n(m(k, f, 2))}"
tot = lambda f: m("TOTAL anual (EUR)", f)
rev = lambda f: m("Revisión humana como % del total", f) * 100
md = f"""# Evaluación y costo de voces e idiomas · Jóvenes

Modelo en `costos.xlsx` (celdas amarillas editables, fórmulas vivas), regenerable con `build_costos.py`, que recalcula el libro con LibreOffice y falla si alguna fórmula devuelve error. Este informe se genera con `escribir_costos_md.py` a partir de esos resultados. Los volúmenes salen del contenido real y los precios son supuestos con su nivel de confianza escrito junto a cada uno.

## Conclusión

Producir audio y traducción con herramientas automáticas cuesta poco. Lo que cuesta es que una persona de cada idioma revise el texto con ojo pastoral y escuche el audio. En el escenario medio, la voz y la traducción automática suman menos del 6% del costo anual de la Fase 1, y la revisión humana más el control de calidad del audio suman cerca del 90%. Si se quiere crecer a 17 idiomas, el presupuesto se decide casi por completo en la contratación de revisores y no en la suscripción de voz.

El lenguaje juvenil añade un costo propio y previo a las traducciones, porque cada idioma se traduce desde el español ya adaptado. Para todo el libro de 365 días cuesta entre {n(rg['TOTAL primer año, Ruta A'][0])} y {n(rg['TOTAL primer año, Ruta A'][2])} euros el primer año si el borrador lo hace una herramienta bajo control editorial, y entre {n(rg['TOTAL primer año, Ruta B'][0])} y {n(rg['TOTAL primer año, Ruta B'][2])} si lo reescribe una persona. Ver la sección «Adaptar el lenguaje de todo el libro».

## Volumen real (30 días de Jóvenes)

| Concepto | Valor |
|---|---|
| Caracteres narrados (guion de audio) | {n(audio)} (media de {n(audio/30)} por día, unos {round(dur/60, 1)} minutos con las pausas) |
| Caracteres a traducir | {n(texto)} |
| Palabras a revisar | {n(pal)} |
| Escala a un año (365 días) | {n(anuales_audio)} caracteres narrados y {n(anual_p)} palabras por idioma |
| Palabras que se reescriben al registro juvenil, por año | {n(anual_a)} |

## Costo anual por fase, en euros

Cada fase incluye los idiomas de la anterior. Fase 1: español, inglés y portugués, que es lo que ya prevé la hoja de ruta de 2027. Fase 2: francés, italiano, alemán, rumano y polaco. Fase 3: nueve idiomas más hasta 17 (ruso, ucraniano, hindi, árabe, coreano, chino, japonés, indonesio y filipino). La lista de 17 es una propuesta de trabajo, porque los documentos del proyecto hablan de 17 idiomas sin nombrarlos.

| Línea (escenario medio) | Fase 1 · 3 idiomas | Fase 2 · 8 idiomas | Fase 3 · 17 idiomas |
|---|---|---|---|
| Voz (ElevenLabs) | {n(m('Voz (ElevenLabs, EUR)',1))} | {n(m('Voz (ElevenLabs, EUR)',2))} | {n(m('Voz (ElevenLabs, EUR)',3))} |
| Traducción automática (DeepL) | {n(m('Traducción automática (DeepL, EUR)',1))} | {n(m('Traducción automática (DeepL, EUR)',2))} | {n(m('Traducción automática (DeepL, EUR)',3))} |
| Revisión nativa y teológica | {n(m('Revisión nativa y teológica (EUR)',1))} | {n(m('Revisión nativa y teológica (EUR)',2))} | {n(m('Revisión nativa y teológica (EUR)',3))} |
| QA de audio (escucha nativa) | {n(m('QA de audio (EUR)',1))} | {n(m('QA de audio (EUR)',2))} | {n(m('QA de audio (EUR)',3))} |
| Canción e instrumental | {n(m('Canción e instrumental (EUR)',1))} | {n(m('Canción e instrumental (EUR)',2))} | {n(m('Canción e instrumental (EUR)',3))} |
| Almacenamiento y entrega | {n(m('Almacenamiento y entrega (EUR)',1))} | {n(m('Almacenamiento y entrega (EUR)',2))} | {n(m('Almacenamiento y entrega (EUR)',3))} |
| **Total anual, medio** | **{n(tot(1))}** | **{n(tot(2))}** | **{n(tot(3))}** |
| Rango bajo a alto | {L('TOTAL anual (EUR)',1)} | {L('TOTAL anual (EUR)',2)} | {L('TOTAL anual (EUR)',3)} |
| Revisión humana sobre el total | {rev(1):.0f}% | {rev(2):.0f}% | {rev(3):.0f}% |

Esto cubre solo el perfil Jóvenes. Los otros tres perfiles tienen volúmenes de texto parecidos o menores, así que el costo de revisión crece de forma casi lineal con cada perfil y cada idioma.

## Adaptar el lenguaje de todo el libro

Sí hay que cambiar la redacción, aunque menos de lo que parece, y la medición lo justifica. La edición Jóvenes ya usa un vocabulario más sencillo que la matriz de Adultos (las palabras de cuatro o más sílabas bajan del 12% al 6,5%), pero la matriz de Adultos tiene frases de hasta 69 palabras y 30 frases por encima de 32. Para un lector de 14 años que además escucha el audio, esa longitud es el principal obstáculo, más que el vocabulario. La regla que se aplica a todo el libro, comprobada por código, está en `contenido/guia-registro-juvenil.md`.

Alcance: se reescriben la reflexión, el reto, la pregunta, la oración y el fruto, unas {n(anual_a)} palabras por año. El versículo, el título y el plan de lectura no cambian.

| Línea | Bajo | Medio | Alto |
|---|---|---|---|
| Guía de registro y glosario (una sola vez) | {n(rg['Guía de registro y glosario (única vez)'][0])} | {n(rg['Guía de registro y glosario (única vez)'][1])} | {n(rg['Guía de registro y glosario (única vez)'][2])} |
| Panel de lectores de 14 a 18 años (4 trimestres) | {n(rg['Panel de lectores (4 trimestres)'][0])} | {n(rg['Panel de lectores (4 trimestres)'][1])} | {n(rg['Panel de lectores (4 trimestres)'][2])} |
| Ruta A: borrador con IA bajo control de registro, más revisión pastoral | {n(rg['Ruta A · Borrador con IA + revisión pastoral'][0])} | {n(rg['Ruta A · Borrador con IA + revisión pastoral'][1])} | {n(rg['Ruta A · Borrador con IA + revisión pastoral'][2])} |
| Ruta B: reescritura humana completa, más revisión pastoral | {n(rg['Ruta B · Reescritura humana + revisión pastoral'][0])} | {n(rg['Ruta B · Reescritura humana + revisión pastoral'][1])} | {n(rg['Ruta B · Reescritura humana + revisión pastoral'][2])} |
| **Total primer año, Ruta A** | **{n(rg['TOTAL primer año, Ruta A'][0])}** | **{n(rg['TOTAL primer año, Ruta A'][1])}** | **{n(rg['TOTAL primer año, Ruta A'][2])}** |
| **Total primer año, Ruta B** | **{n(rg['TOTAL primer año, Ruta B'][0])}** | **{n(rg['TOTAL primer año, Ruta B'][1])}** | **{n(rg['TOTAL primer año, Ruta B'][2])}** |
| Años siguientes, Ruta A (sin guía) | {n(rg['TOTAL años siguientes, Ruta A (sin guía)'][0])} | {n(rg['TOTAL años siguientes, Ruta A (sin guía)'][1])} | {n(rg['TOTAL años siguientes, Ruta A (sin guía)'][2])} |

La Ruta A equivale a cerca del {rg['Ruta A como % del costo de la Fase 1 de idiomas'][1]*100:.0f}% del costo anual de la Fase 1 de idiomas, de modo que es del mismo orden que traducir a inglés y portugués. La recomendación es la Ruta A con revisión pastoral siempre humana, porque la herramienta acelera el borrador pero no decide qué es pastoralmente adecuado. Los otros tres perfiles repiten este costo, y los de preadolescentes y niños necesitan más reescritura todavía, porque pierden la exégesis y cambian de narración.

## Qué se factura realmente en voz

El costo de las tablas es de consumo. La facturación real de ElevenLabs es por plan, y se paga el plan completo aunque no se agote. Con las cifras prudentes del modelo (Creator 100.000 créditos por 22 USD, Pro 500.000 por 99 USD, Scale 1,8 millones por 299 USD):

| Fase | Créditos al mes que necesita Jóvenes (medio) | Plan mínimo | Pago anual del plan |
|---|---|---|---|
| 1 · 3 idiomas | {n(cr[0])} | {plan[0]} | unos 1.090 EUR |
| 2 · 8 idiomas | {n(cr[1])} | {plan[1]} | unos 3.300 EUR |
| 3 · 17 idiomas | {n(cr[2])} | {plan[2]} (dos en el escenario alto) | unos 3.300 EUR, o 6.600 en el alto |

Si la misma cuenta atiende también al podcast diario «Dios Primero» y a los otros perfiles, el consumo se suma y el plan mínimo sube. Con modelos Flash el consumo se reduce a la mitad, a costa de algo de calidad en el matiz pastoral.

## Dos formas de poner la voz

- **Voz por idioma de biblioteca.** Es el enfoque de los mockups actuales (Harold en español, James en inglés y Marcos en portugués). No requiere clonación ni consentimientos nuevos, y la calidad nativa es alta. Pierde la identidad de los fundadores en cada idioma.
- **Voces clonadas de Harold y Yina hablando otros idiomas.** Conserva la identidad y el vínculo, pero exige consentimiento documentado de ambos, una escucha nativa más exigente para detectar acento extranjero, y verificar que el plan contratado incluya la clonación profesional. Es el enfoque más caro en QA y el más valioso para marca.

La recomendación es empezar con voces de biblioteca en inglés y portugués, mantener las voces de Harold y Yina en español, y evaluar la clonación multilingüe con una prueba de dos días de inglés antes de decidir.

## Supuestos y confianza

| Supuesto | Bajo, medio, alto | Confianza |
|---|---|---|
| Precio de voz por 1.000 caracteres | 0,08, 0,17 y 0,22 USD | Media. Derivado de los planes; las fuentes de terceros discrepan y la página oficial no era accesible desde esta sesión |
| Regeneración por errores de pronunciación | 1,2, 1,5 y 2,0 | Baja. Los nombres bíblicos y las palabras originales obligan a repetir |
| DeepL por millón de caracteres | 25, 25 y 27,5 USD más cuota fija | Media. Hay fuentes que indican que las suscripciones nuevas pasan a un plan distinto |
| Revisión nativa y teológica por 1.000 palabras | 15, 30 y 50 EUR | Baja. Pedir cotización a dos revisores por idioma |
| QA de audio por idioma y mes | 30, 60 y 120 EUR | Baja |
| Canción e instrumental por mes | 0, 30 y 150 EUR | Baja |
| Borrador con IA y control de registro, por 1.000 palabras | 8, 15 y 30 EUR | Baja |
| Reescritura humana completa, por 1.000 palabras | 40, 70 y 120 EUR | Baja |
| Guía de registro y glosario, una vez | 600, 1.200 y 2.400 EUR | Baja |
| Panel de lectores jóvenes, por trimestre | 150, 300 y 600 EUR | Baja |

Para afinar el modelo, cambiar las celdas amarillas de la hoja «Supuestos». Todo lo demás se recalcula.

## Lo que no está en el modelo y puede pesar más que la voz

- **Licencia de las Escrituras.** El texto de cada día lleva un versículo de RVR1960. Reproducirlo en pantalla, y sobre todo leerlo en audio dentro de un producto de pago, requiere el permiso del titular de los derechos de esa versión, y cada idioma necesita su propia versión con su propia licencia. Una nota del propio proyecto indica que la NVI tiene tramos por usuarios activos desde 10 USD al mes a través de API.Bible, mientras que RVR1960 exige un trámite más estricto. Este costo está sin cotizar y puede condicionar qué versiones se leen en audio.
- **Revisión teológica de los días sensibles.** Los días 9, 10 y 12 requieren pastoral además de lingüística en cada idioma.
- **Derechos de la música.** Si la canción y el instrumental usan música generada o de biblioteca, hay que confirmar los términos de uso comercial.
- **Impuestos y comisiones de tienda.** No están considerados, y las tiendas de aplicaciones retienen una parte de las suscripciones.
- **Consentimiento de voz.** Hace falta un consentimiento firmado por cada persona clonada y una política de uso, sobre todo si se publica en otros países.

## Cómo reducir el costo sin perder calidad

1. Pasar por revisión humana completa solo el español, el inglés y el portugués, y por muestreo del 20% los idiomas de la Fase 3 hasta tener métricas de calidad.
2. Compartir la canción y el instrumental entre idiomas, como ya prevé el diseño de tres canales, de modo que solo la capa de voz es específica por idioma.
3. Traducir una sola vez cada día con DeepL y revisar las diferencias contra un glosario fijo de términos (Emanuel, Eben-ezer, Yeshua, *proskynēsai*), para que la revisión se concentre en lo pastoral y no en corregir nombres.
4. Generar el audio solo después de aprobar el texto, porque cada repetición por un cambio tardío consume créditos y horas de QA.
"""
(A / "costos.md").write_text(md, encoding="utf-8")
print("costos.md escrito", len(md), "caracteres")
