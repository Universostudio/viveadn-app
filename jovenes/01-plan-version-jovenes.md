# Plan y ejecución · Versión Jóvenes de 30 días (14 años en adelante)

Punto de partida: los 31 días de Diciembre 2026 de la edición Adultos (`Esperanza Eterna · Adviento · El árbol que aguarda`). Resultado: una edición de 30 días con contenido final, una interfaz con las cuatro temporadas verificada en contraste, un prototipo navegable y un modelo de costos de voces e idiomas. Todo se puede regenerar con los scripts incluidos, de modo que el mismo procedimiento sirve para los doce meses de 2027.

## Qué se entrega

| Pieza | Archivo | Estado |
|---|---|---|
| Contenido de 30 días | `contenido/dic2026_jovenes.json` y `.md` | Redactado y validado: 0 fallos y 0 avisos |
| Texto fuente editable | `contenido/texto_01_10.txt`, `texto_11_20.txt`, `texto_21_30.txt` | Fuente de verdad para ajustes de Harold y Yina |
| Constructor y validador | `contenido/build.py` | Falla si algún día rompe una regla VMAD |
| Auditoría de la matriz | `02-auditoria-matriz-diciembre.md` | 11 hallazgos con evidencia |
| Tokens de las 4 temporadas | `interfaz/tokens-estaciones.json`, `jovenes-estaciones.css`, `contraste.md` | 2 marcos x 12 meses x 2 modos, 0 fallos de contraste |
| Prototipo navegable | `interfaz/preview-jovenes.html` | Con los 30 días reales. Se abre en cualquier navegador |
| Momentos de interfaz | `interfaz/momentos-interfaz.md` | 10 momentos más reglas para menores |
| Costos | `costos/costos.xlsx` y `costos.md` | Modelo con supuestos editables, recalculado sin errores |

## Cómo se adaptó cada día

Se conserva lo que la Guía declara intocable entre perfiles: el versículo de RVR1960, la referencia, el plan de lectura, el título, el narrador Simeón y la exégesis de fondo. Se reescribe lo que la Guía y el Brief asignan al perfil: el registro de la reflexión, el territorio de aplicación del reto y de la pregunta, la oración y la frase del fruto.

| Elemento | Adultos (matriz) | Jóvenes 14+ |
|---|---|---|
| Raíz | Versículo RVR1960 | Idéntico |
| Tallo | Tres párrafos, media de 188 palabras, exégesis integrada | Tres párrafos, media de 182 palabras, con ejemplos del entorno juvenil (chats, redes, exámenes, cena de Navidad). La exégesis queda en la prosa solo cuando cambia el sentido y el término se ofrece además como «palabra original» tocable |
| Hoja | Casi siempre «Personal» y casi siempre «Escribe hoy» | Un solo reto concreto, con verbo y objeto, en la dimensión que rota (12 personales, 9 relacionales, 9 sociales) |
| Testimonio | Pregunta de 37 palabras de media | Una sola pregunta de unas 20 palabras, en la misma dimensión que el reto |
| Oración | Tercera persona implícita, tono adulto | Primera persona, tres movimientos (gratitud, confesión, petición), cierre «En el nombre de Jesús, amén» |
| Fruto | 100 a 209 caracteres, tercera persona | 100 a 130 caracteres, primera persona, con un «porque» teológico, legible fuera de contexto |
| Plan de lectura | Con errores en los días 25, 27 y 31 | Un capítulo y dos complementarias, corregido |

Las reglas de marca se cumplen y se comprueban por código: sin rayas largas ni guiones parentéticos, sin «cotidiano», sin voseo y sin autorreferencia al devocional. Los nombres divinos van en versalitas en el cuerpo del texto, y el prototipo ya aplica esa convención.

## Decisiones tomadas

