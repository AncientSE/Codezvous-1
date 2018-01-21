from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.utils import timezone
from .models import Submit, Identity, ClassChoose, ClassTable, Homework
from .forms import UserForm, SubmitForm, IdentityForm
from django.contrib.auth.views import logout
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.

def homepage(request):  # homepage
    if request.user.is_authenticated():
        identity = Identity.objects.filter(name=request.user)
        if(len(identity) is not 0):
            if identity[0].identity == identity[0].STUDENT: #
                classchoose = ClassChoose.objects.filter(student=request.user)
                return render(request, 'ancient/home_student.html', {'classchoose': classchoose, 'user': request.user, 'numofchoose':len(classchoose)})  # the class the user has chosen
            else:
                classteaching = ClassTable.objects.filter(teacher=request.user)
                return render(request, 'ancient/home_teacher.html', { 'user': request.user, 'classteaching':classteaching,'numofchoose':len(classteaching)})
        else:
            return redirect('/admin')
    else:
        return redirect('/login')


def student_home_cs(request, classnumber):  #render the class number
    if request.user.is_authenticated():
        identity = Identity.objects.filter(name=request.user)
        if(len(identity) is not 0):
            if identity[0].identity == identity[0].STUDENT: #
                classchoose = ClassChoose.objects.filter(student=request.user)
                classrender = ClassTable.objects.filter(class_number=classnumber)
                return render(request, 'ancient/student_home_cs.html', {'classchoose': classchoose, 'user': request.user, 'classrender': classrender})  # the class the user has chosen
            else:
                return redirect('/login')
        else:
            return redirect('/admin')
    else:
        return redirect('/login')


def student_home_cc(request):
    if request.user.is_authenticated():
        identity = Identity.objects.filter(name=request.user)
        if(len(identity) is not 0):
            if identity[0].identity == identity[0].STUDENT: #
                classchoose = ClassChoose.objects.filter(student=request.user)
                classchooseid = classchoose.values_list('class_number', flat=True)
                classnotchoose = ClassTable.objects.exclude(pk__in=set(classchooseid))
                return render(request, 'ancient/student_home_cc.html',{'classchoose': classchoose, 'user':request.user, 'classnotchoose':classnotchoose})
            else:
                return redirect('/login')
        else:
            return redirect('/login')
    else:
        return redirect('/login')


def student_home_cc_confirm(request, classnumber):
    if request.user.is_authenticated():
        identity = Identity.objects.filter(name=request.user)
        if(len(identity) is not 0):
            if identity[0].identity == identity[0].STUDENT: #
                classchoose = ClassChoose.objects.filter(student=request.user).values_list('class_number', flat=True)
                classtbchoose = ClassTable.objects.filter(class_number=classnumber)
                if len(classtbchoose) > 0 and not (classtbchoose[0] in classchoose):
                    ClassChoose.objects.create(student=request.user, class_number=classtbchoose[0])
                    messages.info(request, "选课成功！")
                    return redirect('student_home_cc')
                else:
                    messages.info(request, "选课失败！")
    return redirect('student_home_cc')


def student_course_main(request, classnumber):  #class page
    if request.user.is_authenticated():
        identity = Identity.objects.filter(name=request.user)
        if(len(identity) is not 0):
            if identity[0].identity == identity[0].STUDENT: #
                classrender = ClassTable.objects.filter(class_number=classnumber)
                homeworkrender = Homework.objects.filter(class_number = classrender[0]).order_by('homework_number')
                return render(request, 'ancient/student_course_main.html', {'homeworkrender': homeworkrender, 'user': request.user, 'classrender': classrender[0]})  # the class the user has chosen
            else:
                return redirect('/login')
        else:
            return redirect('/admin')
    else:
        return redirect('/login')


def student_course_hw(request, classnumber, homeworknumber):  #
    if request.user.is_authenticated():
        identity = Identity.objects.filter(name=request.user)
        if(len(identity) is not 0):
            if identity[0].identity == identity[0].STUDENT: #
                classrender = ClassTable.objects.filter(class_number=classnumber)
                homeworkrender = Homework.objects.filter(class_number=classrender[0]).order_by('homework_number')
                homeworkcontent = Homework.objects.filter(homework_number=homeworknumber, class_number=classrender[0])
                return render(request, 'ancient/student_course_hw.html', {'homeworkrender': homeworkrender, 'user': request.user, 'classrender': classrender[0], 'content':homeworkcontent})  # the class the user has chosen
            else:
                return redirect('/login')
        else:
            return redirect('/admin')
    else:
        return redirect('/login')


def teacher_home_ct(request, classnumber):  #
    if request.user.is_authenticated():
        identity = Identity.objects.filter(name=request.user)
        if(len(identity) is not 0):
            if identity[0].identity == identity[0].TEACHER: #
                classteaching = ClassTable.objects.filter(teacher=request.user)
                classrender = ClassTable.objects.filter(class_number=classnumber).order_by('class_number')
                return render(request, 'ancient/teacher_home_ct.html', { 'user': request.user, 'classrender': classrender, 'classteaching': classteaching})  # the class the user has chosen
            else:
                return redirect('/login')
        else:
            return redirect('/admin')
    else:
        return redirect('/login')


def teacher_course_main(request, classnumber):  #
    if request.user.is_authenticated():
        identity = Identity.objects.filter(name=request.user)
        if(len(identity) is not 0):
            if identity[0].identity == identity[0].TEACHER: #
                classrender = ClassTable.objects.filter(class_number=classnumber)
                homeworkrender = Homework.objects.filter(class_number=classrender[0]).order_by('homework_number')
                return render(request, 'ancient/teacher_course_main.html', {'homeworkrender': homeworkrender, 'user': request.user, 'classrender': classrender[0]})  # the class the user has chosen
            else:
                return redirect('/login')
        else:
            return redirect('/admin')
    else:
        return redirect('/login')


def teacher_course_hw(request, classnumber, homeworknumber):  #
    if request.user.is_authenticated():
        identity = Identity.objects.filter(name=request.user)
        if(len(identity) is not 0):
            if identity[0].identity == identity[0].TEACHER: #
                classrender = ClassTable.objects.filter(class_number=classnumber)
                homeworkrender = Homework.objects.filter(class_number=classrender[0]).order_by('homework_number')
                homeworkcontent = Homework.objects.filter(homework_number=homeworknumber, class_number=classrender[0])
                return render(request, 'ancient/teacher_course_hw.html', {'homeworkrender': homeworkrender, 'user': request.user, 'classrender': classrender[0], 'content':homeworkcontent})  # the class the user has chosen
            else:
                return redirect('/login')
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

'''
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
'''