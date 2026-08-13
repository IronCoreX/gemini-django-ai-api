import os
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@csrf_exempt
def ask_gemini(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST requests are allowed."},
            status=405
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "Invalid JSON."},
            status=400
        )

    if not isinstance(data, dict):
        return JsonResponse(
            {"error": "Request body must be a JSON object."},
            status = 400
        )

    user_input = data.get("question")

    if not user_input:
        return JsonResponse(
            {"error": "Question is required."},
            status=400
        )

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=user_input,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema={
                    "type": "object",
                    "properties": {
                        "answer": {"type": "string"},
                        "topic": {"type": "string"}
                    },
                    "required": ["answer", "topic"]
                }
            )
        )

        result = json.loads(response.text) # type: ignore

    except Exception:
        return JsonResponse(
            {"error": "Unable to get a valid response from the AI service."},
            status=502
        )

    if "answer" not in result or "topic" not in result:
        return JsonResponse(
            {"error": "Invalid AI response."},
            status=502
        )

    return JsonResponse(result)