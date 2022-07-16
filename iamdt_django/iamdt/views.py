from django.shortcuts import render

# Create your views here.


def index(request):
    """메인페이지"""

    return render(request, "index.html", {})
