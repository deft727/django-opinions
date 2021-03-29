from django.views.generic import DetailView,View,ListView,UpdateView,CreateView
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from .forms import *
from django.template import loader
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate,login
from django.forms import formset_factory


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'tests'

    def get_queryset(self):
        return Tests.objects.all().order_by('-pk')
# .filter(is_active=True)

class DetailView(DetailView):
    model = Tests
    template_name = 'detail.html'
    context_object_name = 'test'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        total = self.get_object()
        test = self.get_object().questions.all()
        page_number = self.request.GET.get('page',1)
        if page_number == 1:
            total.max_points=0
            total.save()
        paginator= Paginator(test, 1)
        page =paginator.get_page(page_number)
        context['test'] = page
        return context


    def post(self,request,*args,**kwargs):

        page=int(self.request.GET.get('page',1))
        questionid = request.POST.get('question')
        question = get_object_or_404(Question, pk=questionid)
        test = self.get_object()
        try:
            choiceid= int(request.POST.get('choice'))
        except:
            paginator= Paginator(test.questions.all(), 1)
            page =paginator.get_page(page)
            return render(request, 'detail.html', {
            'test': paginator.get_page(page),
            'error_message': "You didn't select a choice.",
        })
        choice = Choice.objects.get(pk=choiceid)
        answer = question.answer_set.filter(choice=choice).exists()

        if answer == True:
            test.max_points += 1
            test.save()


        testquestions = test.questions.all()
        paginator= Paginator(testquestions, 1)
        page =paginator.get_page(page)

        if page.has_next():
            return redirect ('/test/{}/?page={}'.format(test.id,page.next_page_number()))
        else:
            user = Profile.objects.get(user=request.user)
            user.complete.add(test)
            return render(request,'results.html',{'test':test,})


class ProfileView(View):
    def get (self,request,*args,**kwargs):
        if not  request.user.is_authenticated:
            return redirect('registration')
        profile = Profile.objects.get(user=request.user)
        # createtest = C

        return render(request,'profile.html',{
                    'profile': profile
                    })


class RegistrationView(View):
    def get(self,request,*args,**kwargs):
        if  request.user.is_authenticated:
            return redirect('index')
        form=RegistrationForm(request.POST or None)
        title = 'Регистрация'
        context = {
            'title':title,
            'form':form,
        }
        return render(request,'registration.html',context)

    def post(self,request,*args,**kwargs):
        form= RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user=form.save(commit=False)
            new_user.username=form.cleaned_data['username']
            new_user.email=form.cleaned_data['email']
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user= authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            Profile.objects.create(user=user)
            login(request,user)
            return redirect('index')
        context={'form':form,}
        return render(request,'registration.html',context)




def updateprofile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST,request.FILES, instance=Profile.objects.get(user=request.user))
        if form.is_valid():
            form = form.save(commit=False)
            form.user=request.user
            form.save()
            return HttpResponseRedirect('/profile')
    else:
        form = UpdateProfileForm(request.POST,request.FILES, instance=Profile.objects.get(user=request.user))
    return render(request, 'updateprofile.html', {'form': form})

    

class LoginView(View):
    def get(self,request,*args,**kwargs):
        if  request.user.is_authenticated:
            return redirect('index')
        form = LoginForm(request.POST or None)
        title = 'Логин'
        context= {'title':title,
        'form':form,
        }
        return render(request,'login.html',context)

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST or None)
        if form.is_valid():
            username= form.cleaned_data['username']
            password = form.cleaned_data['password']
            if '@' in username:
                user1= User.objects.filter(email=username).first()
                user= authenticate(username=user1,password=password)
            else:
                user= authenticate(username=username,password=password)
            if user:
                login(request,user)
            return HttpResponseRedirect('/')
        context={'form':form,}
        return render(request,'login.html',context)

# inlineformset_factory

class CreateTest(CreateView):
    model = Tests
    form_class = AddTestForm
    template_name='addtest.html'

    def form_valid(self, form):
        test = form.save(commit=False)
        test.owner = Profile.objects.get(user=self.request.user)
        test.save()
        return redirect('/add/question/')


class CreateQuestion(CreateView):
    model = Question
    form_class = AddquestionsForm
    template_name='addtest.html'

    def form_valid(self, form):
        test = form.save(commit=False)
        test.save()
        Tests.objects.get(pk=test.test.pk).questions.add(test)
        return redirect('/add/question/choice/')

class CreateChoice(CreateView):
    model = Choice
    form_class = AddchoiceForm
    template_name='addtest.html'
    success_url = '/add/question/choice/answer'


class CreateAnswer(CreateView):
    model = Answer
    form_class = AddanswerForm
    template_name='addtest.html'
    success_url = '/'

