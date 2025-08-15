
from django.shortcuts import render, redirect
from urllib.parse import quote, unquote

def home_view(request):
    if request.method == 'POST':
        youtube_link = request.POST.get('youtube_link')
        if youtube_link:
            return redirect('show_link', link=quote(youtube_link, safe=''))
    return render(request, 'home/home.html')

def show_link_view(request, link):
    return render(request, 'home/show_link.html', {'youtube_link': unquote(link)})

