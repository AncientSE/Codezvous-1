from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.utils import timezone
from .models import Submit, Identity
from .forms import UserForm, SubmitForm, IdentityForm
from django.contrib.auth.views import logout


# Create your views here.
def homepage(request):  # homepage
    if request.user.is_authenticated():
        identity = Identity.objects.filter(name=request.user)
        if(len(identity) is not 0):
            if(identity[0].identity==identity[0].STUDENT):
                submits = Submit.objects.filter(submit_time__lte=timezone.now(), student=request.user).order_by('submit_time')
                return render(request, 'ancient/home_student.html', {'submits': submits, 'user': request.user})
            else:
                return render(request, 'ancient/home_teacher.html', { 'user': request.user})
        else:
            return redirect('/admin')
    else:
        return redirect('/login')


class UserFormView(View):  # register
    form_class_user = UserForm
    form_class_identity = IdentityForm
    template_name = 'ancient/register.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('homepage')
        else:
            form_user = self.form_class_user(None)
            form_identity = self.form_class_identity(None)
            return render(request, self.template_name, {'form_user': form_user, 'form_identity': form_identity})

    def post(self, request):
        form_user = self.form_class_user(request.POST)
        form_identity = self.form_class_identity(request.POST)
        if form_user.is_valid() and form_identity.is_valid():
            user = form_user.save(commit=False)
            username = form_user.cleaned_data['username']
            password = form_user.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            identity = form_identity.save(commit=False)  # save identity
            identity.set_name(user)
            print(identity.identity)
            identity.save()
            identity_i = identity.identity  # get the identity, i.e, student or teacher
            is_identity = Identity.objects.filter(name=user, identity=identity_i)
            if user is not None and len(is_identity) is not 0:
                if user.is_active:
                    login(request, user)
                    return redirect('/')

        return render(request, self.template_name, {'form_user': form_user, 'form_identity': form_identity})


def submit_new(request):  # submit
    if request.method == "POST":
        form = SubmitForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.student = request.user
            post.submit_time = timezone.now()
            post.save()
            return redirect('/')
    else:
        form = SubmitForm()
    return render(request, 'ancient/submit_1.html', {'form': form})