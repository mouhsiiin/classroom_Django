from django.shortcuts import redirect

def student_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == "student":
            return view_func(request, *args, **kwargs)
        else:
            return redirect("socialmedia:post-list")
    return _wrapped_view

def teacher_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == "teacher":
            return view_func(request, *args, **kwargs)
        else:
            return redirect("socialmedia:post-list")
    return _wrapped_view