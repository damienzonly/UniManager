from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.views import access_or_redirect
from app.models import *
from django.http import Http404
from django.core.paginator import Paginator


def index(request):
    return access_or_redirect(request, 'layout/home_layout.html', None, 'dashboard')


@login_required
def dashboard(request):
    try:
        student = Student.objects.get(user__username=request.user.username)
    except Student.DoesNotExist:
        return redirect('logout')
    return render(request, 'dashboard.html', {'student':student})

def search_user(request):
    getQuery = request.GET.get('ricerca', '')
    if getQuery == '': return redirect('dashboard')
    data = User.objects.filter(username__icontains=getQuery).order_by('username')
    posts = Post.objects.filter(author__username__icontains=getQuery, visible=True)
    return render(request, 'search.html', {'users': data, 'query': 'search-user', 'posts':posts})

def search_title(request):
    getQuery = request.GET.get('ricerca', '')
    if getQuery == '': return redirect('dashboard')
    data = Post.objects.filter(title__icontains=getQuery).order_by('author__username')
    return render(request, 'search.html', {'posts': data, 'query': 'search-title'})

def search_content(request):
    getQuery = request.GET.get('ricerca', '')
    if getQuery == '': return redirect('dashboard')
    data = Post.objects.filter(body__icontains=getQuery).order_by('author__username')
    return render(request, 'search.html', {'posts': data, 'query': 'search-content'})

def search_category(request):
    getQuery = request.GET.get('ricerca', '')
    if getQuery == '': return redirect('dashboard')
    data = Post.objects.filter(category__name__icontains=getQuery).order_by('-date_created')
    return render(request, 'search.html', {'posts': data, 'query': 'search-category'})

@login_required
def exams(request):
    from app.models import Course
    display = Course.objects.filter(student__user__username=request.user).exists()

    if request.method == 'POST':
        from app.forms import ExamForm
        from app.models import Student, Subject, Exam, Course
        form = ExamForm(request.POST)
        if form.is_valid():

            sameCourse = Course.objects.get(student__user__username=request.user)
            sameStudent = Student.objects.get(user__username=request.user)
            sent_subject = request.POST['new_subject'].capitalize()
            newSubject, created = Subject.objects.get_or_create(name=sent_subject, course=sameCourse)
            if created:
                newSubject.save()
            newGrade = request.POST['grade'] or None
            newPassed = request.POST.get('passed', '') == 'on'
            newDate = request.POST['date_passed'] or None

            newExam = Exam(
                student=sameStudent,
                subject=newSubject,
                grade=newGrade,
                passed=newPassed,
                date_passed=newDate,
            )

            newExam.save()
            return render(request, 'exams/exams.html', {
                'msg': 'Exam Succesfully Added',
                'newExamForm': ExamForm(),
                'exams': Exam.objects.filter(student__user__username=request.user),
                'display': display
            })
        else:
            return render(request, 'exams/exams.html', {
                'err': 'Invalid data',
                'newExamForm': form,
                'exams': Exam.objects.filter(student__user__username=request.user),
                'display': display
            })

    from app.models import Exam
    from app.forms import ExamForm

    exams = Exam.objects.filter(student__user__username=request.user)

    return render(request, 'exams/exams.html', {
        'exams': exams,
        'request': request,
        'newExamForm': ExamForm(),
        'display': display
    })


