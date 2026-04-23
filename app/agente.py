"""
Agente de IA para Analisis de Costos de Equipos de Construccion.

Este modulo contiene la logica del agente con las herramientas (tools)
que consultan los resultados del EDA, modelamiento y proyecciones.

El agente usa Claude via AWS Bedrock y decide que herramienta usar
segun la pregunta del usuario.

Uso:
    from agente import Agente
    agente = Agente()
    respuesta = agente.consultar("Cual es el mejor modelo para Equipo 1?")
"""

import boto3
import json

# --- Configuracion ---
BUCKET = 'consulting-dataknow-prueba-tecnica'
MODEL_ID = 'us.anthropic.claude-sonnet-4-5-20250929-v1:0'
REGION = 'us-east-2'


# --- Carga de datos desde S3 ---
class DatosS3:
    """Cache de JSONs desde S3."""

    def __init__(self):
        self.s3 = boto3.client('s3', region_name=REGION)
        self._cache = {}

    def cargar(self, key):
        if key not in self._cache:
            try:
                obj = self.s3.get_object(Bucket=BUCKET, Key=key)
                self._cache[key] = json.loads(obj['Body'].read())
            except Exception as e:
                self._cache[key] = {"error": str(e)}
        return self._cache[key]

    @property
    def estadisticas(self):
        return self.cargar('eda_resultados/estadisticas_descriptivas.json')

    @property
    def normalidad(self):
        return self.cargar('eda_resultados/test_normalidad.json')

    @property
    def estacionariedad(self):
        return self.cargar('eda_resultados/test_estacionariedad.json')

    @property
    def correlaciones(self):
        return self.cargar('eda_resultados/correlaciones.json')

    @property
    def causalidad_granger(self):
        return self.cargar('eda_resultados/causalidad_granger.json')

    @property
    def anomalias(self):
        return self.cargar('eda_resultados/anomalias.json')

    @property
    def volatilidad(self):
        return self.cargar('eda_resultados/volatilidad.json')

    @property
    def vif(self):
        return self.cargar('eda_resultados/vif.json')

    @property
    def mutual_information(self):
        return self.cargar('eda_resultados/mutual_information.json')

    @property
    def evaluacion_features(self):
        return self.cargar('eda_resultados/evaluacion_features.json')

    @property
    def feature_importance(self):
        return self.cargar('eda_resultados/feature_importance.json')

    @property
    def segmentacion_covid(self):
        return self.cargar('eda_resultados/segmentacion_covid.json')

    @property
    def rezagos(self):
        return self.cargar('eda_resultados/analisis_rezagos.json')

    @property
    def resumen_eda(self):
        return self.cargar('eda_resultados/resumen_eda.json')

    @property
    def comparacion_modelos(self):
        return self.cargar('eda_resultados/comparacion_modelos.json')

    @property
    def info_modelos(self):
        return self.cargar('eda_resultados/info_modelos_completa.json')

    @property
    def residuos(self):
        return self.cargar('eda_resultados/analisis_residuos.json')

    @property
    def validacion_dist(self):
        return self.cargar('eda_resultados/validacion_distribucional.json')

    @property
    def prophet_resultados(self):
        return self.cargar('eda_resultados/prophet_resultados.json')

    @property
    def resumen_modelamiento(self):
        return self.cargar('eda_resultados/resumen_modelamiento.json')

    @property
    def proyecciones(self):
        return self.cargar('predicciones/proyecciones_resumen.json')


