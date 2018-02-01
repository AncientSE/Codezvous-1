from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils import timezone
# Create your models here.


class newuser(AbstractUser):
    profile = models.CharField('profile', default='', max_length=256)
    def __str__(self):
        return self.username


class Submit(models.Model):  # Homework Submitted
    '''
    student_id = models.ForeignKey('auth.User')
    class_number = models.ForeignKey('ClassTable', null=True)  # actually class
    homework_number = models.ForeignKey('Homework', null=True)  # actually  homework


    submit_content = models.TextField()
    submit_time = models.DateTimeField(
            blank=True, null=True)
    '''

    student_id = models.CharField(max_length=128, default=None)
    class_number = models.CharField(max_length=128, default=None)
    homework_number = models.CharField(max_length=128, default=None)

    # file address
    file_dir = models.FilePathField(name=None, default='./NoAddress')
    ##

    # file name
    file_name = models.CharField(max_length=128, default='No Name')

    ##
    submit_time = models.DateTimeField(
        blank=True, null=True)

    #  added 2018\01\29 by Tiankuang
    score = models.CharField(max_length=10, default="Not Run yet")
    #  add end Tiankuang

    def publish(self):
        self.submit_time = timezone.now()
        self.save()

    def __str__(self):
        return str(self.student_id)


class Identity(models.Model):   # specify teacher or a student
    TEACHER = 'TE'
    STUDENT = 'ST'
    IDENTITY_CHOICES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    )
    name = models.ForeignKey('ancient.newuser')
    identity = models.CharField(max_length=2, choices=IDENTITY_CHOICES, default=STUDENT)

    def set_name(self, name):
        self.name = name

    def is_a_student(self):   # FIX THIS BUG DOES NOT RETURN TRUE WHEN IDENTITY IS STUDENT
        return self.identity == self.STUDENT

    def __str__(self): # find a better one
        return str(self.name)


class ClassTable(models.Model):  # Class
    class_number = models.PositiveSmallIntegerField(unique=True)
    teacher = models.ForeignKey('ancient.newuser')
    class_name = models.CharField(max_length=200)
    class_content = models.TextField()

    def __str__(self):
        return self.class_name


class ClassChoose(models.Model): #class choosen
    class_number = models.ForeignKey('ClassTable', null=True)
    student = models.ForeignKey('ancient.newuser')

    def __str__(self):  # find a better one
        return str(self.student) + str(self.class_number)


class Homework(models.Model):  # teacher gave out
    class_number = models.ForeignKey('ClassTable', null=True, on_delete=models.CASCADE)   #reference to the class table
    homework_number = models.PositiveSmallIntegerField()  # try to bind with the teacher name
    homework_content = models.TextField()
    #test_input = models.FilePathField(name=None, default='./NoAddress')
    #test_output = models.FilePathField(name=None, default='./NoAddress')
    test_input= models.TextField()
    test_output=models.TextField()
    homework_deadline = models.DateTimeField(
            blank=True, null=True)

    def __str__(self):
        return str(self.class_number) + str(self.homework_number)


class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name=u"验证码类型", max_length=10, choices=(("register",u"注册"), ("forget",u"找回密码")))
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)
    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)




