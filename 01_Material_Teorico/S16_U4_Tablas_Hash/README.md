# S16 · Unidad 4 — Tablas Hash

**Posición en el programa:** semana 16. Solo cátedra — el bloque de laboratorio del viernes
es la **Prueba de Unidad 4**.

⚠️ Este tópico **no entra en la Prueba de Unidad 4**: se dicta en la misma semana en que se
rinde la prueba, así que queda fuera por el reglamento de separación. Sí entra en el
Examen Opcional Acumulativo. Hay que avisarlo a los estudiantes al comenzar la unidad.

## Material

| Archivo | Tipo | Sesión |
|---------|------|--------|
| `S16_ALG_TEO_Tablas_Hash.ipynb` | Cátedra (90 min) | Tablas hash y cierre de la Unidad 4 |

## Cátedra — Tablas Hash

- Función hash: distribución uniforme, `hash()` de Python, el problema de las colisiones
  (paradoja del cumpleaños).
- **Encadenamiento separado:** listas enlazadas por casilla, costo esperado O(1 + α).
- **Sondeo lineal:** direccionamiento abierto, agrupamiento primario, borrado con lápidas.
- Factor de carga α y redimensionamiento: por qué se duplica al llegar a α ≈ 0,5–0,75, y
  por qué eso da O(1) **amortizado**.
- Comparación final de la unidad: tabla hash vs. BST vs. árbol balanceado — cuándo conviene
  cada estructura de diccionario.

El notebook incluye implementaciones completas y ejecutables de `HashEncadenamiento` y
`HashSondeoLineal`, con instrumentación de sondeos y factor de carga.

## Trabajo autónomo (reemplaza al laboratorio)

- Ejercicios 1 y 2 del notebook, con verificador automático.
- Zona de experimentación: función hash deliberadamente mala, umbral α = 0,95, y
  acumulación de lápidas.

**Bibliografía:** CLRS cap. 11 · GTG cap. 10.2 · M&R cap. 5.5 · Grok cap. 5 · Fluent cap. 3

**Prerrequisito:** [`../S15_U4_Arboles_Balanceados/`](../S15_U4_Arboles_Balanceados/)
