# S15 · Unidad 4 — Árboles balanceados

**Posición en el programa:** semana 15. Cátedra y laboratorio.

## Material

| Archivo | Tipo | Sesión |
|---------|------|--------|
| `S15_ALG_TEO_Arboles_Balanceados.ipynb` | Cátedra (90 min) | Árboles 2-3 y rojo-negro |
| `S15_ALG_LAB_Arboles_Balanceados.ipynb` | Laboratorio (100 min) | Rotaciones e invariantes |
| `S15_ALG_SOL_Arboles_Balanceados.ipynb` | Solución del laboratorio | *(no se publica)* |

## Cátedra — Árboles 2-3 y árboles rojo-negro

- Degeneración del BST ante inserciones ordenadas como motivación: de O(log n) a O(n).
- Árboles 2-3: nodos de 2 y 3 claves, inserción por división ascendente, altura garantizada.
- Árboles rojo-negro como representación binaria de un árbol 2-3 (variante *left-leaning*).
- Rotaciones y recoloreo: el mecanismo, con traza sobre ejemplos pequeños.
- Garantía h ≤ 2·log₂n en el peor caso. Comparación con el BST simple.

## Laboratorio — Árboles balanceados en Python

- **Bloque 1:** implementar `rotar_izquierda`, `rotar_derecha` y `cambiar_colores`, y las
  tres líneas de rebalanceo de `put`. Verificación de los tres invariantes.
- **Bloque 2:** medir la altura de BST y rojo-negro sobre las mismas claves en orden
  ordenado, inverso y aleatorio; comparar con `dict`; implementar las consultas de orden
  `rango` y `piso` — lo que una tabla hash no puede dar.
- **Entrega Tarea Unidad 4.**

**Bibliografía:** CLRS cap. 13 · GTG cap. 11.2–11.5 · Grok cap. 8

**Prerrequisito:** [`../S14_U4_BST/`](../S14_U4_BST/)
**Continúa en:** [`../S16_U4_Tablas_Hash/`](../S16_U4_Tablas_Hash/)
