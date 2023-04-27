from django.shortcuts import render
import requests

def fetch_todos(request):
    response = requests.get('https://jsonplaceholder.typicode.com/todos/')
    if response.status_code == 200:
        todos = response.json()
        return render(request, 'json_01/todos.html', {'todos': todos})
    else:
        return HttpResponse(f'Ошибка при запросе: {response.status_code}')

