import re

from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404

from word.forms import WikiWordForm
from word.models import WikiWord


def wiki_create(request, title):
    title = title.lower()
    # 생성하려는 단어가 이미 데이터베이스에 있는 경우 해당 단어의 detail url로 이동
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
        # similar() = WikiWord(Model) instance method
        relevant_instances = instance.similar()

        for item in text_to_list:
            pure_item = item.replace('**', '') if item.count('**') == 2 else item
            sub_item = item
            # 본문의 단어가 특정 Title과 일치하거나 Camel 단어이면 링크 걸림
            # Camel의 정의 : 맨 첫 글자가 대문자이고, 단어 중간에 대문자가 한번 이상 더 들어가는 단어
            if pure_item.lower() in title_list or pure_item in camel_list:
                sub_item = f'<a href="/wiki/detail/{pure_item}">{pure_item}</a>'
            # http:// 또는 https://로 시작하는 단어도 링크 걸어 줌
            elif pure_item.startswith('http://') or pure_item.startswith('https://'):
                sub_item = f'<a href="{pure_item}">{pure_item}</a>'
            # [로 시작하고 ]로 끝나는 단어는 대괄호를 삭제하여 본문에 나타나도록 하며 링크를 걸어 줌
            elif pure_item.startswith('[') and pure_item.endswith(']'):
                sub_item = f'<a href="/wiki/detail/{pure_item[1:-1]}">{pure_item[1:-1]}</a>'

            text = text.replace(item, f'<strong>{sub_item}</strong>') \
                if item.count('**') == 2 else text.replace(item, sub_item)

        context = {
            'instance': instance,
            'text': text,
            'relevant_instances': relevant_instances,
        }
        return render(request, 'wiki_detail.html', context)
    # 데이터베이스에 있지 않은 단어의 detail url 입력 시 단어 생성 Form 으로 이동
    except Http404:
        return redirect('wiki-create', title=title)
