from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

''' Rappresenta le tabelle SQL sotto forma di classe '''
class City(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name.capitalize()

class University(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    place = models.ForeignKey(to=City, on_delete=models.CASCADE)
    class Meta:
        unique_together = (('name', 'place'),)

    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'

    def __str__(self):
        return self.name.capitalize()

class Faculty(models.Model):
    university = models.ForeignKey(to=University, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return ', '.join([self.name.capitalize(), self.university.name.__str__()])


class Course(models.Model):
    faculty = models.ForeignKey(to=Faculty, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=60, null=False, blank=False)
    duration = models.IntegerField(validators=[MinValueValidator(3), MaxValueValidator(5)])

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        unique_together = (('faculty','name'),)


    def __str__(self):
        return ', '.join([self.name.capitalize(), self.faculty.name.capitalize()])

class Student(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='user')

    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, null=True, blank=True)
    university = models.ForeignKey(to=University, on_delete=models.CASCADE, related_name='university', null=True, blank=True)

    studentID = models.CharField(max_length=10, blank=False, null=False)
    member_since = models.IntegerField(null=True, blank=True)
    bio = models.TextField(max_length=280, null=True, blank=True)


    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.user.username + ', ' + str(self.studentID)

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=140, null=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name.capitalize()


class Subject(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)

    def __str__(self):
        return ', '.join([self.name.capitalize(), self.course.name.capitalize()])

    class Meta:
        unique_together = (('name','course'),)
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

class Exam(models.Model):
    student = models.ForeignKey(to=Student, on_delete=models.CASCADE, related_name='studente')
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE)
    passed = models.BooleanField(default=False)
    date_passed = models.DateField(null=True, blank=True)
    grade = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(31)], null=True, blank=True)

    class Meta:
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'


    def __str__(self):
        return ', '.join([self.student.user.username.capitalize(), self.subject.name.capitalize()])


class Post(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.ManyToManyField(to=Category)
    title = models.CharField(max_length=40)
    body = models.TextField()
    date_created = models.DateTimeField(null=False, blank=False, default='')
    visible = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        unique_together = ('author', 'title')

    def __str__(self):
        return self.author.username.capitalize() + ', ' + self.title.capitalize()
class Comment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE)
    body = models.TextField()
    date_created = models.DateTimeField(null=False, blank=False, default='')
    visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return ', '.join([self.author.username.capitalize(), self.post.title.capitalize(), self.body[:20] + '...' if len(self.body) > 20 else self.body])