1. **Edad.** Se escribió para 14 años en adelante, que es el perfil «Jóvenes 14 a 18» del Brief y coincide con la edad de consentimiento digital en España. La Guía propone en cambio 18 a 30 y 13 a 17, así que conviene fijar una sola definición antes de producir 2027.
2. **Treinta días.** Diciembre tiene 31. Se fusionaron el 30 y el 31 de la matriz en un último día que conserva el versículo del 31 (Salmo 1:3, el versículo ancla de la obra) y absorbe la gratitud de 1 Pedro 1:3 en la reflexión y en el plan de lectura. El 31 de diciembre queda libre para el momento de cierre del año en la interfaz.
3. **Dimensión.** Se rota por versículo y nunca se repite en días consecutivos, siguiendo el Brief. La rotación semanal de la Guía produciría tres días seguidos de la misma dimensión y chocaría con esa regla.
4. **Longitud de la reflexión.** Entre 165 y 230 palabras. Es la banda de 13 a 17 de la Guía (150 a 220) ampliada un poco hacia la banda de 18 a 30 (200 a 280), porque el perfil cubre las dos. Es una decisión de criterio, no una medida de calidad.
5. **Cuatro temporadas.** Se interpretaron como los cuatro trimestres del año, que la Guía ya define con enfoque teológico propio. Los nombres Brote, Savia, Cosecha y Aguardo son de trabajo y evitan el calendario del hemisferio norte, porque la audiencia incluye España y Latinoamérica.
6. **Dos marcos de marca.** El proyecto tiene dos paletas distintas (VMAD y ViveADN). La interfaz se resuelve con una base neutra por marco y los colores mensuales como identidad del contenido, de modo que cambiar de marco es una línea.

## Decisiones abiertas (con propuesta)

| # | Pregunta | Propuesta |
|---|---|---|
| 1 | ¿Qué edad define el perfil joven? | 14 a 18 como perfil propio, y 18 a 30 como cuarta edición futura |
| 2 | ¿Se corrige Adultos con los hallazgos 1 a 11? | Sí, antes de adaptar 2027. Los frutos deben ser idénticos entre perfiles, así que los frutos nuevos de Jóvenes deberían subir a la matriz de Adultos |
| 3 | ¿Qué marco gobierna la interfaz dentro de la app? | Si el módulo devocional vive dentro del CRM ViveADN, el marco ViveADN. Si es una app propia, el marco VMAD |
| 4 | ¿Qué color tiene Diciembre 2026? | La Guía publica la paleta de 2027, no la de 2026. El prototipo usa Diciembre de 2027 (verde pino `#0F3A1A`) hasta que diseño confirme |
| 5 | ¿Cómo se licencia el audio del versículo? | Pendiente. Leer en voz alta RVR1960 en un producto comercial requiere permiso de su titular. Ver `costos/costos.md` |
| 6 | ¿Se publica un piloto en diciembre de 2026? | Faltan menos de tres semanas para el 1 de diciembre. Es viable solo en español, con revisión pastoral y voz ES, sin inglés ni portugués |

## Cómo escalar a los 365 días

El procedimiento es el mismo que se usó aquí y no depende de esta sesión: la matriz de Adultos del mes se extrae a JSON, se redactan los días del perfil en un archivo de texto con campos fijos, `build.py` fusiona los metadatos y valida las reglas, y el resultado alimenta la maquetación, la app, el audio y el modelo de costos. Para un mes de 30 días la redacción es el único trabajo creativo, y el validador evita que se acumulen los defectos que la auditoría encontró en Adultos (frutos largos, dimensiones repetidas, campos movidos).

Dos advertencias de calendario. El Brief fija una antelación objetivo de tres meses por mes publicado, y la matriz de Adultos 2027 todavía está pendiente de redactarse, por lo que Jóvenes de enero de 2027 no puede adelantarse a ella. Y la edición de diciembre sirve como piloto para calibrar el flujo completo antes de comprometer el año.

## Riesgos principales

- La revisión humana por idioma domina el costo (más del 70% del total anual en todas las fases). Ver `costos/costos.md`.
- Los precios de ElevenLabs y DeepL provienen de fuentes de terceros que discrepan entre sí, porque las páginas oficiales no eran accesibles desde esta sesión. Hay que confirmarlos antes de contratar.
- El audio de las Escrituras y las versiones bíblicas por idioma son un requisito legal, no solo de producción.
- Los días de lamento y sufrimiento (9, 10 y 12) tratan temas delicados para un lector de 14 años. Llevan una tarjeta de cuidado en la interfaz y deben pasar por revisión pastoral antes de publicarse.
