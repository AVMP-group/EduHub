# from channels.auth import login, logout
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from student_management_app.EmailBackEnd import EmailBackEnd
# views.py
from django.shortcuts import render, redirect

def staff_doubt_session(request):
    if request.method == "POST":
        staff_id = request.user.id
        student_id = request.POST.get('student_id')
        doubt_message = request.POST.get('doubt_message')

        doubt = Doubt(staff_id=staff_id, student_id=student_id, doubt_message=doubt_message)
        doubt.save()

        messages.success(request, "Doubt Sent Successfully.")
        return redirect('staff_doubt_session')

    students = Students.objects.all()
    context = {
        'students': students,
    }
    return render(request, 'staff_template/doubt_session_template.html', context)

def staff_doubt_reply(request, doubt_id):
    doubt = Doubt.objects.get(id=doubt_id)

    if request.method == "POST":
        doubt_reply = request.POST.get('doubt_reply')
        doubt.doubt_reply = doubt_reply
        doubt.save()

        messages.success(request, "Doubt Replied Successfully.")
        return redirect('staff_doubt_session')

    context = {
        'doubt': doubt,
    }
    return render(request, 'staff_template/doubt_reply_template.html', context)


def home(request):
    return render(request, 'index.html')


def loginPage(request):
    return render(request, 'login.html')



def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            user_type = user.user_type
            #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user_type == '1':
                return redirect('admin_home')
                
            elif user_type == '2':
                # return HttpResponse("Staff Login")
                return redirect('staff_home')
                
            elif user_type == '3':
                # return HttpResponse("Student Login")
                return redirect('student_home')
            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
            return redirect('login')



def get_user_details(request):
    if request.user != None:
        return HttpResponse("User: "+request.user.email+" User Type: "+request.user.user_type)
    else:
        return HttpResponse("Please Login First")



def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


