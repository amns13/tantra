from django.contrib import admin


class CustomModelAdmin(admin.ModelAdmin):
    """
    Custom Model Admin class.
    Adds functionality to set created by and modified by.
    """

    def save_model(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.created_by:
            instance.created_by = user
        instance.updated_by = user
        instance.save()
        form.save_m2m()
        return instance
