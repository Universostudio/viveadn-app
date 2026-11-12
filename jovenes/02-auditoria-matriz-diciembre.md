# Auditoría de la matriz de Diciembre 2026 (Adultos 30+)

Fuente auditada: `VMAD_Diciembre_2026_v2.docx` (31 días, volumen 12 de 12). Reglas de referencia: Brief Editorial y Producción v1 (mayo 2026) y Guía Estructural de Producción 2027 a 2029. El extractor está en `contenido/fuente/extraer_adultos.py` y los datos extraídos en `contenido/fuente/dic2026_adultos_extraido.json`, de modo que cada cifra de este documento se puede reproducir.

La matriz tiene una base teológica sólida: los términos hebreos y griegos están bien elegidos y bien integrados, no hay voseo, no aparece «cotidiano» ni una sola vez, y la progresión del mes (naturaleza de la esperanza, esperanza en la oscuridad, esperanza encarnada, umbral del año) es coherente. Los problemas están en la ejecución del formato y en las reglas que el propio proyecto se dio, y conviene corregirlos en Adultos antes de seguir adaptando, porque los otros tres perfiles heredan la matriz.

## Hallazgos

| # | Gravedad | Hallazgo | Evidencia | Corrección propuesta |
|---|---|---|---|---|
| 1 | Alta | Los días 27 y 31 tienen los campos desplazados | En el día 27, la «Oración del día» contiene la frase del fruto, la «Frase del día» contiene una referencia (Lucas 2:28-35) y el plan de lectura apunta a Filipenses 4:7 y Juan 14:27. En el día 31, la oración contiene un resumen del año, el fruto es la cita «Salmo 1:1-6» y el campo de capítulo lleva las lecturas complementarias. | Reconstruir ambos días. En la edición Jóvenes ya están reconstruidos, con el plan de lectura corregido. |
| 2 | Alta | La dimensión rota casi nunca | 30 de 31 días son «Personal» y solo el día 7 es «Social». No hay ningún día «Familiar» ni «Relacional». | Aplicar la rotación Personal, Relacional, Social sin repetir dos días seguidos (regla del Brief). Jóvenes queda en 12, 9 y 9. |
| 3 | Alta | Frases del fruto fuera de la regla de 100 a 150 caracteres | 14 de 29 válidas superan 150 (hasta 209) y 2 no llegan a 100 (90 y 74). Con los dos días corruptos, 18 de 31 incumplen. | Reescribir a 100 a 150 caracteres. Jóvenes ya lo cumple en los 30 días. |
| 4 | Media | Los frutos no están en primera persona | 0 de 29 contienen marcas de primera persona, y la Guía de Producción pide «primera persona declarativa». | Redactar en primera persona, que además funciona mejor al compartir en redes. |
| 5 | Media | La reflexión (TALLO) queda por debajo del mínimo | Media de 188 palabras (de 159 a 211). El Brief pide 250 a 350 y la Guía 250 a 320. Ninguno de los 31 llega a 250. | Decidir si se amplía Adultos o si se corrige la regla (ver decisiones abiertas). |
| 6 | Media | Dos fórmulas dominan los retos y las preguntas | 18 de 31 retos empiezan por «Escribe hoy» y 6 por «Evalúa hoy», es decir, 77% con dos aperturas. 23 de 31 preguntas empiezan por «¿Ha» o «¿La». La pregunta promedia 37 palabras con estructura compuesta, lejos de «una sola pregunta» directa. | Variar los verbos de apertura y acortar las preguntas. En Jóvenes «Escribe» baja a 5 de 30 y «¿Qué» a 4 de 30. |
| 7 | Media | Versículo del día 25 no es cita exacta | La matriz cita Lucas 2:21 pero el texto combina Mateo 1:25 y Lucas 2:7. | Usar el texto exacto de Lucas 2:21 en RVR1960. Aplicado en Jóvenes y marcado para verificar contra la edición impresa. |
| 8 | Media | Dos días dependen de meses anteriores | El día 3 abre con «Noviembre trabajó el ancla» y el día 7 con «Septiembre trabajó este versículo». | Hacer cada día autónomo, porque el podcast, la app y los lectores nuevos de 2027 consumen el día suelto. Jóvenes no presupone meses previos. |
| 9 | Media | Plan de lectura con formato incoherente | El día 25 pone dos referencias en «Capítulo del día», y el día 31 pone dos lecturas complementarias como capítulo. | Un capítulo y dos complementarias en todos los días. |
| 10 | Baja | Rayas largas en el interior, contra la regla de marca | 4 apariciones: línea de portada, «2027 — El Árbol en Comunidad», «Simeón — El Relato» y el título del relato final. | Sustituir por dos puntos o coma. |
| 11 | Baja | Erratas | «consueloque» (día 13) y «vino a inaugura» (día 22). | Corregir en la fuente. |

## Contradicciones entre los documentos maestros

Estas diferencias no son errores del contenido sino decisiones pendientes del equipo editorial, y condicionan toda la versión para jóvenes.

| Tema | Brief Editorial (mayo 2026) | Guía 2027 a 2029 |
|---|---|---|
| Edad del perfil joven | Jóvenes 14 a 18 años, formato A5+ | Jóvenes adultos 18 a 30 y Pre jóvenes 13 a 17 |
| Elementos del día | Siete, pero la lista numera dos veces el «6» y cuenta la invitación al libro | Siete: Raíz, Tallo, Hoja, Testimonio, Oración, Fruto y Plan |
| Orden de oración y frase | La lista pone la frase antes de la oración, y el texto dice lo contrario | Oración antes del fruto |
| Dimensiones | Personal, relacional, social, sin repetir días consecutivos | Personal, familiar, social, rotación por semana (S1 personal, S2 familiar, S3 social, S4 personal) |
| Longitud del TALLO | 250 a 350 palabras en general | 250 a 320 adultos, 200 a 280 jóvenes adultos, 150 a 220 pre jóvenes |
| Persona del fruto | No la fija | Primera persona declarativa |
| Paleta | Verde `#1E3A2A`, dorado `#B8924D`, crema `#F5F0E1` | Colores por mes. Los mockups de app usan `#2E7D32`, `#D4AA3A` y `#F8F4EE`, y el CRM ViveADN usa `#00523C`, `#F5A623` y `#F4F0E6` |
| Versión bíblica | Reina-Valera 1960 como única versión citada | La app muestra siete versiones |

## Lo que sí funciona y se conserva

El versículo, la referencia, el plan de lectura, el narrador Simeón, el título de cada día y la exégesis de fondo pasan sin cambio a la edición Jóvenes, tal como pide la Guía en su sección «Lo que NO cambia entre perfiles». Las únicas excepciones están marcadas con una nota editorial en cada día afectado (días 25, 27 y 30).
