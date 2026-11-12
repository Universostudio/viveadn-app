# Guía de registro juvenil (14 años en adelante)

Esta guía responde a una pregunta concreta: si la redacción de Adultos sirve tal cual para un lector joven, y si no, qué cambia y cómo se controla en los 365 días del libro. Las reglas de abajo no son opinión: las comprueba `build.py` en cada compilación y fallan o avisan con el día y la frase exacta.

## Diagnóstico con datos

Se midió la matriz de Adultos de diciembre y la edición Jóvenes con la misma función (`registro.py`): índice Fernández-Huerta, que es la adaptación de Flesch al español, y longitud de frase.

| Medida del TALLO | Adultos (matriz) | Jóvenes, primer borrador | Jóvenes, versión final |
|---|---|---|---|
| Fernández-Huerta medio (más alto es más fácil) | 70 | 78 | 80 |
| Fernández-Huerta del día más difícil | 59 | 68 | 71 |
| Palabras por frase | 17,2 | 17,7 | 15,9 |
| Frases de más de 32 palabras | 30 | 0 | 0 |
| Frase más larga | 69 palabras | 30 | 28 |
| Palabras de 4 o más sílabas | 12% | 6,5% | menos de 7% |

La conclusión es que el vocabulario de la edición Jóvenes ya era más sencillo desde el primer borrador, pero las frases eran largas, y eso fue lo que se corrigió. La longitud pesa más que las palabras por dos razones. En pantalla, una frase de 40 palabras obliga a releer. En audio, que es el formato principal del módulo, el oyente no puede volver atrás, así que una frase larga se pierde.

## Qué cambia respecto a Adultos y qué no

Cambia la longitud de la frase, la cantidad de términos abstractos por párrafo y el territorio de los ejemplos. No cambia la teología, el versículo, los conectores ni la voz pastoral directa: el lector joven no necesita un lenguaje infantil, necesita frases que se puedan seguir de una vez.

Este equilibrio resuelve una tensión que conviene nombrar. La preferencia de prosa del equipo editorial pide párrafos amplios y cohesionados, con conectores variados y sin telegrafismo. Esa preferencia se mantiene entera: lo que cambia es que cada idea larga se reparte en dos o tres frases enlazadas por los mismos conectores (porque, pero, así, de modo que, aunque, por eso, y aun así), en lugar de acumularse en una sola frase subordinada.

## Reglas medibles

Las comprueba `build.py`. Los umbrales están en las constantes de su cabecera.

| Regla | Umbral | Efecto |
|---|---|---|
| Ninguna frase del TALLO, la HOJA o el TESTIMONIO supera 32 palabras | 32 | Fallo, la compilación se detiene |
| Aviso desde 28 palabras por frase | 28 | Aviso con la frase citada |
| Fernández-Huerta del TALLO por día | al menos 70 | Aviso |
| Palabras por frase del TALLO, por día | hasta 18 | Aviso |
| Palabras por frase del TALLO, promedio del mes | hasta 16,5 | Aviso |
| El TESTIMONIO es una sola pregunta | exacta | Fallo |
| Ninguna pausa de audio supera 3 segundos y las pausas del día no pasan de 12 | 3 s y 12 s | Fallo |
| El testimonio se anuncia en el audio y nunca espera la respuesta del oyente | siempre | Fallo |

## Vocabulario

La regla es conservar las palabras de la Escritura y explicar la primera vez que aparecen, no sustituirlas. Las palabras de la reflexión que no vienen del texto bíblico se sustituyen por la forma más común.

| Se evita o se explica | Se usa |
|---|---|
| *tribulación* (palabra del versículo) | se conserva y se explica: «una dificultad enorme» |
| *mansedumbre* y *reverencia* (palabras del versículo) | se conservan y se explican: «firmeza sin dureza y respeto» |
| *trascendente*, *imprescindible* | importante, necesario |
| *incoherente* | no tiene sentido |
| *resignación*, *resignaciones* | rendirse, desánimos |
| *anestesiar* | apagar el dolor |
| *linchamiento digital* | cuando un grupo se ensaña con alguien en redes |
| *imperativo*, *participio* (jerga gramatical) | la orden, la palabra |
| *normalizado*, *autosuficiente*, *improvisada*, *verificable* | acostumbrado, poder con todo yo solo, hecha a última hora, real |

La palabra hebrea o griega no se pierde: sigue en el texto en cursiva y además se ofrece como «palabra original» tocable en la interfaz, con su sentido en una línea.

## Cómo se aplica a los 365 días

1. Se redacta el mes en un archivo de texto con campos fijos, como `texto_01_10.txt`.
2. `build.py` valida las reglas de marca, el registro y el audio, y falla con la lista exacta de problemas.
3. Se corrige hasta tener cero fallos y cero avisos.
4. Un panel de lectores de 14 a 18 años lee una muestra cada trimestre y responde una prueba breve de comprensión. Las métricas dicen si una frase se puede seguir, pero solo un lector real dice si resulta cercana o forzada.
5. La revisión pastoral de Harold y Yina siempre es humana y llega después del control automático, para que su tiempo se dedique a lo pastoral y no a contar palabras.

El costo de este trabajo para el libro completo está en `../costos/costos.md`, sección «Adaptar el lenguaje de todo el libro».

## Límites de las métricas

El índice Fernández-Huerta mide sílabas y longitud de frase, no ideas. Un texto puede obtener buena puntuación y ser abstracto, y otro puede obtener una puntuación baja y ser claro. Por eso las métricas actúan como alarma y no como criterio de calidad, y el criterio final es la prueba con lectores.
