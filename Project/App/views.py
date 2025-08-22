from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import AgentData
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AgentData
from .serializers import AgentDataSerializer
from django.utils import timezone
import datetime

SERVER_START_TIME = datetime.datetime.now(datetime.timezone.utc)

@csrf_exempt
def collect_data(request):
    api_key = request.headers.get("API-KEY")
    if api_key != "utility_api_key":
        return JsonResponse({"error": "Invalid API key"}, status=403)
    
    if request.method == "POST":
        AgentData.objects.all().delete()
        latest_data = json.loads(request.body.decode("utf-8"))
        hostname = latest_data["system_details"]["Name"]

        # Update if hostname exists, else create new
        AgentData.objects.update_or_create(
            hostname=hostname,
            defaults={"data": latest_data,
                      "created_at": timezone.now()}
        )
        return JsonResponse({"status": "success"})
    
    return JsonResponse({"error": "POST required"}, status=400)


@api_view(['GET'])
def get_data(request):
    from .views import SERVER_START_TIME
    agents = AgentData.objects.filter(created_at__gte=SERVER_START_TIME).order_by('-created_at')
    serializer = AgentDataSerializer(agents, many=True)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return Response(serializer.data)
    return render(request, "index.html", {"agents": agents})