FROM python:3.12-slim

# Establecer directorio de trabajo:
WORKDIR /app 

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc build-essential curl ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Instalar uv y agregarlo al PATH
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && ln -s $HOME/.local/bin/uv /usr/local/bin/uv

# Copiar archivos de dependencias
COPY movie_shop_backend/pyproject.toml .
COPY movie_shop_backend/uv.lock .

# Instalar dependencias usando uv
RUN uv sync --frozen --no-dev

# Copiar el código fuente
COPY movie_shop_backend/src ./src

# Crear volumen para datos persistentes
VOLUME ["/app/movie_shop_data"]

# Configurar variables de entorno
ENV STATE_FILE=/app/movie_shop_data/app_state.json
ENV PYTHONUNBUFFERED=1
ENV UV_CACHE_DIR=/app/.uv-cache

# Exponer puerto
EXPOSE 8000

# Comando para iniciar la API
CMD ["uv", "run", "--with", "uvicorn", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]