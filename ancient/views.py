from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.utils import timezone
from .models import Submit, Identity, ClassChoose, ClassTable, Homework,newuser, EmailVerifyRecord
from .forms import UserForm, SubmitForm, IdentityForm, loginForm
from django.contrib.auth.views import logout
from django.http import HttpResponse
from django.contrib import messages
import os
from ancient.utils.email_send import send_register_email
from django.template import RequestContext
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
                homeworkcontent = Homework.objects.filter(homework_number=homeworknumber, class_number=classnumber)

                # specify if the method is POST?
                if (request.method == 'POST'):
                    file = request.FILES['file']
                    fileName = 'code_'+ str(timezone.now())

                    # upload file dir
                    path = os.path.join('./UserUpload/', str(request.user), str(classnumber), str(homeworknumber)) +'/'
                    print('  '+path)
                    if not os.path.exists(path):
                        os.makedirs(path)
                    with open(path + fileName, 'wb+') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)

                    # operating model: Submit

                    submitInfo = Submit()
                    submitInfo.student_id = request.user.id
                    submitInfo.class_number = classnumber
                    submitInfo.homework_number = homeworknumber
                    submitInfo.file_name = fileName
                    submitInfo.file_dir = path + fileName
                    submitInfo.submit_time = timezone.now()
                    submitInfo.save()





                ##


                # file submit area config

                print("    SubmitUserName: "+str(request.user))



                ##


                homeworkInfo = Submit.objects.filter(class_number=classnumber, homework_number = homeworknumber)

                for s_homeworkInfo in homeworkInfo:
                    hwContent = open(s_homeworkInfo.file_dir)
                    s_homeworkInfo.content = hwContent.read(120)

                data = {
                    'homeworkrender': homeworkrender,
                    'user': request.user,
                    'classrender': classrender[0],
                    'contents':homeworkcontent,
                    'hwInfo':homeworkInfo,
                    'hwId':str(homeworknumber),
                }


                return render(request, 'ancient/student_course_hw.html', data)  # the class the user has chosen
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


'''
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
            password_test=form_user.cleaned_data['password_test']
            email = form_user.cleaned_data['email']
            context={
                'form_user': 'form_user',
                'form_identity': 'form_identity'
            }
            error_password = "two password is not equal!"
            error_username = "this name has been registered!"
            error_email = "this email has been registered!"
            if password != password_test:
                context['msg']=error_password
                return render(request, self.template_name, context)
            if len(newuser.objects.filter(username=username))>0:
                context['msg']=error_username
                return render(request, self.template_name, context)
            if len(newuser.objects.filter(email=email))>0:
                context['msg'] = error_email
                return render(request, self.template_name, context)
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password,)
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
def register(request):
    error_password = "two password is not equal!"
    error_username = "this name has been registered!"
    error_email = "this email has been registered!"
    template_name = 'ancient/register.html'
    context = {
        'form_user': UserForm,
        'form_identity': IdentityForm
    }

    if request.method == 'GET':
        form_user = UserForm
        form_identity = IdentityForm
        return render(request, template_name,{'form_user': form_user, 'form_identity': form_identity})
    if request.method == 'POST':
        form_user = UserForm(request.POST)
        form_identity = IdentityForm(request.POST)
        context = {
            'form_user': form_user,
            'form_identity': form_identity
        }
        if form_user.is_valid() and form_identity.is_valid():
            username=form_user.cleaned_data['username']
            email = form_user.cleaned_data['email']
            password = form_user.cleaned_data['password']
            password_test = form_user.cleaned_data['password_test']
            identity=form_identity.cleaned_data['identity']
            User_filter_result = newuser.objects.filter(username=username)
            Email_filter_result = newuser.objects.filter(email=email)
            if len(User_filter_result) > 0:
                context['msg'] = error_username
                return render(request,template_name,context)
            elif len(Email_filter_result) > 0:
                context['msg'] = error_email
                return render(request,template_name,context)
            elif password != password_test:
                context['msg'] = error_password
                return render(request,template_name,context)
            else:
                send_register_email(email, "register")
                newuser.objects.create_user(username=username,email=email,password=password,is_active=False)
                user=newuser.objects.get(username=username)
                user.save()
                Identity.objects.create(name=user,identity=identity)
                return redirect('homepage')
        else:
            return render(request,template_name,context)


def log_in(request):
    template_name='ancient/login.html'
    context = {
        'form': loginForm,
    }
    if request.method == 'GET':
        return render(request,template_name, context)
    if request.method == 'POST':
        form=loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                if user.is_active == False:
                    context['msg']=u"用户还未激活，请到邮箱中进行验证！"
                    return render(request, template_name, context)
                login(request, user)
                return redirect('homepage')
            else:
                context['msg']="password or username is not correct!"
                return render(request,template_name,context)
        else:
            return render(request,template_name,context)

class ActiveUserView(View):
    """账户激活的View"""
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = newuser.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            # active_fail.html在templates中新建的一个文件body中就一个<p>链接失效!</p>
            return render(request, "ancient/active_fail.html", {})
        return render(request,"ancient/active_success.html",{})



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