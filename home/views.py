from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact, Profile, VerifyEmail, Preference
from blog.models import Post
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from notes.forms import *
from home.forms import *
from django.core.mail import send_mail
from django.conf import settings as conf_settings
from django.core.mail import EmailMessage
import uuid

import cv2,time
import numpy as np
from os import listdir
from os.path import join, isfile
# from blog.models import Post

# Create your views here.


def home(request):
    return render(request, 'home/home.html')
    # return HttpResponse("This is home")


def settings(request):
    current_user = request.user
    profiles = Profile.objects.filter(user=current_user)
    preference = Preference.objects.filter(user=current_user).first()
    form = PreferenceForm(instance=preference)
    if request.method == 'POST':
        form = PreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank You! Your Preferences has been Modified.')
            return redirect('../blog/bloghome')

    context = {'profiles': profiles, 'form': form, 'preference': preference}
    return render(request, 'home/settings.html', context)
    # return HttpResponse("This is home")

def userPreference(request):
    current_user = request.user
    profiles = Profile.objects.filter(user=current_user)
    preference = Preference.objects.filter(user=current_user).first()
    form = PreferenceForm(instance=preference)
    if request.method == 'POST':
        form = PreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank You! Your Preferences has been Saved.')
            return redirect('../')

    context = {'profiles': profiles, 'form':form, 'preference':preference}
    return render(request, 'home/userPreference.html', context)
    # return HttpResponse("This is home")


@login_required
def search(request):
    current_user = request.user
    profiles = Profile.objects.filter(user=current_user)
    query = request.GET['query']
    if len(query)>78:
        allPosts = []
        tasks = []
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsCategory = Post.objects.filter(Category__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent, allPostsCategory)
        tasksTitle = Task.objects.filter(title__icontains=query)
        tasksDesc = Task.objects.filter(desc__icontains=query)
        tasksCategory = Task.objects.filter(Category__icontains=query)
        tasks = tasksTitle.union(tasksDesc, tasksCategory)

    if allPosts.count() == 0 and tasks.count() == 0:
        messages.warning(request, 'No Search Result found. Plaese try again.')
    params={'allPosts':allPosts, 'query':query, 'tasks':tasks, 'profiles': profiles}
    return render(request, 'home/search.html', params)


@login_required
def about(request):
    current_user = request.user
    profiles = Profile.objects.filter(user=current_user)
    context = {'profiles': profiles}
    return render(request, 'home/about.html', context)
    # return HttpResponse("This is about")




@login_required
def contact(request):
    current_user = request.user
    profiles = Profile.objects.filter(user=current_user)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, 'Please fill the form correctly.')
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your Message has been successfully sent. Thank You..!!')
    context = {'profiles': profiles}
    return render(request, 'home/contact.html', context)
    # return HttpResponse("This is contact")



def checkUser(request):
    form = UserForm()
    error=""
    if request.method=="POST":
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u,password=p)
        if user is not None:
            login(request, user)
            error="yes"
        else:
            error="no"
    d={'error':error, 'form':form}
    return render(request,'home/checkUser.html',d)





