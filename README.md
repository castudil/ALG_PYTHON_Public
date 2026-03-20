# Bienvenidos a ALG_PYTHON_Public

Este repositorio contiene todo el material teórico, laboratorios y ejercicios para el curso. A continuación encontrarás las instrucciones para acceder a todo el material y mantenerlo sincronizado en tu computador durante el semestre.

> [!NOTE]
> **¿Eres nuevo(a) en el mundo de la programación y no sabes qué es GitHub?**  
> Hemos preparado una guía introductoria rápida para ti. Revisa nuestro documento sobre **[¿Qué es GitHub y por qué lo usamos?](Que_es_GitHub.md)** antes de seguir con las instrucciones.

## Guía técnica: Cómo acceder al material del curso en tu entorno local

### Requisitos previos
* Tener instalado **Git** en tu equipo ([Descargar Git aquí](https://git-scm.com/downloads)).
* Tener un entorno de desarrollo para Python (te recomendamos [Visual Studio Code](https://code.visualstudio.com/) o [Jupyter Lab](https://jupyter.org/install)).

### Paso 1: Clonar el repositorio por primera vez

La clonación solo se realiza **una sola vez**. Esto descargará una copia exacta de todos los archivos del curso en tu computador.

1. Abre tu terminal (Símbolo del sistema o PowerShell en Windows; Terminal en macOS/Linux).
2. Navega hasta la carpeta en la que deseas guardar los archivos del curso. Por ejemplo:
   ```bash
   cd Documentos/Mi_Carpeta_De_Clases
   ```
3. Ejecuta el siguiente comando para clonar el repositorio:
   ```bash
   git clone https://github.com/castudil/ALG_PYTHON_Public.git
   ```
4. Ingresa a la carpeta recién creada:
   ```bash
   cd ALG_PYTHON_Public
   ```

### Paso 2: Mantener el repositorio actualizado

A medida que avancen las clases, el profesor subirá nuevos materiales y laboratorios a este repositorio. Para descargar las últimas actualizaciones en tu computador, **NO** es necesario volver a clonarlo.

1. Abre la terminal y asegúrate de estar dentro de la carpeta del repositorio (`ALG_PYTHON_Public`).
2. Ejecuta el siguiente comando:
   ```bash
   git pull
   ```

Este comando descargará e integrará automáticamente los nuevos archivos creados por el profesor en tu computador.

> **💡 Recomendación:** Ejecuta `git pull` al inicio de cada clase o sesión de estudio para asegurarte de tener siempre la versión más reciente del material sin sobrescribir tus propios archivos.
