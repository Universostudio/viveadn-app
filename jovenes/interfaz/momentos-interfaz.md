# Interfaz Jóvenes · cuatro temporadas y momentos de interacción

El prototipo `preview-jovenes.html` implementa todo lo descrito aquí con el contenido real de los 30 días. Se abre con doble clic y permite cambiar temporada, color del mes, día, modo claro u oscuro y marco de marca. También acepta parámetros en la dirección, por ejemplo `?marco=viveadn&tema=oscuro&mes=dic&dia=24`.

## Las cuatro temporadas

Cada temporada es un trimestre con el enfoque que le asigna la Guía de Producción. La interfaz cambia de color cada mes, y la temporada aporta el ícono y el nombre. Los nombres son de trabajo.

| Temporada | Meses | Enfoque del trimestre | Ícono | Acento de los meses (paleta El Bosque 2027) |
|---|---|---|---|---|
| Brote | Enero a marzo | Fundamentos e identidad | Brote | `#1A3B2A`, `#2A3A4A`, `#4A6B4A` |
| Savia | Abril a junio | Vida sobrenatural y autoridad | Gota | `#7A3A2A`, `#C4622D`, `#A07030` |
| Cosecha | Julio a septiembre | Don, llamado y testimonio | Fruto | `#1A4A3A`, `#5A3A2A`, `#C9963A` |
| Aguardo | Octubre a diciembre | Perseverancia, mayordomía y esperanza | Luna | `#5C1A2A`, `#6A2A5A`, `#0F3A1A` |

La paleta mensual cambia cada año (2027 El Bosque, 2028 La Cosecha, 2029 La Lluvia), así que `tokens.py` la recibe como parámetro y regenera todo. Para 2028 y 2029 basta con añadir la lista de doce colores que ya publica la Guía.

## Tokens y contraste

`tokens.py` genera una variable CSS por token, mes, modo y marco, y comprueba el contraste de cada par en cada combinación. El resultado completo está en `contraste.md` y no tiene fallos: 2 marcos por 12 meses por 2 modos.

Reglas que salen de esa comprobación y que el diseño debe respetar:

- Un color de mes no se usa directamente como texto. Se usa `--j-acento-texto`, que es el color del mes oscurecido en claro hasta 4,5:1 y aclarado en oscuro hasta 7:1. Con 4,5:1 los meses oscuros, como diciembre, se veían apagados sobre fondo oscuro.
- Los botones llevan `--j-boton-bg` y `--j-boton-texto`. En meses claros como septiembre (`#C9963A`) el botón se oscurece hasta cumplir 4,5:1 con texto blanco, y no se pinta con el color crudo.
- La cabecera del día usa un degradado del color del mes hacia un tono 28% más oscuro, con texto blanco. Cumple 4,5:1 en ambos extremos.
- Dos colores heredados de los mockups no pasan como texto o elemento gráfico: el verde `#4CAF50` queda en 2,6:1 sobre `#F0F8F2`, y el oro `#D4AA3A` en 2,2:1 sobre blanco. Se mantienen como decoración y relleno de progreso. El oro de interfaz se ajusta por marco y modo hasta 3:1.

## Diez momentos de interfaz

1. **Apertura del día.** La cabecera toma el color del mes, muestra la temporada, la dimensión del día y una ruta de 30 puntos. El día actual lleva el punto dorado. No existe «racha» que se pierda: la ruta solo avanza.
2. **Raíz con audio.** El versículo se escucha con un toque y puede abrirse en otras versiones sin salir del día. Las versiones disponibles dependen de la licencia de cada una (ver costos).
3. **Palabra original.** El término hebreo o griego aparece en cursiva dentro de la reflexión y como botón. Al tocarlo se abre una hoja inferior con su sentido y su pronunciación. Es el modo de resolver la tensión entre profundidad y lectura ágil: la exégesis está disponible para quien la pida, pero no interrumpe a quien no.
4. **Reto con recordatorio.** Una sola acción, con casilla «Hecho» y un recordatorio opcional a la hora que el lector elija. La dimensión (personal, relacional, social) se muestra con ícono.
5. **Pregunta anunciada.** La pregunta del testimonio se lee en el audio y se muestra en pantalla, pero el día no se detiene a esperar la respuesta: tras leerla suena un puente instrumental de pocos segundos y el audio pasa a la oración. La respuesta escrita pertenece al libro, que tiene una página con espacio para escribirla, así que la app no compite con el libro. «Llevarla conmigo» deja la pregunta a mano en «Para pensar hoy». No hay cuadro de texto dentro del flujo del día.
6. **Audio continuo en tres canales.** Voz, instrumental o canción, como en el audio interactivo ya diseñado. El audio avanza del título al fruto sin esperas: las pausas duran entre medio segundo y 2,5 segundos y las controla `build.py`, que falla si alguna deja al oyente esperando. «Amén» es opcional. El día se completa cuando termina el audio o cuando el lector llega al fruto.
7. **Fruto compartible.** La frase del día se presenta como tarjeta vertical con el color del mes, lista para historias, con marca discreta y sin rastreo. Un segundo botón permite enviarla a un amigo concreto, que es la forma relacional de compartir.
8. **Plan de lectura.** Las tres referencias abren la Biblia integrada en el pasaje exacto.
9. **Momento de cuidado.** Un botón de corazón siempre visible abre «Necesito hablar con alguien». En los días 9, 10 y 12, que tratan el lamento y el sufrimiento, aparece además una tarjeta suave al final del día. En España ofrece el 024. Para otros países la app debe mostrar la línea local y esa lista está pendiente de verificar antes de publicar.
10. **Cierre del día y del año.** El árbol crece al completarse el día, la ruta marca el día y se propone volver mañana a la hora elegida, sin culpa si no ocurre. El 31 de diciembre se reserva para la pantalla de celebración «Día Final» que ya existe en los mockups, con el resumen del árbol del año. El reto del día 30 (carta de gratitud) puede enlazarse con una cápsula del tiempo que se devuelve el 30 de diciembre del año siguiente.

