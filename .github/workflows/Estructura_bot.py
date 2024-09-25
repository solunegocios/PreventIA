from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, TurnContext
from botbuilder.schema import Activity
import openai
import requests

app = Flask(__name__)
adapter = BotFrameworkAdapter("YOUR_APP_ID", "YOUR_APP_PASSWORD")

class MyBot:
    async def on_turn(self, turn_context: TurnContext):
        user_input = turn_context.activity.text
        
        # Preparar los datos en formato JSON para enviar al servicio de predicción
        datos_para_prediccion = {
            "Panel vista": 1, 
            "Panel pdf": 2, 
            "Reporte S": 3, 
            "Reporte M": 4, 
            "Reporte C": 5, 
            "Indicador S": 6, 
            "Indicador M": 7, 
            "Indicador C": 8, 
            "Cantidad_Lbaja": 9, 
            "Cantidad_Baja": 10, 
            "Cantidad_Media": 11, 
            "Cantidad_Alta": 12, 
            "Cantidad de procesos": 13
        }
        
        # Llamar al servicio web del modelo para obtener la predicción
        respuesta_modelo = requests.post("URL_DEL_SERVICIO_WEB", json=datos_para_prediccion)
        prediccion = respuesta_modelo.json()['prediccion']
        
        # Generar la propuesta basada en la predicción
        propuesta = await self.generar_propuesta(prediccion)
        await turn_context.send_activity(Activity(text=propuesta))

    async def generar_propuesta(self, prediccion):
        openai.api_key = "your_openai_api_key"
        prompt = f"""
        Basado en la predicción: {prediccion}, genera una propuesta estructurada para un proyecto de negocio. 
        Este proyecto implica la implementación de soluciones avanzadas en el ámbito de Big Data, Machine Learning, e Inteligencia Artificial.
        La propuesta debe incluir las siguientes secciones:
        1. Introducción: Contextualización
        2. Objetivos: Especifica los objetivos clave del proyecto.
        3. Metodología: Detalla las técnicas y tecnologías que se utilizarán.
        4. Cronograma: Proporciona un cronograma estimado.
        5. Presupuesto: Estima el costo asociado con la infraestructura, herramientas y recursos humanos necesarios para el proyecto.
        6. Conclusión: Resume los beneficios esperados del proyecto.
        """
        # IMPORTANTE LA ESTRUCTURA DEBE MODIFICARSE AL NUEVO ENFOQUE DE LA SOLUCIÓN
        
        respuesta = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=300
        )
        return respuesta.choices[0].text

my_bot = MyBot()

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        json_message = request.json
    else:
        return Response(status=406)
    
    activity = Activity().deserialize(json_message)
    auth_header = request.headers["Authorization"] if "Authorization" in request.headers else ""

    async def aux_func(turn_context):
        await my_bot.on_turn(turn_context)

    task = adapter.process_activity(activity, auth_header, aux_func)
    return Response(status=201)

if __name__ == "__main__":
    app.run(debug=True)
