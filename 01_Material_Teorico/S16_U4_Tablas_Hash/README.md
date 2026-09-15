# S16 · Unidad 4 — Tablas Hash

**Posición en el programa:** semana 16. Solo cátedra — el bloque de laboratorio del viernes
es la **Prueba de Unidad 4**.

⚠️ Este tópico **no entra en la Prueba de Unidad 4**: se dicta el lunes de la misma semana en
que se rinde la prueba, así que queda fuera por el reglamento de separación. Sí entra en el
Examen Opcional Acumulativo de la semana 18. Hay que avisarlo a los estudiantes al comenzar
la unidad.

**Material por generar.**

## Cátedra — Tablas Hash

- Función hash: distribución uniforme, `hash()` de Python, el problema de las colisiones.
- **Encadenamiento separado:** listas enlazadas por casilla, costo esperado O(1 + α).
- **Sondeo lineal:** direccionamiento abierto, agrupamiento primario, borrado con lápidas.
- Factor de carga α y redimensionamiento: por qué se duplica al llegar a α ≈ 0,5–0,75.
- Comparación final de la unidad: tabla hash vs. BST vs. árbol balanceado — cuándo conviene
  cada estructura de diccionario.

## Trabajo autónomo (reemplaza al laboratorio)

- Implementar ambas estrategias de resolución de colisiones.
- Medir el efecto del factor de carga sobre el número de sondeos.
- Comparar con el `dict` nativo de Python.

**Bibliografía:** CLRS cap. 11 · GTG cap. 10.2 · M&R cap. 5.5 · Grok cap. 5 · Fluent cap. 3
