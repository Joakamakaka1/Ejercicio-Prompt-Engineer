# Módulo de Prompt Engineering — Ejercicios con LLMs (Groq)

Dos ejercicios de extracción de información de texto libre con LLMs. El enunciado
completo está en [`Enunciado.md`](Enunciado.md).

| Carpeta | Ejercicio | Notebook |
| --- | --- | --- |
| [`ejercicio-1/`](ejercicio-1) | Alojamientos AirBnB de Oporto: entidades de las descripciones y análisis de comentarios | `analisis_airbnb.ipynb` |
| [`ejercicio-2/`](ejercicio-2) | Reseñas de videojuegos: pipeline de dos LLMs (filtrado + extracción) | `analisis_videojuegos.ipynb` |

Los dos usan la **API de Groq**, **batching** de varias filas por llamada y
**gestión de rate limits** (rotación de claves + `Retry-After`). Todo el
razonamiento de Prompt Engineering está explicado dentro de cada notebook.

## Requisitos

- **Python 3.11–3.13** y **[uv](https://docs.astral.sh/uv/)**.
- Una **API key gratuita de Groq**: https://console.groq.com → *API Keys*.

## Instalación

Un único entorno en la raíz sirve para los dos ejercicios.

```bash
# 1. Instalar dependencias y crear el entorno (.venv) con uv
uv sync

# 2. Configurar la API key (el .env va en la raíz, lo leen los dos notebooks)
cp .env.example .env          # Windows: copy .env.example .env
# edita .env y pon tu GROQ_API_KEY=gsk_...

# 3. (Opcional) registrar el kernel de Jupyter
uv run python -m ipykernel install --user --name pontia-videojuegos \
    --display-name "Pontia Videojuegos (uv)"
```

## Ejecución

```bash
uv run jupyter lab
```

Abre el notebook de la carpeta del ejercicio, comprueba que el kernel es
**"Pontia Videojuegos (uv)"** y ejecuta **Kernel → Restart & Run All** (en VS Code:
selecciona el mismo kernel y pulsa **Run All**). Cada notebook escribe sus
resultados en `output/` dentro de su carpeta.

## Ejercicio 1 — AirBnB Oporto

| Archivo | Descripción |
| --- | --- |
| `analisis_airbnb.ipynb` | Parte 1 (entidades con `openai/gpt-oss-120b`) y Parte 2 (comentarios con `openai/gpt-oss-20b`). |
| `data/listings1_cleaned.csv` | 12.742 anuncios con descripción (HTML limpiado, sin las columnas del anfitrión). |
| `data/Airbnb_reviews_5000.csv` | Las 5.000 reseñas más recientes de esos anuncios (sin nombre ni id del revisor). |

Los textos libres (descripciones y comentarios) pueden seguir mencionando nombres
de pila, como en la fuente pública original.
| `scripts/preparar_datos.py` | Regenera los dos CSV desde Inside Airbnb. |
| `output/` | `entidades_alojamientos.csv/.json`, `analisis_comentarios.csv`, `analisis_por_alojamiento.csv` (se generan al ejecutar; no versionados). |

Los CSV del curso no estaban disponibles, así que se reconstruyen con los datos
públicos de [Inside Airbnb](https://insideairbnb.com) (Oporto, snapshot
2026-09-19, licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)):

```bash
uv run python ejercicio-1/scripts/preparar_datos.py
```

## Ejercicio 2 — Reseñas de videojuegos

| Archivo | Descripción |
| --- | --- |
| `analisis_videojuegos.ipynb` | Pipeline completo y justificaciones. |
| `data/videogames_reviews.csv` | Dataset de entrada (20.000 reseñas). |
| `output/analisis_videojuegos_resultados.csv` | Salida estructurada (se genera al ejecutar; no versionada). |

> **Aviso.** Los modelos que usa este notebook (`llama-3.1-8b-instant` y
> `llama-3.3-70b-versatile`) ya no están disponibles en Groq. Para volver a
> ejecutarlo hay que cambiar `MODELO_FILTRO` y `MODELO_EXTRACCION` (por ejemplo a
> `openai/gpt-oss-20b` y `openai/gpt-oss-120b`, como en el Ejercicio 1).
