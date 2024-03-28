from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
import math, random 
from .models import Classrooms, Teachers, Students, Assignments, Submissions
from itertools import chain
from .forms import CreateAssignmentForm
from . import email
from datetime import datetime
from django.utils.timesince import timesince
from .decorators import student_required, teacher_required


@login_required
def home(request):
    # Get the teacher mapping for the current user
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')

    # Get the student mapping for the current user
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')

    # Combine the teacher and student mappings
    mappings = list(teacher_mapping) + list(student_mapping)

    # Get all teachers
    teachers_all = Teachers.objects.all()

    return render(request, 'classrooms/home.html', {
        'mappings': mappings,
        'teachers_all': teachers_all
    })

@login_required
def create_class_request(request):
    if request.POST.get('action') == 'post':
        classrooms = Classrooms.objects.all()
        existing_codes = []
        for classroom in classrooms:
            existing_codes.append(classroom.class_code)
        class_name = request.POST.get('class_name')
        section = request.POST.get('section')
        if request.FILES.get('students_emails'):
            # Get the students' emails from the uploaded csv or xlx file
            students_emails = request.FILES.get('students_emails')
            students_emails = students_emails.read().decode('utf-8').split('\n')
            for email in students_emails:
                email = email.strip()
                if email:
                    # Send an invitation email to the student
                    email.joining_invitation_mail(class_name, email)

        class_code = generate_class_code(6,existing_codes)
        classroom = Classrooms(classroom_name=class_name,section=section,class_code=class_code)
        classroom.save()
        teacher = Teachers(teacher_id=request.user,classroom_id=classroom)
        teacher.save()
        return JsonResponse({'status':'SUCCESS'})

@login_required
def join_class_request(request):
    if request.POST.get('action') == 'post':
        code = request.POST.get('class_code')
        try:
            classroom = Classrooms.objects.get(class_code=code)
            student = Students.objects.filter(student_id = request.user, classroom_id = classroom)
            if (student.count()!=0):
                return redirect('classrooms:home')
        except Exception as e:
            print(e)
            return JsonResponse({'status':'FAIL','message':str(e)})
        student = Students(student_id = request.user, classroom_id = classroom)
        student.save()
        return JsonResponse({'status':'SUCCESS'})



@login_required
def render_class(request,id):
    classroom = Classrooms.objects.get(pk=id)
    try: 
        assignments = Assignments.objects.filter(classroom_id = id)
    except Exception as e:
        assignments = None

    try:
        students = Students.objects.filter(classroom_id = id)
    except Exception as e:
        students = None
    
    teachers = Teachers.objects.filter(classroom_id = id)
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    mappings = chain(teacher_mapping,student_mapping) 
    return render(request,'classrooms/class_page.html',{'classroom':classroom,'assignments':assignments,'students':students,'teachers':teachers,"mappings":mappings})

@teacher_required
@login_required
def create_assignment(request,classroom_id):
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    mappings = chain(teacher_mapping,student_mapping)

    if request.method == 'POST':
        form = CreateAssignmentForm(request.POST)
        if form.is_valid():
            assignment_name = form.cleaned_data.get('assignment_name')
            due_date = form.cleaned_data.get('due_date')
            due_time = form.cleaned_data.get('due_time')
            classroom_id = Classrooms.objects.get(pk=classroom_id)
            instructions = form.cleaned_data.get('instructions')
            total_marks = form.cleaned_data.get('total_marks')
            assignment = Assignments(assignment_name = assignment_name,due_date = due_date,due_time=due_time,instructions = instructions,total_marks = total_marks,classroom_id=classroom_id)
            assignment.save()
            email.assignment_post_mail(classroom_id,assignment.id)
            return redirect('classrooms:render_class',id=classroom_id.id)
        else:
            return render(request,'classrooms/create_assignment.html',{'form':form,'mappings':mappings})
    form = CreateAssignmentForm()
    return render(request,'classrooms/create_assignment.html',{'form':form,'mappings':mappings})


@teacher_required
@login_required
def assignment_summary(request,assignment_id):
    assignment = Assignments.objects.filter(pk = assignment_id).first()
    submissions = Submissions.objects.filter(assignment_id = assignment_id)
    teachers = Teachers.objects.filter(classroom_id = assignment.classroom_id)
    teacher_mapping = Teachers.objects.filter(teacher_id=request.user).select_related('classroom_id')
    student_mapping = Students.objects.filter(student_id=request.user).select_related('classroom_id')
    no_of_students = Students.objects.filter(classroom_id=assignment.classroom_id)
    mappings = chain(teacher_mapping,student_mapping)
    return render(request,'classrooms/assignment_summary.html',{'assignment':assignment,'submissions':submissions,'mappings':mappings,'no_of_students':no_of_students})


@teacher_required
@login_required
def delete_assignment(request,assignment_id):
    try:
        assignment = Assignments.objects.get(pk=assignment_id)
        classroom_id = assignment.classroom_id.id 
        Assignments.objects.get(pk=assignment_id).delete()
        return redirect('classrooms:render_class', id=classroom_id)
    except Exception as e:
        return redirect('classrooms:home')

@student_required
@login_required    
def unenroll_class(request,classroom_id):
    classroom = Classrooms.objects.get(pk=classroom_id)
    Students.objects.filter(student_id=request.user,classroom_id=classroom).delete()
    return redirect('classrooms:home')
   

@teacher_required
@login_required
def delete_class(request,classroom_id):
    classroom = Classrooms.objects.get(pk=classroom_id)
    teacher_mapping = Teachers.objects.get(teacher_id=request.user,classroom_id=classroom)
    teacher_mapping.delete()
    classroom.delete()
    return redirect('classrooms:home')


@teacher_required
@login_required
def mark_submission_request(request,submission_id,teacher_id):
    if request.POST.get('action') == 'post':
        marks = request.POST.get('submission_marks')
        submission = Submissions.objects.get(pk=submission_id)
        submission.marks_alloted = marks
        submission.save()
        email.submission_marks_mail(submission_id,teacher_id,marks)
        return JsonResponse({'status':'SUCCESS'})

@student_required
@login_required
def submit_assignment_request(request,assignment_id):
    assignment = Assignments.objects.get(pk=assignment_id)
    student_id = Students.objects.get(classroom_id=assignment.classroom_id,student_id=request.user.id)
    file_name = request.FILES.get('myfile')
    try:
        submission = Submissions.objects.get(assignment_id=assignment, student_id = student_id)
        submission.submission_file = file_name
        submission.save()
        return JsonResponse({'status':'SUCCESS'})

    except Exception as e:  
        print(str(e))  
        submission = Submissions(assignment_id = assignment,student_id= student_id,submission_file = file_name)
        dt1=datetime.now()
        dt2=datetime.combine(assignment.due_date,assignment.due_time)
        time = timesince(dt1, dt2)
        if time[0]=='0':
            submission.submitted_on_time=False
        submission.save()
        email.submission_done_mail(assignment_id,request.user,file_name)
        return JsonResponse({'status':'SUCCESS'})




def generate_class_code(total_digits,existing_codes) :  
    digits = ''.join([str(i) for i in range(0,10)])
    code = ""  
    while True:
        for i in range(total_digits) : 
            code += digits[math.floor(random.random() * 10)] 
        if code not in existing_codes:
            print('Code not in existing codes')
            break
    return code 