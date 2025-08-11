# 🧪 School Of Software Engineering Hands-On: Desarrollo de API Rest con Python + FastAPI

## 🎯 Objetivo

El propósito de este hands-on es que desarrollen una API Rest utilizando la base del proyecto Python brindada. Dicha base cuenta con UV preconfigurado y el framework FastAPI instalado.

## 🧩 Actividades a realizar

- Realizar un fork y descargar el repositorio base (la nueva rama tiene que tener la nomeclatura `iniciales-estudiante1_iniciales-estudiante-2_movie_shop`).
- Completen el archivo [api_routes.py](src/routes/api_routes.py) con el código necesario
- Utilizar Swagger para corroborar que el código funciona.
- Subir los cambios en el repositorio realizado a partir del fork en una nueva rama llamada `develop`.

## 📦 Entregables

Se espera que el cambio sea subido como **fecha límite el 15/08**. Deberán crear un Pull Request hacia la branch `main`para que le demos un feedback del código. Una vez aprobado el Pull Request, sus cambios pasarán a la branch de `main`.
 

## 🗂️ Estructura del proyecto

Este proyecto fue creado usando UV. Se compone de los siguientes directorios:

```bash
database_manager
|_ local_file_storage.py
schemas
|_ schemas.py
constants.py
main_base.py
pyproject.toml
README.md
```

Dentro de `database_manager` se encuentra el código necesario para gestionar el uso de nuestra base de datos en un archivo JSON. Dicho archivo tendrá el nombre de la variable `STATE_FILE` en el archivo de constantes `constants.py`.
Dentro del directorio `schemas` se tendrá el archivo `schemas.py` en el cual se definirá todos los esquemas necesarios para desarrollar la API Rest.
Por último, el código con las rutas de la API se encuentra en `main_base.py`.

## 🏗️ Creación del ambiente virtual

### 🧰 Utilizando UV

Como hemos venido trabajando durante el curso vamos a utilizar UV para la creación del ambiente virtual. Para esto procedemos a ejecutar los siguientes pasos:

Inicialización del environment

```bash
uv sync
```
## 🚀 Uso del servicio

Una vez instaladas las dependencias, se inicial el servicio utilizando el siguiente comando:

```bash
# Linux
uv run fastapi dev src/main.py

# Windows
uv run fastapi dev .\src\main.py
```

Una vez inicializado el servicio se puede utilizar el mismo a traves de la siguiente url en el navegador: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) o ingresar a la documentación de Swagger del mismo mediante [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
