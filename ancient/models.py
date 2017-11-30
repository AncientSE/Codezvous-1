from django.db import models

# Create your models here.
from django.utils import timezone


class Submit(models.Model):  # Homework Submitted
    student = models.ForeignKey('auth.User')
    class_number = models.CharField(max_length=200)
    homework_number = models.CharField(max_length=200)
    submit_content = models.TextField()
    submit_time = models.DateTimeField(
            blank=True, null=True)


    def publish(self):
        self.submit_time = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Identity(models.Model):   # specify teacher or a student
    TEACHER = 'TE'
    STUDENT = 'ST'
    IDENTITY_CHOICES = (
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    )
    name = models.ForeignKey('auth.User')
    identity = models.CharField(max_length=2, choices=IDENTITY_CHOICES, default=STUDENT)

    def set_name(self, name):
        self.name = name

    def is_a_student(self):   # FIX THIS BUG DOES NOT RETURN TRUE WHEN IDENTITY IS STUDENT
        return self.identity == self.STUDENT

    def __str__(self): # find a better one
        return self.identity


class ClassTable(models.Model):  # Class
    class_number = models.CharField(max_length=200)
    teacher = models.ForeignKey('auth.User')
    class_name = models.CharField(max_length=200)
    class_content = models.TextField()

    def __str__(self):
        return self.class_name


class ClassChoose(models.Model): #class choosen
    class_number = models.CharField(max_length=200)
    student = models.ForeignKey('auth.User')

    def __str__(self):  # find a better one
        return self.class_number


class Homework(models.Model):  # teacher gave out
    student = models.ForeignKey('auth.User')
    homework_number = models.CharField(max_length=200)
    homework_content = models.TextField()
    homework_deadline = models.DateTimeField(
            blank=True, null=True)

    def __str__(self):
        return self.student


