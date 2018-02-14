import re

from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404

from word.forms import WikiWordForm
from word.models import WikiWord


def wiki_create(request, title):
    title = title.lower()
    if WikiWord.objects.filter(title=title).exists():
        return redirect('wiki-detail', title=title)

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

        for item in text_to_list:
            if item.lower() in title_list:
                text = text.replace(item, f'<a href="/wiki/detail/{item}">{item}</a>')
            elif item.startswith('http://') or item.startswith('https://'):
                text = text.replace(item, f'<a href="{item}">{item}</a>')
            elif item.startswith('[') and item.endswith(']'):
                text = text.replace(item, f'<a href="/wiki/detail/{item[1:-1]}">{item[1:-1]}</a>')
            elif item in camel_list:
                text = text.replace(item, f'<a href="/wiki/detail/{item}">{item}</a>')

        context = {
            'instance': instance,
            'text': text,
        }
        return render(request, 'wiki_detail.html', context)

    except Http404:
        title = title.lower()
        return redirect('wiki-create', title=title)
