from django.http import JsonResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from bson import json_util
from datetime import datetime
import sys
import uuid
import json
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
import itertools
from datetime import datetime, timedelta
import openai
from .openai import generate_quote
#from django_sslify import middleware

def printf(x):
    print(x, file=sys.stderr)
    
openai.api_key = ""
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]
collection.delete_many({})

unique_id = str(uuid.uuid4())
one = {
        "id": unique_id,
        'title' :  'Gym',
        'description' : 'Hit the Gym',
        'date' : "2023-04-01",
        'duration' : '2',
        'deadline' : "2023-04-01",
        'type' : 'Personal',
        "progress": 0,

}

unique_id = str(uuid.uuid4())
quote1 = "quote1"
two = {
        "id": unique_id,
        'title' :  'Machine Learning Project',
        'description' : 'Implementing exchange rate prediction using different regression models and choosing the best from them',
        'date' : "2023-04-01",
        'duration' : '8',
        'deadline' : "2023-04-10",
        'type' : 'Personal',
        "progress": 1,
        "quote": quote1
}

quote2 = "quote2"
two = {
        "id": unique_id,
        'title' :  'Deep Learning',
        'description' : 'Implementing exchange rate prediction using different regression models and choosing the best from them',
        'date' : "2023-04-01",
        'duration' : '8',
        'deadline' : "2023-04-10",
        'type' : 'Personal',
        "progress": 2,
        "quote": quote2
}
collection.insert_one(one)
collection.insert_one(two)

printf(collection)

def fetch():
    data = []
    printf(collection.find())
    blocks = collection.find()

    data = []
    for block in blocks:
        data.append(block)
    printf(data)
    json_data = parse_json(data)

    # Print the JSON string
    print(json_data)
    return {"data":json_data}

def parse_json(data):
    return json.loads(json_util.dumps(data))

# def clear_all(request):
#     # Implement logic to clear all data from database
#     return JsonResponse({'status': 'success'})

# def create(request):
#     # Implement logic to create a new record in the database
#     return JsonResponse({'status': 'success'})

# def read(request):
#     # Implement logic to read data from the database
#     return JsonResponse({'status': 'success'})

# def update(request):
#     # Implement logic to update a record in the database
#     return JsonResponse({'status': 'success'})

# def delete(request):
#     # Implement logic to delete a record from the database
#     return JsonResponse({'status': 'success'})

# def optimize(request):
#     # Implement logic to optimize the database
#     return JsonResponse({'status': 'success'})

# def route(request):
#     return HttpResponse('Hello World!')

def clear(request):
    # Implement logic to clear all data from database
    collection.delete_many({})
    return HttpResponse('Cleared all')

def create(request):
    if request.method == 'GET':
        return JsonResponse({'status': 'error', 'message': 'GET requests not supported'})
    elif request.method == 'POST':
        data = request.POST.dict()
        unique_id = str(uuid.uuid4())

        try:
            my_data = {   
                "id": unique_id,
                "title": data.get('title'),
                "description": data.get('description'),
                "duration": data.get('duration'),
                "date": str("2023-04-01"),
                "deadline": data.get('deadline'),
                "type": data.get('type'),
                "progress": 0
            }
            quote = generate_quote(my_data)
            my_data = {   
                "id": unique_id,
                "title": data.get('title'),
                "description": data.get('description'),
                "duration": data.get('duration'),
                #"date": str(datetime.today().replace(microsecond=0)),
                "date": str("2023-04-01"),
                "deadline": data.get('deadline'),
                "type": data.get('type'),
                "progress": 0,
                "quote": quote
            }

            # Implement logic to insert data into database
            x = parse_json({"data": my_data})
            return JsonResponse({'status': 'success', 'message': 'Data inserted successfully!', 'data': x})

        except Exception as e:
            printf(e)
            return JsonResponse({"Exception": "ERRROROROROROROROOR" + e})
    else:
        return JsonResponse({'status': 'error', 'message': 'Unsupported request method'})


def read(request):
    data = []
    blocks = collection.find()

    for block in blocks:
        data.append(block)

    # Convert data to JSON string
    json_data = json.dumps(data)

    # Convert JSON string to JSON response
    return JsonResponse({'data': json_data})


def update(request):
    if request.method == 'GET':
        return JsonResponse({'status': 'error', 'message': 'GET requests not supported'})
    elif request.method == 'POST':
        data = request.POST.dict()
        blocks = collection.find()

        old_data = []
        quote = ""
        for block in blocks:
            old_data.append(block)
        if old_data["progress"] != data["progress"]:
            quote = generate_quote(data)

        my_query = {
            "id": data["id"]}

        new_values = {"$set": {
            "title": data.get('title'),
            "description": data.get("description"),
            "duration": data.get("duration"),
            "date": data.get("date"),
            "deadline": data.get("deadline"),
            "type": data.get("type"),
            "progress": data.get("progress"),
            "quote": quote
        }}
        # Implement logic to update data in database
        return JsonResponse({'status': 'success', 'message': 'Data updated successfully!', 'data': new_values})
    else:
        return JsonResponse({'status': 'error', 'message': 'Unsupported request method'})


def delete(request):
    if request.method == 'GET':
        return JsonResponse({'status': 'error', 'message': 'GET requests not supported'})
    elif request.method == 'POST':
        data = request.POST.dict()
        my_query = {"id": data["id"]}
        # Implement logic to delete data from database
        return JsonResponse({'status': 'success', 'message': 'Data deleted successfully!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Unsupported request method'})
    

def optimize(request):
    d = fetch()
    data = fetch()["data"]

    events = []
    for i in data:
        events.append(i)

    # Step 1: Sort the events by deadline
    events = sorted(events, key=lambda x: datetime.strptime(x["deadline"], "%Y-%m-%d"))

    # Step 2: Assign priority scores to each event based on deadline
    for i, event in enumerate(events):
        event["priority"] = i

    # Step 3: Initialize the scheduling queue with all events
    scheduling_queue = events.copy()

    # Step 4: Schedule events based on priority score
    current_time = datetime.strptime("2023-04-01", "%Y-%m-%d")  # Set initial time as a datetime object
    while scheduling_queue:
        # Select the event with the highest priority score
        next_event = max(scheduling_queue, key=lambda x: x["priority"])
        # Convert the deadline string to a datetime object
        deadline = datetime.strptime(next_event["deadline"], "%Y-%m-%d")
        # Check if there is enough time to complete the event before the deadline
        if current_time + timedelta(days=int(next_event["duration"])) <= deadline:
            # Assign the event to the current time slot
            next_event["start_time"] = current_time
            current_time += timedelta(days=int(next_event["duration"]))
            # Remove the event from the scheduling queue
            scheduling_queue.remove(next_event)
        else:
            # Remove the event from the scheduling queue if there isn't enough time
            scheduling_queue.remove(next_event)

    # Print the scheduled events
    for event in events:
        print(event)

    return JsonResponse({"sorted_data": events})

