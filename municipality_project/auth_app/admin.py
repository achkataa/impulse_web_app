from django.contrib import admin

# Register your models here.
from municipality_project.auth_app.models import ProjectUser, UserProfile


@admin.register(ProjectUser)
class ProjectUserAdmin(admin.ModelAdmin):
    pass

@admin.register(UserProfile)
class UserDocumentAdmin(admin.ModelAdmin):
    pass