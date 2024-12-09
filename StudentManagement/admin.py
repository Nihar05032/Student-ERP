from django.contrib import admin
from . import models


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'regNo', 'address', 'year', 'division']

@admin.register(models.Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacherID', 'phoneNo', 'position']

@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['groupId', 'groupName' ]
    filter_horizontal = ('students',)  # Use a horizontal filter to select multiple students

@admin.register(models.Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['sellerID', 'name', 'contact_info']


@admin.register(models.Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['announce', 'timestamp', 'enddate']

@admin.register(models.Stationary)
class StationaryAdmin(admin.ModelAdmin):
    list_display = ['itemName', 'price', 'seller']


@admin.register(models.BookIssueStore)
class BookIssueStoreAdmin(admin.ModelAdmin):
    list_display = ['bookName','price','seller']




     
    
