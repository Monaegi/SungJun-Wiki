from difflib import SequenceMatcher

from django.db import models


class WikiWord(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        return super().save(*args, **kwargs)

    def similar(self):
        '''
        self.text 와 모든 인스턴스의 text 를 비교, 50% 이상 일치하는 인스턴스를 리스트에 담아서 리턴.
        str type 으로 비교하는 것 보다 split(' ')을 이용하여 list로 전환시켜 비교하는 것이
        단어들을 기준으로 조금 더 정확한 비교를 하는 것으로 판단, instance.text를 리스트로 전환하여 비교 함.
        :return:  instance list(queryset)
        '''
        queryset = self._meta.model.objects.all()
        standard_text_to_list = self.text.split(' ')
        similar_instance_list = list()
        for instance in queryset:
            target_text_to_list = instance.text.split(' ')
            ratio = SequenceMatcher(None, standard_text_to_list, target_text_to_list).ratio()
            if ratio >= 0.5:
                similar_instance_list.append(instance)
        return similar_instance_list
