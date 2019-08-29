from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Classroom, Student
from .forms import ClassroomForm, SignupForm, SigninForm, StudentForm



def signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("classroom-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)

def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('classroom-list')
    context = {
        "form":form
    }
    return render(request, 'signin.html', context)

def signout(request):
    logout(request)
    return redirect("signin")




def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	student=Student.objects.filter(classroom=classroom)
	context = {
		"classroom": classroom,
		"student":student,
	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):

	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None)
		if form.is_valid():
			class_obj = form.save(commit=False)
			class_obj.teacher = request.user
			form.save()
			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	if not (request.user.is_authenticated and classroom.teacher==request.user):
		return redirect('warn')
	else:
		form = ClassroomForm(instance=classroom)
		if request.method == "POST":
			form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
			if form.is_valid():
				form.save()
				messages.success(request, "Successfully Edited!")
				return redirect('classroom-list')
			print (form.errors)
		context = {
		"form": form,
		"classroom": classroom,
		}
		return render(request, 'update_classroom.html', context)



def classroom_delete(request, classroom_id):
	Classroom.objects.get(id=classroom_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')




def add_student(request, classroom_id):
	classroom_obj = Classroom.objects.get(id=classroom_id)
	form = StudentForm()
	if request.method == "POST":
		form = StudentForm(request.POST, request.FILES or None)
		if form.is_valid():
			student_obj = form.save(commit=False)
			student_obj.classroom = classroom_obj
			student_obj.save()
			messages.success(request, "Successfully Added!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	"class":classroom_obj

	}
	return render(request, 'add_student.html', context)

