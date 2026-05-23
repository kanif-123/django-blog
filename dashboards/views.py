# from unicodedata import category

from django.shortcuts import get_object_or_404, redirect, render
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required
from .forms import AddUserForm, BlogPostForm, CategoryForm, EditUserForm
from django.utils.text import slugify
from django.contrib.auth.models import User
from .models import ExcelDocument
import os  # <-- Ye add karein file delete karne ke liye

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    category_count= Category.objects.all().count()
    blogs_count= Blog.objects.all().count()

    context ={
        'category_count':category_count,
        'blogs_count':blogs_count,
    }
    return render(request, 'dashboard/dashboard.html', context)

def categories(request):
    return render(request, 'dashboard/categories.html') 


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('categories')
    form = CategoryForm()
    context= {
        'form' : form,
    }
    return render(request, 'dashboard/add_category.html', context)


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categories')
    form = CategoryForm(instance=category)
    context = {
        'form' : form,
        'category' : category,
    }
    return render(request, 'dashboard/edit_category.html', context)

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('categories')

def posts(request):
    posts = Blog.objects.all()
    context= {
        'posts' : posts,
    }
    return render (request, 'dashboard/posts.html', context)

def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) # temprary saving the form
            post.author = request.user
            post.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-'+str(post.id)
            post.save()
            return redirect('posts')
    form = BlogPostForm()
    context= {
        'form': form,
    }

    return render(request, 'dashboard/add_post.html', context)


def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-'+str(post.id)
            post.save()
            return redirect('posts')

    form = BlogPostForm(instance=post)
    context = {
        'form' : form,
        'post' : post,
    }
    return render(request, 'dashboard/edit_post.html', context)


def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('posts')



# users 
def users(request):
    users = User.objects.all()
    context = {
        'users' : users,
    }
    return render(request, 'dashboard/users.html', context)


def add_user(request):   # View function to handle adding a new user
   
    if request.method == 'POST':       # Check if the request method is POST (form submission)
        
        form = AddUserForm(request.POST)        # Create form instance with submitted POST data
        
        if form.is_valid():         # Check if form data passes validation rules
            
            form.save()             # Save the validated user data into the database

            return redirect('users')             # Redirect to 'users' page after successful save

    else:    # If request method is not POST (means GET request)

        form = AddUserForm()         # Create an empty form to display on page load

    # form = AddUserForm() anoter comment

    context = {             # Attach form (empty or with errors) to context
        'form' : form,
    }

    return render(request, 'dashboard/add_user.html', context)

# edit user

def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    form = EditUserForm(instance=user)
    context = {
        'form' : form,
    }
    return render(request, 'dashboard/edit_user.html', context)

# delete user

def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('users')


# upload excel file

def upload_excel(request):
    if request.method == 'POST':
        # form se multiple files nikalne ke liye getlist() use karte hain
        files = request.FILES.getlist('excel_files')
        
        for f in files:
            ExcelDocument.objects.create(file=f)
            
        return redirect('download_excel')
        
    return render(request, 'dashboard/upload_excel.html') # Template ka rasta dhyan se dekhein

def download_excel(request):
    files = ExcelDocument.objects.all().order_by('-uploaded_at')
    return render(request, 'dashboard/download_excel.html', {'files': files})

# delete function 
def delete_excel(request, pk):
    # File ko database se dhoondhein
    document = get_object_or_404(ExcelDocument, pk=pk)
    
    # Server ke storage (media folder) se actual file ko delete karein
    if document.file:
        if os.path.isfile(document.file.path):
            os.remove(document.file.path)
            
    # Database se record delete karein
    document.delete()
    
    # Delete hone ke baad wapas download list par bhej dein
    return redirect('download_excel')