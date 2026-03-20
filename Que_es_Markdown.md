# ¿Qué es Markdown (y Markup)?

En programación y redacción de documentos técnicos, es muy común escuchar los términos **Markup** y **Markdown**. A continuación, te explicamos la diferencia y por qué **Markdown** será tu mejor amigo a la hora de tomar apuntes en las celdas de texto de tus Jupyter Notebooks a lo largo de este curso.

## 1. El concepto: Lenguajes de Marcado (Markup Languages)

Un **Lenguaje de Marcado (Markup Language)** es un sistema que utiliza etiquetas o símbolos especiales para indicarle al computador **cómo** debe mostrar u organizar un texto. A diferencia de un procesador de texto como Word (donde usas botones visuales), aquí usas "códigos" para indicar qué va en negrita, qué es un título o dónde va una imagen. 

El lenguaje de marcado más famoso del mundo es **HTML** (HyperText Markup Language), que se utiliza para construir todas las páginas web de internet. Sin embargo, HTML utiliza etiquetas largas como `<b>texto</b>` o `<h1>título</h1>` que pueden ser tediosas de escribir a mano para tomar apuntes rápidos.

## 2. ¿Qué es Markdown?

**Markdown** es una versión extremadamente simplificada, ligera e intuitiva de un lenguaje de marcado. Su objetivo principal es que sea muy fácil escribir y leer texto formateado usando caracteres comunes del teclado.

Con Markdown puedes dar formato a tus textos de manera ultrarrápida. Por ejemplo:

* Si escribes `**Hola Mundo**`, se transformará visualmente en **Hola Mundo** (negrita).
* Si escribes `# Mi Título`, se transformará en un **Título grande**.
* Si escribes `- Item 1`, se transformará en un punto de viñeta.

## 3. ¿Por qué lo usamos en el curso?

1. **En los Jupyter Notebooks:** Como vimos en la guía anterior, los *Jupyter Notebooks* tienen "Celdas de Texto". **Estas celdas utilizan Markdown** para darles diseño. Si aprendes Markdown, podrás escribir ecuaciones, hacer títulos estructurales, crear listas de estudio fáciles de leer y hacer tus apuntes mucho más prolijos.
2. **En Plataformas de desarrollo:** GitHub, Discord, Slack, Reddit y casi todas las herramientas modernas de desarrollo utilizan Markdown. (¡Incluso este mismo documento que estás leyendo ahora está escrito íntegramente en Markdown!).
3. **Productividad y rapidez:** No necesitas sacar las manos del teclado para usar el ratón y hacer clic en un botón de "Negrita" o "Cursiva". Todo el formato se hace escribiendo los símbolos directamente.

## 4. Guía ultrarrápida de Markdown

Aquí tienes una "hoja de trucos" (*cheat sheet*) con las etiquetas más usadas que te servirán para tus clases:

| ¿Qué quieres lograr? | ¿Cómo se escribe el código Markdown? | ¿Cómo se ve al ejecutar/renderizar? |
| :--- | :--- | :--- |
| **Negrita** | `**Texto importante**` | **Texto importante** |
| *Cursiva* | `*Texto inclinado*` | *Texto inclinado* |
| Título Principal | `# Titulo 1` | Un título muy grande |
| Subtítulo | `## Titulo 2` | Un título mediano |
| Lista o viñetas | `- Primer elemento` <br> `- Segundo elemento` | • Primer elemento <br> • Segundo elemento |
| Lista numerada | `1. Paso uno` <br> `2. Paso dos` | 1. Paso uno <br> 2. Paso dos |
| Código en línea | Usa comillas invertidas: \`print(Hola)\` | `print(Hola)` |
| Enlace web | `[Universidad](https://utalca.cl)` | [Universidad](https://utalca.cl) |

---

> [!TIP]
> **Para practicar en tu computador:**  
> Cuando abras tu primer Jupyter Notebook y crees una **Celda de Texto** (Celda tipo "Markdown"), intenta escribir algunos de los ejemplos de la tabla derecha y luego "ejecuta" la celda (`Shift + Enter`) para ver la magia de cómo el texto cambia su diseño automáticamente.
