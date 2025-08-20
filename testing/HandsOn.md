# 🧪 Hands-On: Automatización de Testing para APIs

## 🎯 Objetivo

El propósito de esta práctica es que desarrollen pruebas automatizadas para la API que construyeron junto a Nico. Esto implica no solo escribir código de testing, sino también comprender y planificar qué aspectos de la API serán probados, y cómo.

## 🧩 Actividades a realizar

### 📝 Planificación de pruebas

- Crear un **Test Plan** en Azure DevOps.  
- Documentar **casos de prueba** que verifiquen el funcionamiento de los endpoints de la API.  
- Determinar cuáles de estos casos pueden ser **automatizados**.

### 🤖 Automatización

- Implementar una **suite de tests automatizados** en Python utilizando `pytest`, `requests`, u otras librerías pertinentes.  
- Cubrir los siguientes verbos HTTP:
  - `GET`
  - `POST`
  - `PUT`
  - `DELETE`
- Asegurarse de probar tanto **respuestas exitosas** como **errores esperados**.

### 🔀 Repositorio

- Crear una rama llamada `testing` en su repositorio de Azure DevOps.  
- Realizar **commits frecuentes** a medida que implementan los cambios a dicha rama.  
- El día **jueves 21 de agosto** será la **fecha límite** para realizar modificaciones en dicha rama y generar un **Pull Request (PR)** hacia `main`.

## 📦 Entregables

Antes de la fecha límite, deberán subir a la rama `testing`:

- Una **captura de pantalla** de los test cases definidos en Azure DevOps.
- El proyecto de pruebas **completo y funcional**, con todos los tests ejecutables.
- Un **reporte HTML** de ejecución de pruebas.
- El **PR creado hacia `main`**.