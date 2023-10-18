from ads.models import FbGroup, IgnoreGroupWord

words = IgnoreGroupWord.objects.all()
regex_words = ['.{0,255}' + word.word + '.{0,255}' for word in words]
regex = '|'.join(regex_words)

groups = FbGroup.objects.filter(name__iregex=regex)
for group in groups:
    print(group.name)

print('\n', groups.count())