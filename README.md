# School Of Software Engineering : FastAPI Development

## Estructura del proyecto

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

## Creación del ambiente virtual

### Utilizando UV

Como hemos venido trabajando durante el curso vamos a utilizar UV para la creación del ambiente virtual. Para esto procedemos a ejecutar los siguientes pasos:

Inicialización del environment

```bash
uv sync
```
## Uso del servicio

Una vez instaladas las dependencias, se inicial el servicio utilizando el siguiente comando:

```bash
# Linux
uv run fastapi dev src/main.py

# Windows
uv run fastapi dev .\src\main.py
```

Una vez inicializado el servicio se puede utilizar el mismo a traves de la siguiente url en el navegador: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) o ingresar a la documentación de Swagger del mismo mediante [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Bonus track

### Generar archivo requirements.txt con UV

Se puede ejecutar el siguiente comando para generar un archivo de `requirements.txt` utilizando UV:

```bash
uv pip freeze > requirements.txt
```