# --- Definicion de Tools ---
TOOLS = [
    {
        "name": "consultar_eda",
        "description": "Consulta resultados del analisis exploratorio de datos: estadisticas descriptivas, distribucion, normalidad, estacionariedad, anomalias de cualquier variable (Price_X, Price_Y, Price_Z, Price_Equipo1, Price_Equipo2). Usa esta herramienta cuando pregunten sobre las caracteristicas de los datos, distribucion, valores atipicos, estacionariedad o estadisticas basicas.",
        "input_schema": {
            "type": "object",
            "properties": {
                "variable": {
                    "type": "string",
                    "description": "Variable a consultar: Price_X, Price_Y, Price_Z, Price_Equipo1, Price_Equipo2, o 'todas' para resumen general."
                }
            },
            "required": ["variable"]
        }
    },
    {
        "name": "consultar_correlaciones",
        "description": "Consulta correlaciones entre variables (Pearson, Spearman), VIF (multicolinealidad), mutual information y causalidad de Granger. Usa esta herramienta cuando pregunten sobre relaciones entre variables, que materias primas influyen mas, multicolinealidad o dependencias.",
        "input_schema": {
            "type": "object",
            "properties": {
                "tipo": {
                    "type": "string",
                    "description": "Tipo de consulta: 'pearson', 'spearman', 'vif', 'mutual_info', 'granger', 'rezagos', o 'todas' para resumen completo."
                }
            },
            "required": ["tipo"]
        }
    },
    {
        "name": "consultar_features",
        "description": "Consulta informacion sobre las features creadas, cuales se seleccionaron, ranking de importancia por correlacion y mutual information, y evaluacion de features con y sin interacciones. Usa esta herramienta cuando pregunten sobre feature engineering, que variables son mas importantes, o seleccion de features.",
        "input_schema": {
            "type": "object",
            "properties": {
                "equipo": {
                    "type": "string",
                    "description": "Equipo a consultar: 'Price_Equipo1', 'Price_Equipo2', o 'ambos'."
                }
            },
            "required": ["equipo"]
        }
    },
    {
        "name": "consultar_modelo",
        "description": "Consulta metricas, parametros, residuos y detalles de cualquier modelo entrenado (Lasso, Ridge, LinearRegression, ElasticNet, RandomForest, GradientBoosting, XGBoost). Incluye comparacion entre rondas de entrenamiento. Usa esta herramienta cuando pregunten sobre un modelo especifico, sus metricas, parametros, o comparacion entre modelos.",
        "input_schema": {
            "type": "object",
            "properties": {
                "consulta": {
                    "type": "string",
                    "description": "Que consultar: 'mejor_modelo', 'comparacion', 'residuos', 'feature_importance', 'validacion_distribucional', o nombre de un modelo especifico."
                },
                "equipo": {
                    "type": "string",
                    "description": "Equipo: 'Price_Equipo1', 'Price_Equipo2', o 'ambos'."
                }
            },
            "required": ["consulta"]
        }
    },
    {
        "name": "consultar_prophet",
        "description": "Consulta resultados especificos de Prophet: metricas, changepoints detectados, componentes, parametros, intervalos de confianza, cobertura del IC, y residuos. Usa esta herramienta cuando pregunten especificamente sobre Prophet o modelos de series de tiempo.",
        "input_schema": {
            "type": "object",
            "properties": {
                "equipo": {
                    "type": "string",
                    "description": "Equipo: 'Price_Equipo1', 'Price_Equipo2', o 'ambos'."
                }
            },
            "required": ["equipo"]
        }
    },
    {
        "name": "proyectar_costos",
        "description": "Consulta las proyecciones de costos de los equipos para los proximos meses. Incluye proyeccion mensual con Prophet (con intervalos de confianza al 95%) y Lasso, horizonte de prediccion, justificacion del horizonte, y analisis de incertidumbre. Usa esta herramienta cuando pregunten sobre proyecciones, costos futuros, presupuesto, o cuanto va a costar un equipo.",
        "input_schema": {
            "type": "object",
            "properties": {
                "equipo": {
                    "type": "string",
                    "description": "Equipo: 'Price_Equipo1', 'Price_Equipo2', o 'ambos'."
                },
                "mes": {
                    "type": "string",
                    "description": "Mes especifico (formato YYYY-MM, ej: '2024-01') o 'todos' para el horizonte completo."
                }
            },
            "required": ["equipo"]
        }
    },
    {
        "name": "consultar_segmentacion",
        "description": "Consulta resultados del analisis por periodos: pre-COVID, COVID y post-COVID. Incluye estadisticas, correlaciones y comportamiento de las relaciones en cada periodo. Usa esta herramienta cuando pregunten sobre el impacto del COVID, cambios de regimen, o diferencias entre periodos.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "consultar_volatilidad",
        "description": "Consulta resultados del analisis de volatilidad: rolling std de retornos a 30 y 90 dias, clusters de volatilidad, y maximos historicos de volatilidad. Usa esta herramienta cuando pregunten sobre volatilidad, riesgo, variabilidad de precios o estabilidad.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "comparar_modelos",
        "description": "Devuelve la tabla comparativa completa de todos los modelos entrenados con sus metricas (R2, RMSE, MAE, MAPE), ronda de entrenamiento, y gap train-test (indicador de sobreajuste). Incluye todos los modelos: lineales, tree-based y Prophet. Usa esta herramienta cuando pregunten cual es el mejor modelo, comparar modelos, o ver la tabla de resultados.",
        "input_schema": {
            "type": "object",
            "properties": {
                "equipo": {
                    "type": "string",
                    "description": "Equipo: 'Price_Equipo1', 'Price_Equipo2', o 'ambos'."
                }
            },
            "required": ["equipo"]
        }
    }
]


