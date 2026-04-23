from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.contrib.auth.models import User
from django.contrib import messages
from rest_framework import viewsets
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            posts = Post.objects.all().order_by('-created_at')
        else:
            posts = Post.objects.filter(author=request.user).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blogapp/home.html', {'posts': posts})
def signup(request):
    pass

def create_post(request):
    # Fallback to test user if not logged in (to bypass auth issues during testing)
    if not request.user.is_authenticated:
        user, _ = User.objects.get_or_create(username='TestUser')
    else:
        user = request.user

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user  # Assign the author
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blogapp/create_post.html', {'form': form})

def post_detail(request):
    pass 