## Principio de continuidad: el día no espera

Según lo que describió Harold, el guion de audio de una versión anterior dejaba una pausa de espera tras la pregunta, del tipo «cuando hayas terminado, te espero». Ese guion no estaba en el repositorio, así que esta sección se apoya en esa descripción. Esa pausa interrumpe la continuidad por tres razones que se ven en el diseño. Quien escucha en el trayecto o con las manos ocupadas no puede escribir, y un silencio largo suena a audio roto. La pregunta del testimonio ya tiene su lugar natural en el libro, donde hay tiempo y papel, y duplicarla dentro de la app pone a ambos a competir. Y una espera sin límite convierte cada día en un punto donde se puede abandonar.

Por eso la pregunta se anuncia y se sigue: se lee con claridad, suena un puente instrumental de unos dos segundos y continúa la oración. El audio no tiene ningún punto de espera, y `build.py` lo garantiza: ningún segmento puede pausar más de 3 segundos, las pausas del día no pueden sumar más de 12 y el testimonio debe estar marcado como anunciado.

Esto encaja con la invitación diaria al libro que el Brief ya prevé como séptimo elemento: la pregunta puede cerrar con «tiene su página en el libro», de modo que cada día refuerza la compra en lugar de competir con ella. Queda una decisión abierta para quien no tiene el libro, y la propuesta es no ofrecer cuaderno digital en el lanzamiento y mantener solo «Llevarla conmigo». Que esto mejore la finalización del día es una hipótesis razonable y todavía no está medida: conviene comparar con una prueba A/B la proporción de lectores que llegan al fruto con y sin la pausa.

## Reglas específicas para menores

- **Sin diario dentro de la app.** Lo que el joven escribe vive en el libro. Si más adelante se añade un cuaderno digital, será local y privado, y el adulto del plan familiar verá cumplimiento, nunca contenido.
- **Sin presión de racha.** Los avisos de «tu racha está en riesgo» pueden producir ansiedad en adolescentes. La ruta de 30 días conserva todo lo avanzado y las notificaciones son invitaciones, no advertencias.
- **Sin publicidad ni rastreo en el perfil joven.** Coincide con la promesa «sin publicidad nunca» del plan de precios.
- **Edad de consentimiento.** En España la edad de consentimiento digital es 14 años (LOPDGDD, artículo 7), y el RGPD permite fijarla entre 13 y 16 según el país. Un perfil «14 en adelante» encaja en España, pero para cada país de destino debe validarse con asesoría legal, y esta nota no sustituye ese análisis.
- **Seguridad del contenido.** Los días 9, 10 y 12 deben pasar por revisión pastoral antes de publicarse, y la guía de cuidado debe estar disponible desde cualquier pantalla.

## Accesibilidad

- Todos los pares de color cumplen WCAG 2.2 AA, y el texto de acento en oscuro llega a 7:1.
- La lectura del TALLO usa 17 píxeles con interlineado de 1,7 en Georgia, y la interfaz usa DM Sans, como en los mockups.
- Los controles tienen nombre accesible, foco visible de 3 píxeles y objetivo táctil de al menos 36 píxeles.
- Se respeta `prefers-reduced-motion`: el crecimiento del árbol se vuelve instantáneo.
- Pendiente: tamaño de texto ajustable por el lector y descarga offline del audio del mes. Treinta días de narración pesan unos 57 MB por voz y por idioma.

## Para pasar a Flutter

`tokens-estaciones.json` está pensado para alimentar una extensión de tema por marco, modo y mes, de modo que el color del mes se resuelve por fecha y no está escrito en cada pantalla. Los nombres de los tokens CSS (`--j-acento`, `--j-hero-desde`, etc.) se corresponden uno a uno con las claves del JSON.