# --- Implementacion de Tools ---
def ejecutar_tool(nombre, parametros, datos):
    """Ejecuta una tool y devuelve el resultado como string."""

    if nombre == "consultar_eda":
        variable = parametros.get("variable", "todas")
        resultado = {}

        if variable == "todas":
            resultado["resumen"] = datos.resumen_eda
            resultado["estadisticas"] = datos.estadisticas
        else:
            resultado["estadisticas"] = {k: v.get(variable) for k, v in datos.estadisticas.items() if isinstance(v, dict)}
            resultado["normalidad"] = datos.normalidad.get(variable, {})
            resultado["estacionariedad"] = datos.estacionariedad.get(variable, {})
            resultado["anomalias"] = datos.anomalias.get(variable, {})

        return json.dumps(resultado, ensure_ascii=False, default=str)

    elif nombre == "consultar_correlaciones":
        tipo = parametros.get("tipo", "todas")
        resultado = {}

        if tipo == "todas" or tipo == "pearson":
            resultado["pearson"] = datos.correlaciones.get("pearson", {})
        if tipo == "todas" or tipo == "spearman":
            resultado["spearman"] = datos.correlaciones.get("spearman", {})
        if tipo == "todas" or tipo == "vif":
            resultado["vif"] = datos.vif
        if tipo == "todas" or tipo == "mutual_info":
            resultado["mutual_information"] = datos.mutual_information
        if tipo == "todas" or tipo == "granger":
            resultado["causalidad_granger"] = datos.causalidad_granger
        if tipo == "todas" or tipo == "rezagos":
            resultado["rezagos"] = datos.rezagos

        return json.dumps(resultado, ensure_ascii=False, default=str)

    elif nombre == "consultar_features":
        equipo = parametros.get("equipo", "ambos")
        resultado = {}

        if equipo == "ambos":
            resultado["evaluacion"] = datos.evaluacion_features
            resultado["importance"] = datos.feature_importance
        else:
            resultado["evaluacion"] = datos.evaluacion_features.get(equipo, {})
            resultado["importance"] = datos.feature_importance.get(equipo, {})

        resultado["resumen"] = datos.resumen_eda

        return json.dumps(resultado, ensure_ascii=False, default=str)

    elif nombre == "consultar_modelo":
        consulta = parametros.get("consulta", "mejor_modelo")
        equipo = parametros.get("equipo", "ambos")
        resultado = {}

        info = datos.info_modelos

        if consulta == "mejor_modelo":
            if equipo == "ambos":
                for t in ["Price_Equipo1", "Price_Equipo2"]:
                    resultado[t] = info[t]["mejor_modelo_ml"]
            else:
                resultado[equipo] = info.get(equipo, {}).get("mejor_modelo_ml", {})

        elif consulta == "comparacion":
            if equipo == "ambos":
                resultado = datos.comparacion_modelos
            else:
                resultado = datos.comparacion_modelos.get(equipo, [])

        elif consulta == "residuos":
            resultado["lasso"] = datos.residuos
            resultado["prophet"] = {t: info[t]["prophet"].get("residuos", {}) for t in ["Price_Equipo1", "Price_Equipo2"]}

        elif consulta == "feature_importance":
            resultado = datos.feature_importance

        elif consulta == "validacion_distribucional":
            resultado = datos.validacion_dist

        else:
            # Buscar modelo especifico en la comparacion
            comp = datos.comparacion_modelos
            for t in ["Price_Equipo1", "Price_Equipo2"]:
                modelos_target = [m for m in comp.get(t, []) if consulta.lower() in m.get("modelo", "").lower()]
                if modelos_target:
                    resultado[t] = modelos_target

        return json.dumps(resultado, ensure_ascii=False, default=str)

    elif nombre == "consultar_prophet":
        equipo = parametros.get("equipo", "ambos")
        info = datos.info_modelos
        resultado = {}

        targets = ["Price_Equipo1", "Price_Equipo2"] if equipo == "ambos" else [equipo]
        for t in targets:
            resultado[t] = info.get(t, {}).get("prophet", {})

        return json.dumps(resultado, ensure_ascii=False, default=str)

    elif nombre == "proyectar_costos":
        equipo = parametros.get("equipo", "ambos")
        mes = parametros.get("mes", "todos")
        proy = datos.proyecciones
        resultado = {"horizonte": proy.get("horizonte", {})}

        targets = ["Price_Equipo1", "Price_Equipo2"] if equipo == "ambos" else [equipo]

        resultado["proyecciones"] = {}
        for t in targets:
            mensual = proy.get("resumen_mensual", {}).get(t, {})
            if mes != "todos" and mes in mensual:
                resultado["proyecciones"][t] = {mes: mensual[mes]}
            else:
                resultado["proyecciones"][t] = mensual

        resultado["incertidumbre"] = {t: proy.get("incertidumbre", {}).get(t, {}) for t in targets}
        resultado["fuentes"] = proy.get("fuentes_datos_proyeccion", {})
        resultado["modelos_usados"] = proy.get("modelos_usados", {})

        return json.dumps(resultado, ensure_ascii=False, default=str)

    elif nombre == "consultar_segmentacion":
        return json.dumps(datos.segmentacion_covid, ensure_ascii=False, default=str)

    elif nombre == "consultar_volatilidad":
        return json.dumps(datos.volatilidad, ensure_ascii=False, default=str)

    elif nombre == "comparar_modelos":
        equipo = parametros.get("equipo", "ambos")
        resultado = {}

        if equipo == "ambos":
            resultado = datos.comparacion_modelos
        else:
            resultado = datos.comparacion_modelos.get(equipo, [])

        # Agregar resumen
        resultado["resumen"] = datos.resumen_modelamiento
        resultado["observaciones"] = datos.info_modelos.get("Price_Equipo1", {}).get("observaciones", [])

        return json.dumps(resultado, ensure_ascii=False, default=str)

    return json.dumps({"error": f"Tool '{nombre}' no encontrada"})


