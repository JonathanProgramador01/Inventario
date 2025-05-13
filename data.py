'''
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│  ALMACENES  │     │   PRODUCTOS   │     │  CATEGORÍAS  │
├─────────────┤     ├───────────────┤     ├──────────────┤
│ PK id       │     │ PK sku        │     │ PK id        │
│   nombre    │     │   nombre      │     │   nombre     │
│   ubicacion │     │ FK categoria  │     │   descripcion│
│   capacidad │     │   unidad_med  │     └──────────────┘
│   encargado │     │   stock_min   │             ▲
│   telefono  │     │   stock_max   │             │
└─────────────┘     │   precio      │             │
        ▲           └───────────────┘             │
        │                    ▲                   │
        │                    │                   │
        │                    │                   │
┌───────────────────┐  ┌─────────────────────┐  │
│ INVENTARIO_ALMACEN│  │    MOVIMIENTOS      │  │
├───────────────────┤  ├─────────────────────┤  │
│ PK id             │  │ PK id               │  │
│ FK almacen_id     │  │   tipo (ent/sal)    │  │
│ FK producto_sku   │  │   fecha             │  │
│   cantidad        │  │ FK almacen_id       │  │
│   lote (opcional) │  │   proveedor/cliente │  │
│   fecha_venc (op) │  │   referencia        │  │
└───────────────────┘  │   responsable       │  │
        ▲              └─────────────────────┘  │
        │                     ▲                 │
        │                     │                 │
        │                     │                 │
┌──────────────────────┐ ┌───────────────────────┐
│ DETALLE_MOVIMIENTOS  │ │   HISTORICO_INVENTARIO│
├──────────────────────┤ ├───────────────────────┤
│ PK id                │ │ PK id                 │
│ FK movimiento_id     │ │ FK producto_sku       │
│ FK producto_sku      │ │   fecha               │
│   cantidad           │ │   cantidad_anterior   │
│   precio_unitario    │ │   cantidad_actual     │
└──────────────────────┘ │   tipo_movimiento     │
                         │   referencia_mov      │
                         └───────────────────────┘
'''



almacenes = [
    {
        "id": 1,
        "nombre": "Almacén Central CDMX",
        "ubicacion": "Ciudad de México",
        "capacidad": "10,000 m²",
        "encargado": "Ing. Laura Méndez",
        "telefono": "55-1234-5678"
    },
    {
        "id": 2,
        "nombre": "Almacén Norte MTY",
        "ubicacion": "Monterrey",
        "capacidad": "7,500 m²",
        "encargado": "Lic. Carlos Rodríguez",
        "telefono": "81-2345-6789"
    },
    {
        "id": 3,
        "nombre": "Almacén Pacífico GDL",
        "ubicacion": "Guadalajara",
        "capacidad": "6,000 m²",
        "encargado": "Ing. Sofía Navarro",
        "telefono": "33-3456-7890"
    }
]

categorias = [
    {"id": 1, "nombre": "Electrónicos", "descripcion": "Dispositivos electrónicos y componentes"},
    {"id": 2, "nombre": "Muebles", "descripcion": "Mobiliario para oficina y hogar"},
    {"id": 3, "nombre": "Suministros", "descripcion": "Materiales de oficina y limpieza"},
    {"id": 4, "nombre": "Equipo Industrial", "descripcion": "Maquinaria y herramientas pesadas"}
]

productos = [
    {
        "sku": "ELEC-1001",
        "nombre": "Laptop Empresarial",
        "categoria": "Electrónicos",
        "unidad_medida": "pieza",
        "stock_minimo": 50,
        "stock_maximo": 200,
        "precio": 18999.00,
        "ubicaciones": [
            {"almacen": "Almacén Central CDMX", "cantidad": 120},
            {"almacen": "Almacén Norte MTY", "cantidad": 75}
        ]
    },
    {
        "sku": "MUEB-2005",
        "nombre": "Silla Ejecutiva",
        "categoria": "Muebles",
        "unidad_medida": "pieza",
        "stock_minimo": 30,
        "stock_maximo": 150,
        "precio": 4299.00,
        "ubicaciones": [
            {"almacen": "Almacén Central CDMX", "cantidad": 85},
            {"almacen": "Almacén Pacífico GDL", "cantidad": 60}
        ]
    },
    {
        "sku": "SUMI-3010",
        "nombre": "Paquete de Papel A4",
        "categoria": "Suministros",
        "unidad_medida": "paquete (500 hojas)",
        "stock_minimo": 100,
        "stock_maximo": 500,
        "precio": 249.00,
        "ubicaciones": [
            {"almacen": "Almacén Central CDMX", "cantidad": 320},
            {"almacen": "Almacén Norte MTY", "cantidad": 180},
            {"almacen": "Almacén Pacífico GDL", "cantidad": 210}
        ]
    }
]

movimientos = [
    {
        "id": 1001,
        "tipo": "entrada",
        "fecha": "2023-05-15",
        "almacen": "Almacén Central CDMX",
        "proveedor": "TecnoSuministros SA",
        "referencia": "OC-2023-0512",
        "items": [
            {"sku": "ELEC-1001", "cantidad": 50, "precio_unitario": 17500.00},
            {"sku": "SUMI-3010", "cantidad": 100, "precio_unitario": 230.00}
        ],
        "responsable": "Juan Pérez"
    },
    {
        "id": 1002,
        "tipo": "salida",
        "fecha": "2023-05-16",
        "almacen": "Almacén Norte MTY",
        "cliente": "Corporación Industrial Norte",
        "referencia": "FV-2023-2105",
        "items": [
            {"sku": "MUEB-2005", "cantidad": 25, "precio_unitario": 4299.00},
            {"sku": "ELEC-1001", "cantidad": 15, "precio_unitario": 18999.00}
        ],
        "responsable": "María González"
    }
]

reportes = {
    "inventario_actual": {
        "fecha_generacion": "2023-05-20",
        "total_productos": 3,
        "valor_total": 3845720.00,
        "detalle_almacenes": [
            {
                "almacen": "Almacén Central CDMX",
                "valor": 2568900.00,
                "productos": 3
            },
            {
                "almacen": "Almacén Norte MTY",
                "valor": 824400.00,
                "productos": 2
            },
            {
                "almacen": "Almacén Pacífico GDL",
                "valor": 452420.00,
                "productos": 2
            }
        ]
    },
    "movimientos_mensuales": {
        "mes": "Mayo 2023",
        "total_entradas": 1,
        "total_salidas": 1,
        "valor_entradas": 905000.00,
        "valor_salidas": 334860.00
    }
}

alertas = [
    {
        "tipo": "stock_minimo",
        "producto": "SUMI-3010",
        "almacen": "Almacén Norte MTY",
        "cantidad_actual": 85,
        "cantidad_minima": 100,
        "fecha_alerta": "2023-05-18"
    },
    {
        "tipo": "vencimiento",
        "producto": "MED-4002",
        "lote": "LT-2023-04",
        "fecha_vencimiento": "2023-06-15",
        "dias_restantes": 26,
        "cantidad": 120
    }
]