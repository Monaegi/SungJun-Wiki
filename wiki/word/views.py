from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404

from word.forms import WikiWordForm
from word.models import WikiWord


def wiki_create(request, title):
    title = title
    if request.method == 'POST':
        form = WikiWordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wiki-detail', title=title)
    else:
        form = WikiWordForm()

    context = {
        'title': title,
        'form': form,
    }
    return render(request, 'wiki_form.html', context)


def wiki_detail(request, title):
    try:
        wikiword = get_object_or_404(WikiWord, title=title)
        context = {
            'wikiword': wikiword
        }
        return render(request, 'wiki_detail.html', context)
    except Http404:
        return redirect('wiki-create')
