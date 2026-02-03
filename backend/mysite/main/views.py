from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
import csv
from io import TextIOWrapper

from .serializer import RegisterSerializer

@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok"})

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def upload_csv(request):
    if "file" not in request.FILES:
        return Response(
            {"error": "No file uploaded"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    file = request.FILES["file"]

    if not file.name.endswith(".csv"):
        return Response(
            {"error": "Only CSV files are allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    decoded_file = TextIOWrapper(file, encoding="utf-8")
    reader = csv.DictReader(decoded_file)

    required_fields = {
        "Equipment Name",
        "Type",
        "Flowrate",
        "Pressure",
        "Temperature",
    }

    if not required_fields.issubset(reader.fieldnames):
        return Response(
            {"error": "CSV missing required columns"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    total = 0
    flowrate_sum = 0.0
    pressure_sum = 0.0
    temperature_sum = 0.0
    type_distribution = {}

    for row in reader:
        try:
            flowrate = float(row["Flowrate"])
            pressure = float(row["Pressure"])
            temperature = float(row["Temperature"])
            eq_type = row["Type"]
        except (ValueError, KeyError):
            continue

        total += 1
        flowrate_sum += flowrate
        pressure_sum += pressure
        temperature_sum += temperature

        type_distribution[eq_type] = type_distribution.get(eq_type, 0) + 1

    if total == 0:
        return Response(
            {"error": "No valid rows found"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    response_data = {
        "total_count": total,
        "average_flowrate": flowrate_sum / total,
        "average_pressure": pressure_sum / total,
        "average_temperature": temperature_sum / total,
        "equipment_type_distribution": type_distribution,
    }

    return Response(response_data, status=status.HTTP_200_OK)