# --- System Prompt ---
SYSTEM_PROMPT = """Eres un agente de IA especializado en el analisis de costos de equipos de construccion.

Tienes acceso a los resultados completos de un proyecto de ciencia de datos que analizo la relacion entre precios de materias primas (X, Y, Z) y costos de dos tipos de equipos de construccion (Equipo 1 y Equipo 2).

CONTEXTO DEL PROYECTO:
- Datos historicos de 2010 a agosto 2023 (3,530 registros diarios)
- 3 materias primas (X, Y, Z) y 2 equipos
- Se realizo un EDA exhaustivo, feature engineering, y se entrenaron multiples modelos
- El mejor modelo es Lasso (R2 ~0.991 para Equipo1, ~0.985 para Equipo2)
- Prophet se usa para proyecciones con intervalos de confianza
- Se proyecto a 6 meses (sep 2023 - feb 2024)

HALLAZGOS PRINCIPALES:
- Price_Y es el predictor dominante del Equipo 1 (correlacion 0.997)
- Price_Z es el predictor dominante del Equipo 2 (correlacion 0.983)
- Price_X tiene correlacion moderada con ambos (~0.53)
- La relacion es fundamentalmente lineal
- Los modelos tree-based se sobreajustaron por cambio de regimen post-COVID
- Las series no son estacionarias en niveles pero si en primera diferencia

INSTRUCCIONES:
- Usa las herramientas disponibles para responder con datos reales, no de memoria
- Si te preguntan algo que requiere datos especificos, usa la herramienta correspondiente
- Responde en espanol
- Se conciso pero informativo
- Cuando des metricas, explica brevemente que significan
- Si te preguntan sobre la diferencia entre IA convencional y agente de IA, explica:
  * IA convencional: modelo que predice, clasifica o genera a partir de datos (ej: Lasso, Prophet)
  * Agente de IA: sistema autonomo que percibe su entorno, toma decisiones y ejecuta acciones usando herramientas, memoria y razonamiento para alcanzar un objetivo
  * Tu mismo eres un ejemplo de agente: recibes preguntas, decides que herramienta usar, consultas datos y generas respuestas"""