def confirmUser(request):
    form = UserForm()
    error=""
    if request.method=="POST":
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u,password=p)
        if user.is_staff:
            data_path = 'D:/PROJECTS/checkk/Takebook/home/images/'
            onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]

            Training_Data, Labels = [], []

            for i, files in enumerate(onlyfiles):
                image_path = data_path + onlyfiles[i]
                images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                Training_Data.append(np.asarray(images, dtype=np.uint8))
                Labels.append(i)

            Labels = np.asarray(Labels, dtype=np.int32)

            model = cv2.face.LBPHFaceRecognizer_create()

            model.train(np.asarray(Training_Data), np.asarray(Labels))

            print("Model training Complete !!!!!")

            face_classifier = cv2.CascadeClassifier(
                'D:/PROJECTS/checkk/Takebook/home/haarcascade_frontalface_default.xml')

            def face_detector(img, size=0.5):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)

                if faces is ():
                    return img, []

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    roi = img[y:y + h, x:x + w]
                    roi = cv2.resize(roi, (200, 200))

                return img, roi

            cap = cv2.VideoCapture(0)
            while True:

                ret, frame = cap.read()

                image, face = face_detector(frame)

                try:
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    result = model.predict(face)

                    if result[1] < 500:
                        confidence = int(100 * (1 - (result[1]) / 300))

                    if confidence > 85:
                        login(request,user)
                        cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                        cv2.imshow('Face Cropper', image)
                        time.sleep(5)
                        error="yes"
                        break


                    else:
                        cv2.putText(image, "Can't Unlocked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                        cv2.imshow('Face Cropper', image)
                        time.sleep(5)
                        error="no"
                        break


                except:
                    cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow('Face Cropper', image)
                    time.sleep(5)
                    error="noface"
                    break

            cap.release()

            cv2.destroyAllWindows()

    d={'error':error, 'form':form}
    return render(request,'home/confirmUser.html',d)




def handlelogin(request):
    error=""
    if request.method=="POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        print(user)
        if user.is_staff:
            data_path = 'D:/PROJECTS/checkk/Takebook/home/images/'
            onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]

            Training_Data, Labels = [], []

            for i, files in enumerate(onlyfiles):
                image_path = data_path + onlyfiles[i]
                images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                Training_Data.append(np.asarray(images, dtype=np.uint8))
                Labels.append(i)

            Labels = np.asarray(Labels, dtype=np.int32)

            model = cv2.face.LBPHFaceRecognizer_create()

            model.train(np.asarray(Training_Data), np.asarray(Labels))

            print("Model training Complete !!!!!")

            face_classifier = cv2.CascadeClassifier(
                'D:/PROJECTS/checkk/Takebook/home/haarcascade_frontalface_default.xml')

            def face_detector(img, size=0.5):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, 1.3, 5)

                if faces is ():
                    return img, []

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
                    roi = img[y:y + h, x:x + w]
                    roi = cv2.resize(roi, (200, 200))

                return img, roi

            cap = cv2.VideoCapture(0)
            while True:

                ret, frame = cap.read()

                image, face = face_detector(frame)

                try:
                    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                    result = model.predict(face)

                    if result[1] < 500:
                        confidence = int(100 * (1 - (result[1]) / 300))

                    if confidence > 85:
                        login(request,user)
                        cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                        cv2.imshow('Face Cropper', image)
                        time.sleep(5)
                        error="yes"
                        break


                    else:
                        cv2.putText(image, "Can't Unlocked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                        cv2.imshow('Face Cropper', image)
                        time.sleep(5)
                        error="no"
                        break


                except:
                    cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.imshow('Face Cropper', image)
                    time.sleep(5)
                    error="noface"
                    break

            cap.release()

            cv2.destroyAllWindows()
    d={'error':error}
    return render(request,'home/signIn.html',d)



def signup(request):
    error = 'n'
    if request.method=="POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        a = request.POST['add']
        i = request.FILES['image']
        user = User.objects.create_superuser(username=u,password=p,email=e,first_name=f,last_name=l)
        Profile.objects.create(user=user,add=a,image=i)


        face_classifier = cv2.CascadeClassifier(
            'D:/PROJECTS/checkk/Takebook/home/haarcascade_frontalface_default.xml')

        def face_extractor(img):

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            if faces is ():
                return None

            for (x, y, w, h) in faces:
                cropped_faces = img[y:y + h, x:x + w]

            return cropped_faces

        cap = cv2.VideoCapture(0)
        count = 0

        while True:
            ret, frame = cap.read()
            if face_extractor(frame) is not None:
                count += 1
                face = cv2.resize(face_extractor(frame), (400, 400))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                file_name_path = 'D:/PROJECTS/checkk/Takebook/home/images/user' + str(count) + '.jpg'
                cv2.imwrite(file_name_path, face)

                cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Face Cropper', face)

            else:
                print("Face Not Found")
                pass

            if cv2.waitKey(1) == 13 or count == 100:
                break

        cap.release()
        cv2.destroyAllWindows()
        error = 'y'

        token = uuid.uuid4()
        verifyemail = VerifyEmail(customer=user, token=token, is_verified=False)
        verifyemail.save()
        print(request.META['HTTP_HOST'])
        subject = 'Account Verification'
        message = 'Welcome ' + u + '!\n\n Please Complete Your Registration By Clicking On The Link below \n\n\n\n\n' + request.scheme + ':' + '//' + \
                  request.META['HTTP_HOST'] + '/email/verify/' + str(token)
        email_from = conf_settings.EMAIL_HOST_USER
        recipient_list = [e, ]
        res = send_mail(subject, message, email_from, recipient_list)
        if res == 1:
            error = 'Yes'
        error = 'No'

    d = {'error':error}
    return render(request,'home/signup.html',d)

def verifyemail(request,token):
	users = VerifyEmail.objects.filter(token=token).update(is_verified=True)
	# users[0]
	print("user saved ")
	return HttpResponse('''<h2>Thank You! Your account has been successfully verified..!!</h2><br><h4>Click Here to go back to TakeBOOK App</h4><h4><a href="http://127.0.0.1:8000/">TakeBOOK</a></h4>''')
	# return HttpResponse("Thank You! Your account has been successfully verified..!!")


def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out! Sign In here to continue")
    return redirect('home')


@login_required
def profile(request):
    current_user = request.user
    profiles = Profile.objects.filter(user=current_user)
    user = User.objects.get(id=request.user.id)
    data = Profile.objects.get(user = user)
    context = {'data':data, 'user':user, 'profiles':profiles}
    return render(request, 'home/profile.html', context)


@login_required
def editProfile(request):
    current_user = request.user
    profiles = Profile.objects.filter(user=current_user)
    user = User.objects.get(id=request.user.id)
    data = Profile.objects.get(user = user)
    if request.method=='POST':
        f=request.POST['firstname']
        l=request.POST['lastname']
        e=request.POST['email']
        a=request.POST['add']
        user.first_name=f
        user.last_name=l
        user.email=e
        data.add=a
        if 'image' in request.FILES:
            data.image = request.FILES['image']
            data.save()
        user.save()
        data.save()
        messages.success(request, "Your Information has been Updated.!")
        return redirect('../profile')

    context = {'data':data, 'user':user, 'profiles':profiles}
    return render(request, 'home/editProfile.html', context)


@login_required
def changepassword(request):
    current_user = request.user
    profiles = Profile.objects.filter(user=current_user)
    if request.method=='POST':
        o=request.POST['old']
        n=request.POST['new']
        c=request.POST['confirm']
        if c==n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            messages.success(request, "Your Password has been Successfully Changed")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Check Again")

    context = {'profiles':profiles}
    return render(request, 'home/changepassword.html', context)


def base(request):
	current_user = request.user
	profiles = Profile.objects.filter(user=current_user)
	context = {'profiles': profiles}
	return render(request, 'base.html', context)












# def handlelogin(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         print(username)
#         print(password)
#         user = authenticate(username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             messages.success(
#                 request, "You have been successfully Logged In into your Account!S")
#             return redirect('../blog/bloghome')
#         else:
#             messages.error(
#                 request, "User already exist or Invalid Credentials, Please try again")
#             return redirect('../signIn')
#
#     return render(request, 'home/signIn.html')
#
#
# def handlelogout(request):
#     logout(request)
#     messages.success(request, "Successfully Logged Out! Sign In here to continue")
#     return redirect('../signIn')
#
#
# def signup(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         phone = request.POST['phone']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']
#
#         if len(username) > 10:
#             messages.error(request, "Phone Number must be of 10 digits.")
#             return redirect('../signup')
#
#         if len(phone) > 10:
#             messages.error(request, "Username must be under 10 characters.")
#             return redirect('../signup')
#
#         if not username.isalnum():
#             messages.error(
#                 request, "Username should only contain letters and number.")
#             return redirect('../signup')
#
#         if pass1 != pass2:
#             messages.error(request, "Password must be same.")
#             return redirect('../signup')
#
#         myuser = User.objects.create_user(username, email, pass1)
#         myuser.first_name = fname
#         myuser.last_name = lname
#         myuser.phone_number = phone
#         myuser.save()
#         messages.success(
#             request, "Welcome! Your account has been successfully created.")
#         return redirect('../signIn')
#     return render(request, 'home/signup.html')
