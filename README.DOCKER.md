# Docker Setup - Gas Emissions API

Esta guía explica cómo ejecutar la aplicación completa (backend y frontend) usando Docker y Docker Compose.

## Prerrequisitos

- Docker (versión 20.10 o superior)
- Docker Compose (versión 2.0 o superior)

## Estructura Docker

El proyecto incluye:

- **Backend**: Django API en Python 3.13
- **Frontend**: Angular 21 con Nginx
- **Docker Compose**: Orquesta ambos servicios

## Inicio Rápido

### 1. Construir y ejecutar todos los servicios

```bash
docker-compose up --build
```

Este comando:
- Construye las imágenes de Docker para backend y frontend
- Inicia ambos contenedores
- Configura la red entre servicios
- Ejecuta las migraciones de Django automáticamente

### 2. Acceder a la aplicación

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **API Endpoints**: http://localhost:8000/api/emissions/

### 3. Detener los servicios

```bash
docker-compose down
```

Para eliminar también los volúmenes:

```bash
docker-compose down -v
```

## Comandos Útiles

### Ver logs

```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

### Ejecutar comandos en los contenedores

```bash
# Backend - Ejecutar migraciones manualmente
docker-compose exec backend python manage.py migrate

# Backend - Crear superusuario
docker-compose exec backend python manage.py createsuperuser

# Backend - Cargar datos de prueba
docker-compose exec backend python manage.py loaddata emissions/fixtures/sample_emissions.json

# Backend - Ejecutar tests
docker-compose exec backend pytest

# Frontend - Acceder al shell
docker-compose exec frontend sh
```

### Reconstruir un servicio específico

```bash
# Reconstruir solo el backend
docker-compose build backend
docker-compose up -d backend

# Reconstruir solo el frontend
docker-compose build frontend
docker-compose up -d frontend
```

## Variables de Entorno

Las variables de entorno se pueden configurar en un archivo `.env` en la raíz del proyecto:

```env
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
```

O pasarlas directamente en `docker-compose.yml`.

## Desarrollo

### Modo Desarrollo con Hot Reload

Para desarrollo, el código del backend está montado como volumen, por lo que los cambios se reflejan automáticamente. Sin embargo, para el frontend necesitarás reconstruir la imagen después de cambios significativos.

### Base de Datos

La base de datos SQLite se persiste en `./backend/db.sqlite3` mediante un volumen de Docker.

## Producción

Para producción, considera:

1. **Eliminar el volumen de código fuente** en `docker-compose.yml` (línea comentada)
2. **Configurar variables de entorno** apropiadas
3. **Usar una base de datos externa** (PostgreSQL, MySQL) en lugar de SQLite
4. **Configurar HTTPS** con un proxy reverso (Nginx, Traefik)
5. **Optimizar las imágenes** de Docker

## Troubleshooting

### El backend no inicia

```bash
# Ver logs detallados
docker-compose logs backend

# Verificar que el puerto 8000 no esté en uso
netstat -tuln | grep 8000
```

### El frontend no se conecta al backend

Verifica que:
- Ambos contenedores estén en la misma red (`emissions-network`)
- El frontend use `http://backend:8000` para las llamadas API (no `localhost`)
- Los healthchecks estén pasando: `docker-compose ps`

### Limpiar todo y empezar de nuevo

```bash
# Detener y eliminar contenedores, redes y volúmenes
docker-compose down -v

# Eliminar imágenes
docker-compose rm -f

# Limpiar sistema Docker (cuidado: elimina todo)
docker system prune -a
```

## Arquitectura

```
┌─────────────────┐
│   Frontend      │
│   (Nginx)       │
│   Port: 4200    │
└────────┬────────┘
         │
         │ HTTP
         │
┌────────▼────────┐
│   Backend       │
│   (Django)      │
│   Port: 8000    │
└─────────────────┘
```

Ambos servicios están en la red `emissions-network` y pueden comunicarse usando los nombres de servicio (`backend`, `frontend`).
