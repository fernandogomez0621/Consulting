# 🚀 Consulting App

Aplicación web desarrollada para la gestión, análisis y visualización de servicios de consultoría. Esta plataforma permite centralizar procesos, mejorar la toma de decisiones y ofrecer una interfaz amigable para usuarios finales.

---

## 🌐 Demo en producción

Puedes acceder a la aplicación desplegada aquí:

👉 http://3.16.212.12:8501/

---

## 📂 Repositorio

Código fuente disponible en:

👉 https://github.com/fernandogomez0621/Consulting/

---

## 🧠 Descripción del proyecto

Este proyecto implementa # 📊 Consulting — Predicción de Costos Operativos en Construcción

Solución de análisis de datos y machine learning para anticipar el costo de adquisición de equipos críticos en proyectos de construcción, a partir del comportamiento histórico de materias primas. Incluye modelo predictivo, proyección de costos con intervalos de confianza y un agente conversacional de IA para explorar los resultados de forma interactiva.

## 🚀 App Desplegada

Accede a la aplicación en producción aquí:

🔗 **[http://3.16.212.12:8501/](http://3.16.212.12:8501/)**

---

## 🧠 Contexto del Problema

Una empresa del sector constructor necesita gestionar el suministro continuo de dos tipos de equipos críticos durante la ejecución de un proyecto. Históricamente, los costos de estos equipos han mostrado comportamientos variables que generan desviaciones presupuestales recurrentes.

La solución propuesta identifica qué materias primas del mercado explican el comportamiento del precio de cada equipo, construye un modelo predictivo reproducible y proyecta los costos esperados para los meses futuros del proyecto.

---

## 📁 Estructura del Repositorio

```
Consulting/
├── app/                        # Aplicación Streamlit + Agente de IA
│   └── main.py                 # Punto de entrada de la app
├── notebooks/                  # Análisis exploratorio y modelado
│   ├── 01_EDA.ipynb            # Análisis exploratorio de datos
│   ├── 02_modelado.ipynb       # Selección de variables y entrenamiento
│   └── 03_proyeccion.ipynb     # Proyección de costos
├── informe.pdf                 # Informe final del análisis
└── a.md                        # Notas y documentación auxiliar
```

---

## ⚙️ Metodología

### 1. Análisis Exploratorio (EDA)
- Revisión de series de tiempo de precios de materias primas (X, Y, Z)
- Análisis de correlaciones con precios históricos de Equipo 1 y Equipo 2
- Identificación de variables relevantes y descarte de ruido estadístico

### 2. Modelado
- Regresión para cuantificar la relación entre materias primas y precios de equipos
- Validación del modelo con métricas estadísticas (R², MAE, RMSE)
- Selección de variables determinantes por equipo a partir del análisis

### 3. Proyección de Costos
- Proyección del comportamiento esperado de costos para los meses del proyecto
- Inclusión de intervalos de confianza para reflejar la incertidumbre
- Justificación del horizonte de predicción según la naturaleza de los datos

### 4. Agente de IA
- Agente conversacional que permite consultar los resultados del modelo de forma interactiva
- Combina el pronóstico con contexto externo de mercado (tendencias, noticias del sector, contexto económico)
- A diferencia de un modelo convencional, el agente es **autónomo**, usa **herramientas**, tiene **memoria** y puede **ejecutar acciones** para alcanzar un objetivo


---

## 🛠️ Tecnologías Utilizadas

- **Python** — Lenguaje principal
- **Streamlit** — Interfaz web interactiva y agente conversacional
- **Pandas / NumPy** — Procesamiento de datos
- **Scikit-learn / Statsmodels** — Modelado estadístico y predictivo
- **Matplotlib / Plotly** — Visualización de datos
- **Jupyter Notebook** — Análisis exploratorio
- **AWS** — Infraestructura cloud

---

## ⚙️ Instalación y Ejecución Local

### 1. Clonar el repositorio

```bash
git clone https://github.com/fernandogomez0621/Consulting.git
cd Consulting
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
streamlit run app/main.py
```

La aplicación estará disponible en `http://localhost:8501`.

---

## 📄 Informe

El archivo [`informe.pdf`](./informe.pdf) incluye:

- Explicación del caso
- Supuestos del análisis
- Formas para resolver el caso y opción seleccionada
- Resultados del análisis de datos y modelos
- Proyección de costos y horizonte de predicción
- Futuros ajustes o mejoras
- Apreciaciones y comentarios del caso

---

## 📊 Entregables

- ✅ Código funcional
- ✅ Proyección de costos con intervalos de confianza
- ✅ Agente de IA conversacional interactivo
- ✅ Arquitectura propuesta en la nube
- ✅ Informe completo

---

## 👤 Autor

**Fernando Gómez**
- GitHub: [@fernandogomez0621](https://github.com/fernandogomez0621)

---

## 📝 Licencia

Este proyecto es de uso privado. Todos los derechos reservados.

---



---

## 👨‍💻 Autor

**Andres Fernando Gomez**  
Data Scientist | Developer | Data Analyst  
📍 Bogotá, Colombia  

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT.
