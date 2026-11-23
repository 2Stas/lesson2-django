import json

from django.http import JsonResponse
from django.shortcuts import render

from .models import CustomLocation

# Create your views here.
LOCATIONS = [
    {
        "id": 1,
        "name": "Ivano-Frankivsk City Hall",
        "category": "Landmark",
        "description": "A historic city hall in the heart of the city, now home to the Museum of History.",
        "lat": 48.9226,
        "lng": 24.7111,
    },
    {
        "id": 2,
        "name": "Shevchenko Park",
        "category": "Park",
        "description": "A popular green space with walking paths, a lake, and recreational areas.",
        "lat": 48.9155,
        "lng": 24.7047,
    },
    {
        "id": 3,
        "name": "Potocki Palace",
        "category": "Historic site",
        "description": "The remains of a 17th-century palace complex associated with the city's founders.",
        "lat": 48.9228,
        "lng": 24.7068,
    },
    {
        "id": 4,
        "name": "Cathedral of the Holy Resurrection",
        "category": "Religious site",
        "description": "A landmark Greek Catholic cathedral located near the central square.",
        "lat": 48.9227,
        "lng": 24.7092,
    },
    {
        "id": 5,
        "name": "Bastion",
        "category": "Historic site",
        "description": "A restored section of the city's old defensive fortifications with shops and galleries.",
        "lat": 48.9205,
        "lng": 24.7103,
    },
]


def map_page(request):
    locations = LOCATIONS.copy()

    custom_locations = CustomLocation.objects.all()

    for location in custom_locations:
        locations.append({
            "id": len(LOCATIONS) + location.id,
            "name": location.name,
            "category": location.category,
            "description": location.description,
            "lat": location.lat,
            "lng": location.lng,
        })

    return render(request, "places/index.html", {
        "locations": locations
    })


def create_location(request):
    try:
        data = json.loads(request.body)

        name = str(data.get("name", "")).strip()
        category = str(data.get("category", "My place")).strip()
        description = str(data.get("description", "")).strip()

        if not name:
            return JsonResponse(
                {"error": "Enter a name for the marker."},
                status=400
            )

        if len(name) > 150 or len(category) > 100:
            return JsonResponse(
                {"error": "Name or category is too long."},
                status=400
            )

        lat = float(data["lat"])
        lng = float(data["lng"])

        if not (-90 <= lat <= 90 and -180 <= lng <= 180):
            raise ValueError

        location = CustomLocation.objects.create(
            name=name,
            category=category or "My place",
            description=description,
            lat=lat,
            lng=lng
        )

        return JsonResponse({
            "id": len(LOCATIONS) + location.id,
            "name": location.name,
            "category": location.category,
            "description": location.description,
            "lat": location.lat,
            "lng": location.lng,
        }, status=201)

    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        return JsonResponse(
            {"error": "Invalid marker data."},
            status=400
        )
