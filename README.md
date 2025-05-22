# 🚚 Sistema de Control de Inventario para Logística

![Dashboard Preview](https://i.imgur.com/JK4mW7d.png)
*Captura del panel principal del sistema*

## 📌 Descripción

Sistema interno de control de inventario para gestión de almacenes distribuidos en múltiples ciudades, desarrollado para una empresa de logística. Incluye módulos completos para:

- Gestión de entradas/salidas de mercancía
- Control de existencias en tiempo real
- Generación de reportes mensuales
- Solicitudes y aprobaciones de materiales

## ✨ Características Principales

| Módulo | Funcionalidades | Icono |
|--------|----------------|-------|
| **Almacenes** | Gestión multi-ciudad, ubicaciones físicas | 🏭 |
| **Productos** | Categorización, unidades de medida | 📦 |
| **Inventario** | Existencias en tiempo real, alertas | 📊 |
| **Solicitudes** | Flujo de aprobación (miembros → veteranos/admin) | 📋 |

![Flujo de Solicitudes](https://i.imgur.com/8mXwvQk.png)
*Diagrama del proceso de solicitudes*

## 🛠 Tecnologías Utilizadas

**Backend:**
- Python 3.10
- Flask
- SQLAlchemy (PostgreSQL)
- Redis (para cache)

**Frontend:**
- HTML5/CSS3 (Flexbox/Grid)
- JavaScript (Vanilla)
- Bootstrap 5
- Font Awesome Icons

**Infraestructura:**
- Docker
- Nginx
- AWS EC2 (para despliegue)

## 🚀 Instalación

1. Clonar repositorio:
```bash
git clone https://github.com/tu-usuario/sistema-inventario-logistica.git
cd sistema-inventario-logistica
