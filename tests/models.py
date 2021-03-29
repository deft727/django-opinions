from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Tests(models.Model):

    class Meta:
        verbose_name='Тесты'

    owner = models.ForeignKey('Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=150,verbose_name='Название тесте')
    questions = models.ManyToManyField('Question',  blank=True, )
    max_points = models.FloatField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('test',kwargs={'pk': self.pk})

        
class Question(models.Model):

    class Meta:
        verbose_name='Вопросы'

    test = models.ForeignKey(Tests, on_delete=models.CASCADE)
    title = models.CharField(max_length=150,verbose_name='Какой вопрос')
    
    def __str__(self):
        return " {} , Тест {} ".format(self.title,self.test.title)

    def get_absolute_url(self):
        return reverse('detail',kwargs={'pk': self.pk})


class Choice(models.Model):

    class Meta:
        verbose_name='Варианты ответа'

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=4096,verbose_name='Варианты ответа')
    points = models.FloatField(default=1)

    def __str__(self):
        return "{} {}".format(self.title,self.question)


class Answer(models.Model):

    class Meta:
        verbose_name='Правильный ответ'

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.choice.title


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True)
    about = models.TextField(max_length=500,null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    create_test = models.ForeignKey(Tests,null=True,blank=True, on_delete=models.DO_NOTHING)
    complete = models.ManyToManyField(Tests,  blank=True, related_name='complete')
    
    def __str__(self):
        return self.user.username