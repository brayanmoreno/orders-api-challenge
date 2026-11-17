# Contrato de la API (v1)

Todas las respuestas son JSON. Los montos (`amount`) se exponen como string con dos decimales, tal como vienen de facturación.

## `GET /orders`

Lista de pedidos. **La respuesta es un arreglo JSON** (no un objeto envolvente): la app de bodega y el reporte semanal lo consumen así.

```json
[
  {"id": 15, "customer": "acme", "status": "shipped", "amount": "9.90",
   "created_at": "2026-03-12T12:25:00", "priority": 0}
]
```

Parámetros: `status` (opcional).

## `GET /orders/large?min_amount=<número>`

Pedidos con `amount >= min_amount` (comparación numérica), ordenados por `id`. Por defecto `min_amount=1000`.

## `GET /orders/{id}`

Un pedido, más `tags`: `priority` si el pedido es prioritario, `high-value` si `amount >= 1000`, y siempre su `status`. `404` si no existe.

## `GET /customers/{slug}/stats`

```json
{"customer": "umbrella", "orders": 2, "total": 1550.0, "average": 775.0}
```

Excluye pedidos `cancelled`. Un cliente sin pedidos válidos devuelve `orders: 0, total: 0, average: 0`. `404` si el cliente no existe.
