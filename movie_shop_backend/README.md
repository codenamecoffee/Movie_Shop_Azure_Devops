# 🧪 School Of Software Engineering : FastAPI Development

## 👩‍💻👨‍💻🤝 Equipo

Mariana Guerra (marianaguerra965) and Federico González (fglmr95)

## 🎯 Objetivo

El propósito de esta práctica es que pasen por la experiencia de programar una API Rest utilizando FastAPI con Python. Nos basaremos solamente en el desarrollo de las rutas y los schemas definidos y comentados en clase.

## 🧩 Actividades a realizar

Dada la siguiente realidad:

*Una persona quiere retornar a lo Vintage y por esto decidió crear una franquicia de VideoClubs, en donde espera almacenar información de las diferentes Shops y Movies de cada shop. Para esto, precisa de un grupo de desarrolladores que implementen la API Rest asociada a esta necesidad.*

*Se deben utilizar las siguientes estructuras:*

```python
Movie:
  id: Number
  name: String
  director: String
  gender: List[String]
  shop: Number
  rent: Boolean
```

```python
Shop:
  id: Number
  address: String
  manager: String
  movies: List[Movie]
```

*La persona espera que **al crear un Shop, no se tengan Movie asociadas**, por lo tanto, deben crearse primero las Shop y luego las Movie, que al ser creadas, sean asociadas a esta. Tampoco quiere usar **la edición del Shop para editar cada lista de Movie, sino que las Movie sean agregadas una vez que se haga una creación al id de Shop asignado**.*

*A su vez, **las Movie no pueden editar atributos de shop o de rent cuando se use la edición de Movie**. El alquiler y el pasaje de una Movie entre Shop debe realizarse en endpoints diferentes.*

*Por último, tener en cuenta que cuando **se elimina un Shop, se deben eliminar todas las Movie que estaban en la estructura general (`movies` dentro de `routes/api_routes.py`)** y al **eliminar una Movie, debe eliminarse dentro de la lista de Shop en la que estaba agregada**.*


### 📝 Entregable

Es esperable que el código sea subido en un repositorio a partir de un **fork** de este proyecto en una branch llamada `develop` que posteriormente se cree un Pull Request para agregar los cambios de la misma en `main`. Se espera que este trabajo sea realizado para el **viernes 15/08**.

---------------------------

## 🗂️ Estructura del proyecto

Este proyecto fue creado usando UV. Se compone de los siguientes directorios:

```bash
database_manager
|__init__.py
|_ local_file_storage.py
routes
|__init__.py
|_ api_routes.py
schemas
|__init__.py
|_ schemas.py
constants.py
main_base.py
pyproject.toml
README.md
```

Dentro de `database_manager` se encuentra el código necesario para gestionar el uso de nuestra base de datos en un archivo JSON. Dicho archivo tendrá el nombre de la variable `STATE_FILE` en el archivo de constantes `constants.py`.
Dentro del directorio `schemas` se tendrá el archivo `schemas.py` en el cual se definirá todos los esquemas necesarios para desarrollar la API Rest.
En la carpeta `routes` se tendrá el archivo `api_routes.py` donde se implementarán las rutas de la API a desarrollar.
Por último, el código con las rutas de la API se encuentra en `main_base.py`.

## 🏗️ Uso del proyecto

### 🧰 Utilizando UV

Como hemos venido trabajando durante el curso vamos a utilizar UV para la creación del ambiente virtual. Para esto procedemos a ejecutar los siguientes pasos:

Inicialización del environment

```bash
uv sync
```
## 🚀 Uso del servicio

Una vez instaladas las dependencias, se inicia el servicio utilizando el siguiente comando:

```bash
# Linux
uv run fastapi dev src/main.py

# Windows
uv run fastapi dev .\src\main.py
```

Una vez inicializado el servicio se puede utilizar el mismo a través de la siguiente url en el navegador: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) o ingresar a la documentación de Swagger del mismo mediante [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

