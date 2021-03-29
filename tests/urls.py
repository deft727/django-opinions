from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
        path('', IndexView.as_view(), name='index'),
            path('test/<int:pk>/',DetailView.as_view(), name='test'),
                path('profile/',ProfileView.as_view(),name='profile'),
                    path('registration/',RegistrationView.as_view(), name='registration'),
                        path('login/',LoginView.as_view(), name='login'),
                            path('logout/',LogoutView.as_view(next_page="/"), name='logout'),
                                path('updateprofile/',updateprofile,name='updateprofile'),
                path('add/', CreateTest.as_view(), name='add'),
                                path('add/question/',CreateQuestion.as_view(), name='question'),
                            path('add/question/choice/',CreateChoice.as_view(),name='choice'),
                            path('add/question/choice/answer',CreateAnswer.as_view(),name='answer'),

                    # path('vote/<int:question_id>/', vote, name='vote'),
]