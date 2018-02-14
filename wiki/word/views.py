import re

from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404

from word.forms import WikiWordForm
from word.models import WikiWord


def wiki_create(request, title):
    title = title.lower()
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
        instance = get_object_or_404(WikiWord, title=title)
        title_list = [x.title for x in queryset]
        text = instance.text
        text_to_list = text.replace('\r\n', ' ').split(' ')
        camel_list = re.findall(r'^[A-Z]\w*?[A-Z]\w*?$', text)

        for title in title_list:
            if title in text_to_list:
                text = text.replace(title, f'<a href="/wiki/detail/{title}">{title}</a>')

        for value in text_to_list:
            if value.startswith('http://') or value.startswith('https://'):
                text = text.replace(value, f'<a href="{value}">{value}</a>')
            elif value.startswith('[') and value.endswith(']'):
                text = text.replace(value, f'<a href="/wiki/detail/{value[1:-1]}">{value[1:-1]}</a>')

        for camel in camel_list:
            if camel in text_to_list:
                text = text.replace(camel, f'<a href="/wiki/detail/{camel}">{camel}</a>')

        context = {
            'instance': instance,
            'text': text,
        }
        return render(request, 'wiki_detail.html', context)

    except Http404:
        return redirect('wiki-create', title=title)
