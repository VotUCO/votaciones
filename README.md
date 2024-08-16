# Sistema de Votaciones

Este proyecto es un sistema de votaciones que utiliza Django, MongoDB Y PostgreSQL.

## Descripción

El Sistema de Votaciones es una aplicación web que permite a los usuarios participar en Procesos electorales con distintos sistemas de votación (Scoring, Schuzle y Mayoritario). Utiliza una arquitectura de microservicios con diferentes bases de datos para manejar distintos aspectos del sistema.

## Tecnologías utilizadas

- Django: Framework web de Python
- MongoDB: Base de datos NoSQL para almacenar cuestionarios
- PostgreSQL: Base de datos relacional para el sistema principal
- Docker: Para la contenerización de la aplicación

## Requisitos previos

- Docker
- Docker Compose

## Configuración y ejecución

1. Clona este repositorio:
   ```
   git clone https://github.com/votuco/votaciones.git
   cd votaciones
   ```

2. Construye e inicia los contenedores:
   ```
   docker-compose build
   docker-compose up
   ```

3. La aplicación se desplegará en `http://localhost:8000`

## Estructura del proyecto

- `deploy/`: Contiene archivos de configuración para Docker
- `src/`: Código fuente de la aplicación Django
    - `src/users/`: Código fuente de la aplicación de usuarios
    - `src/voting/`: Código fuente de la aplicación de votaciones
    - `src/vote/`: Código fuente de la aplicación de votos
    - `src/shared/`: Código fuente de la aplicación de common
- `docker-compose.yaml`: Configuración de los servicios Docker

## Servicios

- Web: Aplicación Django
- MongoDB: Base de datos para cuestionarios
- PostgreSQL: Base de datos principal

## Desarrollo

Para desarrollar en este proyecto:

1. Asegúrate de tener Docker instalados.
2. Realiza los cambios en el código fuente.
3. Reconstruye los contenedores si has hecho cambios en el Dockerfile:
   ```
   docker-compose build
   ```
4. Inicia los servicios:
   ```
   docker-compose up
   ```

## Pruebas

Para ejecutar las pruebas:
```
python3 manage.py test
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios propuestos antes de hacer un pull request.

## Licencia

Mozilla Public License 2.0