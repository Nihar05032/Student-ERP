from django.db import models
from django.contrib.auth.models import User

# Django automatically creates an id field in every model class and sets it as the primary key by default.
#The Parent Class Should be above the base class but if you cant do that pass the args as 'String'



class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name="teacher")
    teacherID = models.BigAutoField(primary_key= True)
    name = models.CharField(max_length= 255)
    phoneNo = models.CharField(max_length= 255)
    position = models.CharField(max_length= 255)

    def __str__(self) -> str:                 #For returning the name of the teacher instead of original object string representation
        return self.name
    
    class Meta:                               #For Sorting the table according to the teachers ID
        ordering = ['teacherID']


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name="student")
    regNo = models.BigAutoField(primary_key= True)
    name = models.CharField(max_length= 255)
    rollNo = models.SmallIntegerField()
    phoneNo = models.CharField(max_length=10, default="None")
    address = models.CharField(max_length= 255)
    YEAR_CHOICES = [
        ('FE', 'First Year'),
        ('SE', 'Second Year'),
        ('TE', 'Third Year'),
        ('BE', 'Fourth Year'),
    ]
    DIVISION_CHOICES = [(i, f"Division {i}") for i in range(1, 9)]    #8 sem hota ha engineering ma
    year = models.CharField(max_length=2, choices=YEAR_CHOICES, default='FE')
    division = models.IntegerField(choices=DIVISION_CHOICES, default=1)
    UPI_HANDLE_CHOICES = [
        ('@oksbi', '@oksbi'),
        ('@okhdfc', '@okhdfc'),
        ('@okicici', '@okicici'),
        ('@okaxis', '@okaxis'),
        ]
    upiId = models.CharField(max_length=50)  # For UPI ID before the '@'
    upiHandle = models.CharField(max_length=10, choices=UPI_HANDLE_CHOICES, default='@oksbi')

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['regNo']


class Group(models.Model):
    groupId = models.BigAutoField(primary_key= True)      
    groupName = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_groups')
    students = models.ManyToManyField(Student, related_name='groups')

    def __str__(self):
        return self.groupName
    
class Seller(models.Model):
    sellerID = models.BigAutoField(primary_key= True)
    name = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)
    UPI_HANDLE_CHOICES = [
        ('@oksbi', '@oksbi'),
        ('@okhdfc', '@okhdfc'),
        ('@okicici', '@okicici'),
        ('@okaxis', '@okaxis'),
        ]
    upiId = models.CharField(max_length=50)  # For UPI ID before the '@'
    upiHandle = models.CharField(max_length=10, choices=UPI_HANDLE_CHOICES, default='@oksbi',null=True, blank=True)



    def __str__(self):
        return self.name


class Announcement(models.Model):
    announce = models.CharField(max_length= 255)
    timestamp = models.DateTimeField(auto_now_add= True)
    enddate = models.DateField(blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_announcements')
    group = models.ForeignKey(Group, on_delete=models.CASCADE,null=True, blank=True, related_name='announcements')  # Link announcement to a group


class Calender(models.Model):
    event = models.CharField(max_length= 255)
    eventTime = models.DateTimeField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='events')
    students = models.ManyToManyField(Student, related_name='events_viewable')


class BookIssueStore(models.Model):
    #price = models.SmallIntegerField()
    bookName = models.CharField(max_length= 255)
    price = models.DecimalField(max_digits= 6, decimal_places= 2)
    image = models.ImageField(upload_to='item_images/')  # Customize the upload path...This argument specifies the directory within your media root where uploaded images will be saved. You'll need to configure your media settings in settings.py
    seller = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='books_sold')
    desc = models.CharField(max_length= 255, null=True, blank= True)
    #buyer = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='books_bought', null=True, blank=True)


class Stationary(models.Model):
    itemName = models.CharField(max_length= 255)
    price = models.DecimalField(max_digits= 6, decimal_places= 2)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='stationery_items',null=True, blank=True) #It should return all the books that are being bought from the stationary by a particular student
    category = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)


class ToDoList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)  # Link to the User model

    def __str__(self):
        return f"To-Do List for {self.user.username}"
    
class Task(models.Model):
    taskID = models.AutoField(primary_key=True)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE, related_name='tasks')  # A task belongs to a to-do list
    taskName = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)  # Mark task as completed or not

    def __str__(self):
        return self.taskName
