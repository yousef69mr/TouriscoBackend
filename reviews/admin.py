from django.contrib import admin
from .models import Review,ReviewImage

# Register your models here.


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    ordering = ['id']
    list_display = ['id','userObject','content_object','rating' , 'created', 'active']
    list_display_links = ['id', 'rating', 'created']
    list_filter = ['content_type','created', 'active']


admin.site.register(Review, ReviewAdmin)


class ReviewImageAdmin(admin.ModelAdmin):
    model = ReviewImage
    ordering = ['id']
    list_display = ['id','review','image', 'created', 'active']
    list_display_links = ['id','review' , 'created']
    list_filter = ['created', 'active']


admin.site.register(ReviewImage, ReviewImageAdmin)

