from bboard.models import Rubric


def my_middleware(next):
    def core_middleware(request):
        # обработка клиентского запроса
        response = next(request)
        # обработка ответа
        return response
    return core_middleware


class MyMiddleware:
    def __init__(self, next):
        self._next = next

    def __call__(self, request):
        # Обработка клиентского запроса
        response = self._next(request)
        # Обработка ответа
        return response


class RubricsMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_template_response(self, request, response):
        response.context_data['rubrics'] = Rubric.objects.all()
        return response
