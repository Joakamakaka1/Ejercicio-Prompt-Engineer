# Ejercicio 2 — Análisis de reseñas de videojuegos con LLMs (Groq)

Pipeline de **dos pasos con LLMs** que, a partir de `videogames_reviews.csv`:

1. **Filtra** las reseñas relevantes (descarta spam / texto sin contenido).
2. **Extrae información estructurada** (sentimiento, aspectos, dificultad, etc.)
   de las reseñas relevantes.

Se usa la **API de Groq** (cloud) con **dos modelos distintos** —uno por tarea—,
**batching** de varias reseñas por llamada y **gestión de rate limits**. Todo el
razonamiento de Prompt Engineering está explicado dentro de `analisis_videojuegos.ipynb`.

## Requisitos

- **Python 3.11–3.13** y **[uv](https://docs.astral.sh/uv/)**.
- Una **API key gratuita de Groq**: https://console.groq.com → *API Keys*.

## Instalación

```bash
# 1. Instalar dependencias y crear el entorno (.venv) con uv
uv sync

# 2. Configurar la API key
cp .env.example .env          # Windows: copy .env.example .env
# edita .env y pon tu GROQ_API_KEY=gsk_...

# 3. (Opcional) registrar el kernel de Jupyter
uv run python -m ipykernel install --user --name pontia-videojuegos \
    --display-name "Pontia Videojuegos (uv)"
```

## Ejecución

**Opción A — Jupyter Lab**

```bash
uv run jupyter lab
```

Abre `analisis_videojuegos.ipynb`, comprueba que el kernel seleccionado es
**"Pontia Videojuegos (uv)"** y ejecuta **Kernel → Restart & Run All**.

**Opción B — VS Code**

Abre `analisis_videojuegos.ipynb`, arriba a la derecha selecciona el kernel
**"Pontia Videojuegos (uv)"** y pulsa **Run All**.

En ambos casos, al terminar se genera `output/analisis_videojuegos_resultados.csv`.

## Contenido

| Archivo | Descripción |
| --- | --- |
| `analisis_videojuegos.ipynb` | Notebook con todo el pipeline y las justificaciones. |
| `data/videogames_reviews.csv` | Dataset de entrada (20 000 reseñas). |
| `pyproject.toml` / `uv.lock` | Dependencias del proyecto (uv). |
| `output/…resultados.csv` | Salida estructurada (se genera al ejecutar; no versionada). |
| `PLAN.md` | Plan de trabajo del ejercicio. |