# --- Clase Agente ---
class Agente:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime', region_name=REGION)
        self.datos = DatosS3()
        self.historial = []

    def consultar(self, mensaje_usuario):
        """Envia un mensaje al agente y obtiene respuesta."""

        self.historial.append({"role": "user", "content": mensaje_usuario})

        # Llamar a Bedrock con tools
        response = self._llamar_bedrock(self.historial)

        # Procesar respuesta (puede haber multiples tool calls)
        while response.get("stop_reason") == "tool_use":
            # Extraer tool calls
            assistant_content = response["content"]
            self.historial.append({"role": "assistant", "content": assistant_content})

            # Ejecutar cada tool call
            tool_results = []
            for block in assistant_content:
                if block.get("type") == "tool_use":
                    resultado = ejecutar_tool(block["name"], block["input"], self.datos)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block["id"],
                        "content": resultado
                    })

            self.historial.append({"role": "user", "content": tool_results})

            # Llamar de nuevo a Bedrock con los resultados
            response = self._llamar_bedrock(self.historial)

        # Extraer texto final
        texto_respuesta = ""
        for block in response.get("content", []):
            if block.get("type") == "text":
                texto_respuesta += block["text"]

        self.historial.append({"role": "assistant", "content": response.get("content", [])})

        return texto_respuesta

    def _llamar_bedrock(self, messages):
        """Llama a Bedrock con messages y tools."""

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "system": SYSTEM_PROMPT,
            "messages": messages,
            "tools": TOOLS
        }

        response = self.bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body)
        )

        return json.loads(response['body'].read())

    def reiniciar(self):
        """Reinicia el historial de conversacion."""
        self.historial = []


# --- Ejecucion directa para pruebas ---
if __name__ == "__main__":
    agente = Agente()

    print("Agente de Costos de Equipos de Construccion")
    print("Escribe 'salir' para terminar, 'reset' para reiniciar")
    print("-" * 50)

    while True:
        pregunta = input("\nTu: ")

        if pregunta.lower() == 'salir':
            break
        elif pregunta.lower() == 'reset':
            agente.reiniciar()
            print("Historial reiniciado.")
            continue

        try:
            respuesta = agente.consultar(pregunta)
            print(f"\nAgente: {respuesta}")
        except Exception as e:
            print(f"\nError: {e}")
