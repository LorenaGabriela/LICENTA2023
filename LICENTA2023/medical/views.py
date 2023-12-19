from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth, AbstractUser
from .forms import  UploadFileForm
from .models import UploadedFile
from .skin_detector import predict_image_class, m


def home(request):
    return render(request, 'medical/home.html')

def register_pacient(request):
    if request.method == 'POST':
        username = request.POST['username']
        nume_pacient = request.POST['nume_pacient']
        prenume_pacient = request.POST['prenume_pacient']
        email = request.POST['email_pacient']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Contul exista deja!')
                return redirect(register_pacient)
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=nume_pacient,last_name=prenume_pacient)
                user.set_password(password)
                user.save()
                print('succes')
                return redirect('home')
    else:
        print('this is not post method')
        return render(request, 'medical/register_pacient.html')

def login_pacient(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('upload_photo_pacient.html')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login_pacient.html')
    else:
        return render(request, 'medical/login_pacient.html')


@login_required
def upload_photo_pacient(request):
    diagnostic = None
    uploaded_file = None
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.save()

            # Afiseaza calea către fișier în consolă
            # print("Calea către fișier:", uploaded_file.file.path)
            diagnostic = predict_image_class(uploaded_file, m)
            print("Diagnosticul este " + diagnostic)
            # return redirect('upload_photo_pacient.html')  # înlocuiți 'pagina_de_destinatie' cu pagina dorită
            return render(request, 'medical/upload_photo_pacient.html', {'form': form,'diagnostic': diagnostic, 'uploaded_file': uploaded_file} )

    return render(request, 'medical/upload_photo_pacient.html', {'form': form,'diagnostic': diagnostic, 'uploaded_file': uploaded_file})
