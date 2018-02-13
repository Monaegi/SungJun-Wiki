from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404

from word.forms import WikiWordForm
from word.models import WikiWord


def wiki_create(request, title):
    title = title
    if request.method == 'POST':
        form = WikiWordForm(request.POST)
        if form.is_valid():
            form.instance.title = title
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
        queryset = WikiWord.objects.all()
        title_list = [x.title for x in queryset]
        instance = get_object_or_404(WikiWord, title=title)
        text = instance.text
        text_to_list = text.split(' ')

        for title in title_list:
            if title in text_to_list:
                text = text.replace(title, f'<a href="/wiki/detail/{title}">{title}</a>')

        context = {
            'instance': instance,
            'text': text,
        }
        return render(request, 'wiki_detail.html', context)

    except Http404:
        return redirect('wiki-create', title=title)
