# Evaluación y costo de voces e idiomas · Jóvenes

Modelo en `costos.xlsx` (celdas amarillas editables, fórmulas vivas) y regenerable con `build_costos.py`, que recalcula el libro con LibreOffice y falla si alguna fórmula devuelve error. Los volúmenes salen del contenido real de la edición, y los precios son supuestos con su nivel de confianza escrito junto a cada uno.

## Conclusión

Producir audio y traducción con herramientas automáticas cuesta muy poco. Lo que cuesta es que una persona de cada idioma revise el texto con ojo pastoral y escuche el audio. En escenario medio, la voz y la traducción automática suman menos del 6% del costo anual de la Fase 1, y la revisión humana más el control de calidad del audio suman cerca del 90%. Si se quiere crecer a 17 idiomas, el presupuesto se decide casi por completo en la contratación de revisores, no en la suscripción de voz.

## Volumen real (30 días de Jóvenes)

| Concepto | Valor |
|---|---|
| Caracteres narrados | 54.625 (media de 1.821 por día, unos 2 minutos de audio) |
| Caracteres a traducir | 57.229 |
| Palabras a revisar | 10.226 |
| Escala a un año (365 días) | 664.000 caracteres narrados y 124.000 palabras por idioma |

## Costo anual por fase, en euros

Cada fase incluye los idiomas de la anterior. Fase 1: español, inglés y portugués, que es lo que ya prevé la hoja de ruta de 2027. Fase 2: francés, italiano, alemán, rumano y polaco. Fase 3: nueve idiomas más hasta 17 (ruso, ucraniano, hindi, árabe, coreano, chino, japonés, indonesio y filipino). La lista de 17 es una propuesta de trabajo, porque los documentos del proyecto hablan de 17 idiomas sin nombrarlos.

| Línea (escenario medio) | Fase 1 · 3 idiomas | Fase 2 · 8 idiomas | Fase 3 · 17 idiomas |
|---|---|---|---|
| Voz (ElevenLabs) | 468 | 1.247 | 2.651 |
| Traducción automática (DeepL) | 93 | 173 | 317 |
| Revisión nativa y teológica | 7.465 | 26.127 | 69.798 |
| QA de audio (escucha nativa) | 2.160 | 5.760 | 12.240 |
| Canción e instrumental | 360 | 360 | 360 |
| Almacenamiento y entrega | 0 | 1 | 2 |
| **Total anual, medio** | **10.546** | **33.668** | **85.367** |
| Rango bajo a alto | 5.082 a 19.763 | 16.587 a 59.502 | 42.335 a 147.827 |
| Revisión humana sobre el total | 71% | 78% | 82% |

Esto cubre solo el perfil Jóvenes. Los otros tres perfiles tienen volúmenes de texto parecidos o menores, así que el costo de revisión crece de forma casi lineal con cada perfil y cada idioma.

## Qué se factura realmente en voz

El costo de la tabla es de consumo. La facturación real de ElevenLabs es por plan, y se paga el plan completo aunque no se agote. Con las cifras prudentes del modelo (Creator 100.000 créditos por 22 USD, Pro 500.000 por 99 USD, Scale 1,8 millones por 299 USD):

| Fase | Créditos al mes que necesita Jóvenes (medio) | Plan mínimo | Pago anual del plan |
|---|---|---|---|
| 1 · 3 idiomas | 245.812 | Pro | unos 1.090 EUR |
| 2 · 8 idiomas | 655.500 | Scale | unos 3.300 EUR |
| 3 · 17 idiomas | 1.392.938 | Scale (dos en el escenario alto) | unos 3.300 EUR, o 6.600 en el alto |

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

Para afinar el modelo, cambiar las celdas amarillas de la hoja «Supuestos». Todo lo demás se recalcula.

## Lo que no está en el modelo y puede pesar más que la voz

- **Licencia de las Escrituras.** El texto de cada día lleva un versículo de RVR1960. Reproducirlo en pantalla, y sobre todo leerlo en audio dentro de un producto de pago, requiere el permiso del titular de los derechos de esa versión, y cada idioma necesita su propia versión con su propia licencia. Una nota del propio proyecto indica que la NVI tiene tramos por usuarios activos desde 10 USD al mes a través de API.Bible, mientras que RVR1960 exige un trámite más estricto. Este costo está sin cotizar y puede condicionar qué versiones se leen en audio.
- **Revisión teológica de los días sensibles.** Los días 9, 10 y 12 requieren pastoral además de lingüística en cada idioma.
- **Derechos de la música.** Si la canción y el instrumental usan música generada o de biblioteca, hay que confirmar los términos de uso comercial.
- **Impuestos y comisiones de tienda.** No están considerados, y las tiendas de aplicaciones retienen una parte de las suscripciones.
- **Soporte a la clonación de voz.** Hacen falta un consentimiento firmado por cada persona clonada y una política de uso, sobre todo si se publica en otros países.

## Cómo reducir el costo sin perder calidad

1. Pasar por revisión humana completa solo el español, el inglés y el portugués, y por muestreo del 20% los idiomas de la Fase 3 hasta tener métricas de calidad. Con esa medida la revisión de los 14 idiomas adicionales bajaría de forma proporcional.
2. Compartir la canción y el instrumental entre idiomas, como ya prevé el diseño de tres canales, de modo que solo la capa de voz es específica por idioma.
3. Traducir una sola vez cada día con DeepL y revisar las diferencias contra un glosario fijo de términos (Emanuel, Eben-ezer, Yeshua, *proskynēsai*), para que la revisión se concentre en lo pastoral y no en corregir nombres.
4. Generar el audio solo después de aprobar el texto, porque cada repetición por un cambio tardío consume créditos y horas de QA.
