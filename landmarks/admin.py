from django.contrib import admin
from .models import (
    Landmark,
    LandmarkLanguageBased,
    LandmarkImage,
    LandmarkReview,
    LandmarkTourismCategory
)
# Register your models here.


class LandmarkAdmin(admin.ModelAdmin):
    model = Landmark
    ordering = ['id']
    list_display = ['id', 'name', 'height',
                    'govObject', 'area', 'created', 'active']
    list_display_links = ['id', 'name', 'area', 'created']
    list_filter = ['created', 'active']


admin.site.register(Landmark, LandmarkAdmin)


class LandmarkLanguageBasedAdmin(admin.ModelAdmin):
    model = LandmarkLanguageBased
    ordering = ['id']
    list_display = ['id', 'title', 'lang', 'created', 'active']
    list_display_links = ['id', 'title', 'lang', 'created']
    list_filter = ['created', 'lang', 'active']


admin.site.register(LandmarkLanguageBased, LandmarkLanguageBasedAdmin)

class LandmarkImageAdmin(admin.ModelAdmin):
    model = LandmarkImage
    ordering = ['id']
    list_display = ['id','landmark','image', 'created', 'active']
    list_display_links = ['id','landmark','image' , 'created']
    list_filter = ['created', 'active']


admin.site.register(LandmarkImage, LandmarkImageAdmin)


class LandmarkReviewAdmin(admin.ModelAdmin):
    model = LandmarkReview
    ordering = ['id']
    list_display = ['id','landmark','review', 'created', 'active']
    list_display_links = ['id','landmark' , 'created']
    list_filter = ['created', 'active']


admin.site.register(LandmarkReview, LandmarkReviewAdmin)


class LandmarkTourismCategoryAdmin(admin.ModelAdmin):
    model = LandmarkTourismCategory
    ordering = ['id']
    list_display = ['id','landmarkObject','categoryObject', 'created', 'active']
    list_display_links = ['id','landmarkObject' ,'categoryObject' ,'created']
    list_filter = ['created', 'active']
    search_fields=['categoryObject__id','landmarkObject__id']


admin.site.register(LandmarkTourismCategory, LandmarkTourismCategoryAdmin)

