from django.shortcuts import render
from django.views import View 


class MainPage(View):
    def get(self,request, *args ,**kwargs):
        return render(
            request,
            'pages-html/main.html'
        )

