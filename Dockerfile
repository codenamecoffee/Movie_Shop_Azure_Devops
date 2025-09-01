# Usar imagen base de Python (No importa sino tengo esa versión instalada localmente.)
# -slim es una versión más liviana de python:

FROM python:3.12-slim

# Establecer directorio de trabajo:
WORKDIR /app 

# Instalar dependencias del sistema (le copio al profe):
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential curl ca-certificates \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && rm -rf /var/lib/apt/lists/*

# Usar curl -LsSf para no usar pip para instalar uv. (No queremos usar pip).

# Copiamos los archivos
COPY movie_shop_backend/pyproject.toml .
COPY movie_shop_backend/uv.lock .

# Agregamos los nuevos directorios a la variable de entorno path: (prevenir errores)
ENV PATH="/root/.cargo/bin:/root/.local/bin:${PATH}"

# Usar uv para installar dependencias:
RUN uv sync --frozen

# Copiamos los datos del proyecto:
COPY movie_shop_backend/src ./src
COPY movie_shop_backend/app_state.json .

# Crear directorio para datos persistentes:
RUN mkdir -p data

# Mover archivos de estado al directorio de datos:
RUN mv app_state.json data/

# Configurar variable de entorno en el contenedor:
# (La api del contenedor, utilizará esta variable)
ENV STATE_FILE=/app/data/app_state.json

# Declaramos el punto de montaje: (Carpeta en común entre el contenedor y el host)
# Permite que app_state.json persista fuera del contenedor.
VOLUME ["/app/data"] 

# Configurar el puerto y comando
EXPOSE 8000

# (Uvicorn da problemas - porque no está en el pyproyect.toml original)
# CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Solución: UV instala 'uvicorn' en un entorno temporal:
CMD ["uv", "run", "--with", "uvicorn", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

