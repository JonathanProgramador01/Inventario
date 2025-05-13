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


'''

/* INSERT INTO user (usuario, contraseña, rol)
VALUES ('Jonathan', '1234', 'admin');

INSERT INTO user (usuario, contraseña, rol)
VALUES ('Pepe', '1234', 'miembro');

INSERT INTO user (usuario, contraseña, rol)
VALUES ('Axel', '1234', 'veterano'); */

-- Usuarios
INSERT INTO user (usuario, contraseña, rol) VALUES
('admin', 'admin123', 'admin'),
('jperez', 'contra123', 'veterano'),
('mgarcia', 'password', 'miembro'),
('lrodriguez', 'seguro456', 'veterano'),
('amartinez', 'acceso789', 'miembro');

-- Almacenes
INSERT INTO almacen (nombre, ciudad, direccion) VALUES
('Almacén Central', 'Ciudad de México', 'Av. Principal 123, Col. Centro'),
('Almacén Norte', 'Monterrey', 'Calle Industria 456, Parque Industrial'),
('Almacén Pacífico', 'Guadalajara', 'Blvd. Tecnológico 789, Zona Industrial'),
('Almacén Sur', 'Puebla', 'Calle Comercio 321, Distrito Comercial');

-- Productos
INSERT INTO producto (nombre, descripcion, unidad) VALUES
('Laptop Empresarial', 'Laptop i7 16GB RAM 512GB SSD', 'pieza'),
('Monitor 24"', 'Monitor Full HD LED 24 pulgadas', 'pieza'),
('Teclado Inalámbrico', 'Teclado ergonómico inalámbrico', 'pieza'),
('Mouse Óptico', 'Mouse con cable 1600DPI', 'pieza'),
('Tóner Impresora', 'Tóner para impresora modelo LX-200', 'pieza'),
('Silla Ejecutiva', 'Silla ergonómica para oficina', 'pieza'),
('Paquete de Papel', 'Resma de papel bond tamaño carta', 'paquete'),
('Escritorio Oficina', 'Escritorio de madera 1.60m', 'pieza');

-- Existencias (inventario actual)
INSERT INTO existencia (producto_id, almacen_id, cantidad_actual) VALUES
(1, 1, 15), (1, 2, 8), (1, 3, 5),
(2, 1, 20), (2, 2, 12), (2, 3, 7), (2, 4, 10),
(3, 1, 35), (3, 3, 18),
(4, 2, 50), (4, 4, 30),
(5, 1, 25), (5, 2, 15), (5, 3, 10),
(6, 1, 8), (6, 4, 5),
(7, 1, 120), (7, 2, 80), (7, 3, 60), (7, 4, 90),
(8, 2, 6), (8, 3, 4);

-- Entradas (movimientos de entrada)
INSERT INTO entrada (producto_id, almacen_id, cantidad, fecha) VALUES
(1, 1, 10, '2023-05-01 09:00:00'),
(2, 1, 15, '2023-05-02 10:30:00'),
(3, 3, 20, '2023-05-03 11:15:00'),
(4, 2, 30, '2023-05-04 14:00:00'),
(5, 1, 15, '2023-05-05 16:45:00'),
(6, 4, 5, '2023-05-08 10:00:00'),
(7, 2, 50, '2023-05-09 11:30:00'),
(8, 3, 4, '2023-05-10 13:15:00');

-- Salidas (movimientos de salida)
INSERT INTO salida (producto_id, almacen_id, cantidad, fecha) VALUES
(1, 1, 2, '2023-05-06 10:00:00'),
(1, 2, 1, '2023-05-06 11:30:00'),
(2, 1, 3, '2023-05-07 09:45:00'),
(2, 3, 2, '2023-05-07 14:15:00'),
(3, 1, 5, '2023-05-08 16:00:00'),
(4, 2, 8, '2023-05-09 10:30:00'),
(5, 1, 3, '2023-05-10 12:00:00'),
(7, 3, 15, '2023-05-11 15:45:00');
'''

