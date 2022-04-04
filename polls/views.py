from asyncio.format_helpers import _format_callback_source
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView, DetailView, ListView, CreateView

from .models import Question, Choice, UserProfile
from .forms import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import *

# classes to handle auth
class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('polls:index')

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_message = "Your profile was created successfully"

class IndexView(ListView):    
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'polls/detail.html'

class QuestionResultsView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = 'polls/results.html'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    # model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/view_profile.html'
    success_url = reverse_lazy('polls:profile')

    def get_context_data(self, **kwargs):
            data = super(ProfileUpdateView, self).get_context_data(**kwargs)
            if self.request.POST:
                data['userProfile'] = userProfileFormSet(self.request.POST)
            else:
                data['userProfile'] = userProfileFormSet()
            return data


    def form_valid(self, form):
        context = self.get_context_data()
        profile = context['userProfile']
        if profile.is_valid():
            self.object = form.save()
            profile.instance = self.object
            profile.save()
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        #  return reverse('polls:profile', kwargs={'pk': self.pk})
        return reverse('polls:profile', kwargs={'pk': self.request.user.id})


    

    def get_queryset(self):
        userProfile = User.objects.get(id=self.request.user.id)
        print(userProfile)
        return User.objects.filter(id=userProfile.id)


# class SuccessView(LoginRequiredMixin, DetailView):
#     model = UserProfile
#     template_name = 'accounts/view_profile.html'

# class EditProfile(LoginRequiredMixin, generic.FormView):
#     model = UserProfile
#     template_name = 'accounts/edit_profile.html'
#     context_object_name = 'edit_profile'
#     success_url = '/accounts/view_profile.html'



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
