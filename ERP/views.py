from django.shortcuts import redirect, render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q,F                        #for OR operations
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from StudentManagement.models import ToDoList, Task, Group, Announcement, Stationary, Student, BookIssueStore, Teacher
from StudentManagement.forms import TaskForm, GroupForm, AnnouncementForm
from django.core.exceptions import PermissionDenied


@login_required
def say_truth(request):
    profile_set = Student.objects.all()
    return render(request, 'hello.html', {'students': profile_set})  # Pass the data as 'students'

def user_login(request):
    if request.method == 'POST':
        username  = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged In.")
            return redirect('home')
        else:
            messages.success(request, "There was an Error")
            return redirect('login')
    else:
        return render(request, 'login.html')
 
def register_student(request):
    if request.method == 'POST':
        # Extract form data from the request
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        roll_no = request.POST.get('rollNo')
        phone_no = request.POST.get('phoneNo')
        address = request.POST.get('address')
        year = request.POST.get('year')
        division = request.POST.get('division')
        upi_id = request.POST.get('upiId')
        upi_handle = request.POST.get('upiHandle')

        # Create a new user in the default Django User model
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
        # After user creation, create the Student object linked to this user
        student = Student.objects.create(
            user=user,
            name=f'{first_name} {last_name}',
            rollNo=roll_no,
            phoneNo=phone_no,
            address=address,
            year=year,
            division=division,
            upiId=upi_id,
            upiHandle=upi_handle
        )
        
        # Redirect or render success page
        return redirect('home')  # Update with your desired redirect page

    # If the request method is GET, display the form page
    return render(request, 'register.html')


def todo_list(request):
    user = request.user  # Get the current logged-in user
    try:
        # Try to get the to-do list for the user
        todo_list = ToDoList.objects.get(user=user)
    except ToDoList.DoesNotExist:
        # If no to-do list exists, create one for the user
        todo_list = ToDoList.objects.create(user=user)

    tasks = todo_list.tasks.all()  # Retrieve all tasks in the user's to-do list

    # Debugging: print the tasks and their IDs to the console
    print("Tasks: ", [(task.taskID, task.taskName) for task in tasks])
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.todo_list = todo_list
            task.save()
            return redirect('todo_list')

    return render(request, 'todo_list.html', {'todo_list': todo_list, 'tasks': tasks, 'form': form})


# View to mark a task as complete/incomplete
def toggle_task_completion(request, task_id):
    task = get_object_or_404(Task,taskID=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('todo_list')


def delete_task(request, task_id):
    task = get_object_or_404(Task, taskID=task_id)
    task.delete()
    return redirect('todo_list')


def user_groups_announcements(request, group_id=None):
    # Get the logged-in user
    user = request.user

    # Get all groups the user belongs to
    groups = Group.objects.filter(students=user.student)

    # If a group ID is provided, filter announcements for that group
    announcements = None
    if group_id:
        group = get_object_or_404(groups, groupId=group_id)
        announcements = Announcement.objects.filter(group=group).order_by('-timestamp')
    else:
        group = None

    context = {
        'groups': groups,
        'group': group,
        'announcements': announcements,
    }

    return render(request, 'announcement.html', context)


def group_announcements(request, group_id):
    # Get the group the user is trying to access
    group = get_object_or_404(Group, groupId=group_id)
    
    # Get announcements for the group, ordered by timestamp
    announcements = Announcement.objects.filter(group=group).order_by('-timestamp')

    context = {
        'group': group,
        'announcements': announcements,
    }

    return render(request, 'group_announcements.html', context)

    
def seller_items(request):
    # Group items by category (assuming category is stored as a CharField)
    items_by_category = {}
    
    # Get all distinct categories
    categories = Stationary.objects.values_list('category', flat=True).distinct()

    for category in categories:
        # Get items for each category
        category_items = Stationary.objects.filter(category=category)
        items_by_category[category] = category_items
    
    # Pass the grouped items to the template
    return render(request, 'seller_items.html', {'items_by_category': items_by_category})


def store_view(request):
    if request.method == 'POST':
        book_name = request.POST.get('bookName')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        seller = request.user.student
        desc = request.POST.get('desc')

        # Create a new BookIssueStore instance
        book = BookIssueStore(
            bookName=book_name,
            price=price,
            image=image,
            desc=desc,
            seller=seller,
        )
        book.save()
        return redirect('store_view')    
    
    items = BookIssueStore.objects.all()  # Get all items in the store
    return render(request, 'store_items.html', {'items': items})

@login_required
def create_group(request):
    try:
        # Check if the user has a related teacher object
        teacher = request.user.teacher
    except Teacher.DoesNotExist:
        # If the user is not a teacher, raise a permission error or handle accordingly
        raise PermissionDenied("You are not authorized to create a group because you are not a teacher.")
    
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.teacher = teacher  # Assign the logged-in teacher to the group
            group.save()
            form.save_m2m()  # Save the many-to-many field (students)
            return redirect('group_list')
    else:
        form = GroupForm()
    
    return render(request, 'create_group.html', {'form': form})


@login_required
def group_list(request):
    try:
        teacher = request.user.teacher  # Get the teacher associated with the current user
        groups = Group.objects.filter(teacher=teacher)  # Filter groups created by this teacher
    except Teacher.DoesNotExist:
        groups = []  # If the user is not a teacher, return an empty list or handle as needed
    
    return render(request, 'group_list.html', {'groups': groups})


@login_required
def create_announcement(request):
    teacher = request.user.teacher  # Get the teacher associated with the logged-in user
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, teacher=teacher)  # Pass teacher to the form
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.teacher = teacher  # Link the announcement to the logged-in teacher
            announcement.save()
            return redirect('group_list')  # Redirect after successful creation
    else:
        form = AnnouncementForm(teacher=teacher)  # Pass teacher to the form
    
    return render(request, 'create_announcement.html', {'form': form})

@login_required
def baseTemplate(request):
    return render(request, 'index.html')


@login_required
def user_detail(request):
    # Check if the user is a student or teacher
    if hasattr(request.user, 'student'):
        user_type = 'student'
        user_detail = request.user.student
    elif hasattr(request.user, 'teacher'):
        user_type = 'teacher'
        user_detail = request.user.teacher
    else:
        user_type = 'none'
        user_detail = None

    return render(request, 'user_detail.html', {'user_type': user_type, 'user_detail': user_detail})