from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from .models import UserProfile

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            mobile_number = form.cleaned_data['mobile_number']
            email = form.cleaned_data['email']
            face_image = form.cleaned_data['face_image']
            
            # Créer le profil utilisateur
            profile = UserProfile.objects.create(
                user=user,
                mobile_number=mobile_number,
                email=email,
            )
            try:
                profile.save_face_encoding(face_image)
            except ValueError as e:
                form.add_error(None, str(e))
                user.delete()  # Supprimer l'utilisateur en cas d'erreur d'encodage
                return render(request, 'signup.html', {'form': form})

            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            face_image = form.cleaned_data['face_image']

            user = authenticate(request, username=username, password=password)
            if user:
                profile = UserProfile.objects.get(user=user)
                if profile.verify_face(face_image):
                    login(request, user)
                    return redirect('home')
                else:
                    form.add_error(None, "Reconnaissance faciale échouée.")
            else:
                form.add_error(None, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def home_view(request):
    return render(request, 'home.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def about_view(request):
    return render(request, 'about.html')
