from django.contrib import admin
from .models import Article, Category, Comment, Tag

from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin
from jalali_date import datetime2jalali, date2jalali


# Register your models here.
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Tag)

@admin.register(Article)
# class ArticleAdmin(admin.ModelAdmin):
class ArticleAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('title', 'category', 'writer', 'get_publish_jalali', 'status')
    list_filter = ('status', 'publish')
    list_editable = ('status',)
    search_fields = ('title', 'writer__username')
    raw_id_fields = ('writer',)
    prepopulated_fields = {'slug': ('title',)}

    def get_publish_jalali(self, obj):
        return datetime2jalali(obj.publish).strftime('%Y/%m/%d %H:%M:%S')

    get_publish_jalali.short_description = 'تاریخ انتشار'
    get_publish_jalali.admin_order_field = 'publish'


# admin.site.register(Article, ArticleAdmin)
