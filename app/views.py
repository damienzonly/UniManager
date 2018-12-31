from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login, authenticate as django_authenticate, logout as django_logout
from app.models import Student

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        queryUser = django_authenticate(username=username, password=password)

        if queryUser is not None:
            django_login(request, user=queryUser)
            return redirect('dashboard')
        else:
            return render(request, 'auth/login.html', {
                'username': username,
                'msg': 'Invalid Credentials',
                'request': request
            })

    else:
        return access_or_redirect(request, 'layout/home_layout.html', {'request': request}, 'dashboard')


@login_required
def logout(request):
    django_logout(request)
    return redirect('index')

def signup(request):

    if request.method == 'GET':
        return access_or_redirect(request, 'auth/signup.html', {'request': request}, 'dashboard')

    if request.method == 'POST':
        errs = []
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # Fill every field
        if not all([username, email, password]):
            errs.append('Fill every field, please')
            return render(request, 'auth/signup.html', {
                'username': username,
                'email': email,
                'password': password,
                'errs': errs,
                'reuest': request
            })

        # all fields covered
        else:
            # check if already exists
            email_exists = User.objects.filter(email=email).exists()
            username_exists = User.objects.filter(username=username).exists()
            if email_exists: error = 'Email already taken'
            elif username_exists: error = 'Username already taken'
            else:
                # Create new user
                newUser = User.objects.create_user(username=username, email=email)
                newUser.set_password(password)
                newUser.save()
                newStudent = Student(user=newUser)
                newStudent.save()
                django_login(request, user=newUser)
                return render(request, 'dashboard.html', {'request': request})


            return render(request, 'auth/signup.html', {
                'username': username,
                'email': email,
                'password': password,
                'errs': errs+[error],
                'request': request
            })


    return render(request, 'auth/signup.html', {'request': request})


def access_or_redirect(request, template, args, dest):
    if request.user.is_authenticated:
        return redirect(dest)
    else:
        return render(request, template, args)