@login_required
def profile(request):
    from django import forms

    Quser = Student.objects.get(user__username=request.user)

    class UniversityInfoForm(forms.Form):

        # universita
        university_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))

        # universita e city
        city = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'class': 'form-control'}))

        # universita e facolta
        faculty_name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'form-control'}))

        # facolta e corso
        course_name = forms.CharField(max_length=60, widget=forms.TextInput(attrs={'class': 'form-control'}))
        course_length = forms.IntegerField(validators=[MinValueValidator(3), MaxValueValidator(5)], widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Course length (years)')

    class ProfileInfoForm(forms.Form):
        # bio
        bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
        student_id = forms.CharField(max_length=10, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Student ID')
        member_since = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Member since (year)')

    class UserInfoForm(forms.ModelForm):

        class Meta:
            model = User
            fields = ['email', 'first_name', 'last_name']
            widgets = {
                'email': forms.TextInput(attrs={'class': 'form-control'}),
                'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            }

    if request.method == 'POST':
        form = UniversityInfoForm(request.POST)
        formBio = ProfileInfoForm(request.POST)
        if form.is_valid():
            nome_universita = form.cleaned_data['university_name'].lower()
            citta = form.cleaned_data['city'].lower()
            nome_facolta = form.cleaned_data['faculty_name'].lower()
            nome_corso = form.cleaned_data['course_name'].lower()
            durata_corso = form.cleaned_data['course_length']

            nome_universita_db = University.objects.filter(name=nome_universita)
            citta_db = City.objects.filter(name=citta)
            nome_facolta_db = Faculty.objects.filter(name=nome_facolta)
            nome_corso_db = Course.objects.filter(name=nome_corso)

            nome_universita_exists = nome_universita_db.exists()
            citta_exists = citta_db.exists()
            nome_facolta_exists = nome_facolta_db.exists()
            nome_corso_exists = nome_corso_db.exists()

            if not citta_exists:
                newCitta = City(name=citta)
                newCitta.save()
            else:
                newCitta = citta_db[0]

            if not nome_universita_exists:
                newUniversity = University(name=nome_universita, place=newCitta)
                newUniversity.save()
            else:
                newUniversity = nome_universita_db[0]

            if not nome_facolta_exists:
                newFaculty = Faculty(university=newUniversity, name=nome_facolta)
                newFaculty.save()
            else:
                newFaculty = nome_facolta_db[0]

            if not nome_corso_exists:
                newCorso = Course(faculty=newFaculty, name=nome_corso, duration=durata_corso)
                newCorso.save()
            else:
                newCorso = nome_corso_db[0]

            Quser.course = newCorso
            Quser.university = newUniversity

            Quser.save()

        if formBio.is_valid():
            newStudenteID = formBio.cleaned_data['student_id']
            member_since = formBio.cleaned_data['member_since']
            newBio = formBio.cleaned_data['bio'].capitalize()

            student = Student.objects.get(user__username=request.user)

            student.studentID = newStudenteID
            student.member_since = member_since
            student.bio = newBio
            student.save()

    return render(request, 'profile/profile.html', {'form': UniversityInfoForm(), 'formBio': ProfileInfoForm(), 'user': User.objects.get(username=request.user), 'student': Student.objects.get(user__username=request.user)})


@login_required
def edit_exam(request, id):
    from app.forms import EditExamForm, ExamForm
    try:
        user = User.objects.get(username=request.user)
    except:
        raise Http404('Invalid User')
    try:
        exam = Exam.objects.get(id=id, student__user__username=request.user)
    except:
        raise Http404('Invalid Exam')

    if request.method == 'POST':
        newGrade = request.POST['grade'] or None
        newPassed = request.POST.get('passed', '') == 'on'
        newDatePassed = request.POST['date_passed'] or None

        if newGrade and newDatePassed:
            exam.grade = newGrade
            if newPassed:
                exam.date_passed = newDatePassed
                exam.passed = newPassed
            else:
                exam.date_passed = None
                exam.grade = None
                exam.passed = False
            exam.save()
        else:
            exam.date_passed = None
            exam.grade = None
            exam.passed = False
            exam.save()

        return redirect('exams')
    return render(request, 'exams/edit_exam.html', {'form': EditExamForm(), 'exam': exam, 'request': request, 'user': user, 'student': Student.objects.get(user__username=request.user)})


@login_required
def delete_exam(request, id):
    try:
        user = User.objects.get(username=request.user)
    except:
        raise Http404('Invalid User')
    try:
        exam = Exam.objects.get(id=id, student__user__username=request.user)
    except:
        raise Http404('Invalid Exam')

    if request.method == 'POST':
        name = exam.subject.name
        exam.delete()
        return redirect('exams')

    return render(request, 'exams/delete_exam.html', {'exam': exam})


def _create_category(categories, post):
    for cat_item in categories:
        catQuery, categ_createdNow = Category.objects.get_or_create(name=cat_item.lower().strip())
        if not post.category.filter(post__category=catQuery).exists():
            post.category.add(catQuery)
            post.save()
    return post


@login_required
def create_post(request):
    from app.forms import CreatePostForm
    if request.method == 'POST':
        title = request.POST.get('title', '').strip() or None
        body = request.POST.get('body', '').strip() or None
        categories = request.POST.get('categories', '') or None

        if all([title, body, categories]):
            from datetime import datetime
            try:
                newPost = Post.objects.create(author_id=request.user.id, title=title, body=body, date_created=datetime.now(), visible=True)
            except:
                return render(request, 'posts/create_post.html', {'form': CreatePostForm(), 'err': 'You already used this title'})
            categories = [item.lower().strip() for item in categories.split(',')]
            _create_category(categories, newPost)
            return redirect('display_post')
        else:
            return create_post(request)

    return render(request, 'posts/create_post.html', {'form': CreatePostForm()})


@login_required
def display_posts(request, msg=None, err=None):
    userPosts = Post.objects.filter(author__username=request.user.username, visible=True).order_by('-date_created')
    paginatorObject = Paginator(userPosts, 2)

    page = request.GET.get('page', '1')
    filtered_posts_list = paginatorObject.get_page(page)
    return render(request, 'posts/display_posts.html', {'posts': filtered_posts_list, 'count': filtered_posts_list.__len__(), 'page': page, 'msg':msg, 'err':err})


def get_post(request, id):
    try:
        requested_post = Post.objects.get(id=id, visible=True)
        comments_related = Comment.objects.filter(post=requested_post)
        comment_count = comments_related.count()
        categories = requested_post.category.all()
        return render(request, 'posts/get_post.html', {'auth': False, 'post': requested_post, 'comments':comments_related, 'user': requested_post.author, 'request':request, 'comment_count':comment_count, 'categories': categories})
    except Post.DoesNotExist:
        return render(request, 'posts/get_post.html', {'err':'Couldn\'t get requested post'})




@login_required
def edit_post(request, id):
    from app.forms import EditPostForm
    if request.method == 'GET':
        try:
            postQuery = Post.objects.get(author__username=request.user.username, id=id, visible=True)
        except Post.DoesNotExist:
            return display_posts(request, err='Couldn\'t get post requested')
        categories = Category.objects.filter(post=postQuery)
        categories_pylist = [category.name.lower() for category in categories]
        categories_pylist = ', '.join(categories_pylist)
        return render(request, 'posts/edit_post.html', {'post':postQuery,'categories':categories_pylist, 'form': EditPostForm()})
    else:
        # da cambiare alla posts page con messaggio
        from app.forms import EditPostForm

        body = request.POST.get('body', '')
        categories = request.POST.get('categories', '')

        try:
            postQuery = Post.objects.get(author__username=request.user.username, id=id)
        except Post.DoesNotExist:
            raise Http404('Cannot edit this post')

        postQuery.body = body
        _create_category(categories.split(','), postQuery)

        return redirect('display_post')

@login_required
def delete_post(request, id):
    try:
        post = Post.objects.get(author__username=request.user.username, id=id, visible=True)
    except Post.DoesNotExist:
        raise Http404('Post not found')

    if request.method == 'POST':
        # elimina post
        post.visible = False
        post.save()
        return redirect('display_post')

    return render(request, 'posts/delete_post.html', {'post':post})

def comment_post(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        raise Http404('Post not found')

    if request.method == 'POST':
        # crea il commento
        from datetime import datetime
        body = request.POST.get('body', '')
        if body:
            newComment = Comment(
                author_id=request.user.id,
                post=post,
                body=body,
                date_created=datetime.now(),
                visible=True
            )
            newComment.save()
        return redirect('get_post', id=post.id)

    return render(request, 'comments/comment_post.html', {'post':post})


@login_required
def delete_comment(request, id):

    try:
        comment = Comment.objects.get(author__username=request.user.username, id=id)
    except Comment.DoesNotExist:
        raise Http404('Comment not found')

    if request.method == 'POST':
        comment.delete()
        return redirect('get_post', id=comment.post.id)

    return render(request, 'comments/delete_comment.html', {'comment':comment, 'post':comment.post })



def profile_posts(request, username):
    try:
        user = User.objects.get(username=username, is_active=True)
    except Student.DoesNotExist:
        raise Http404('User not found')

    user_posts = Post.objects.filter(author_id=user.id, visible=True)
    return render(request, 'profile/profile_posts.html', {
        'user':user,
        'posts':user_posts
    })


@login_required
def profile_info(request, username):
    try:
        user = User.objects.get(username=username)
        student = Student.objects.get(user=user)
    except Student.DoesNotExist:
        raise Http404('User not found')
    posts = Post.objects.filter(author__username=username, visible=True).order_by('-date_created')[:5]
    return render(request, 'profile/profile_info.html', {'user':user, 'posts':posts, 'student': student})

    # return render(request, 'posts')





