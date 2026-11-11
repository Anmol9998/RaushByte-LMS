from django.http import JsonResponse
from django.shortcuts import render


def health_check(request):
    return JsonResponse({"status": "ok"}, status=200)


def custom_404(request, exception):

    if request.path.startswith('/api/'):
        return JsonResponse(
            {
                'status': 404,
                'error': 'Not found',
                'message': 'The requested API endpoint does not exist.'
            }, 
            status=404
        )

    return render(request, '404.html', status=404)