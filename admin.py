from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Comment, Like, Post
from accounts.admin_site import admin_site


@admin.register(Post, site=admin_site)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_link', 'published', 'created_at', 'comment_count', 'like_count', 'post_preview')
    list_filter = ('published', 'created_at', 'author__is_staff')
    search_fields = ('title', 'content', 'author__username', 'author__email')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    list_per_page = 20
    readonly_fields = ('post_preview', 'created_at', 'updated_at')
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'author', 'content', 'published')
        }),
        ('Media', {
            'fields': ('image', 'post_preview'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def author_link(self, obj):
        if obj and obj.author and obj.author.id:
            app_label = obj.author._meta.app_label
            model_name = obj.author._meta.model_name
            url = reverse(f'admin:{app_label}_{model_name}_change', args=[obj.author.id])
            return mark_safe(f'<a href="{url}">{obj.author.username}</a>')
        return "-"
    author_link.short_description = 'Author'
    author_link.admin_order_field = 'author__username'

    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comments'

    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Likes'

    def post_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 100%;" />',
                obj.image.url
            )
        return "No image"
    post_preview.short_description = 'Image Preview'


@admin.register(Comment, site=admin_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('truncated_body', 'author_link', 'post_link', 'created_at')
    list_filter = ('created_at', 'author')
    search_fields = ('body', 'author__username', 'post__title')
    date_hierarchy = 'created_at'
    list_per_page = 20
    readonly_fields = ('created_at',)
    
    def truncated_body(self, obj):
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body
    truncated_body.short_description = 'Comment'
    
    def author_link(self, obj):
        if obj and obj.author and obj.author.id:
            app_label = obj.author._meta.app_label
            model_name = obj.author._meta.model_name
            url = reverse(f'admin:{app_label}_{model_name}_change', args=[obj.author.id])
            return mark_safe(f'<a href="{url}">{obj.author.username}</a>')
        return "-"
    author_link.short_description = 'Author'
    author_link.admin_order_field = 'author__username'
    
    def post_link(self, obj):
        url = reverse('admin:posts_post_change', args=[obj.post.id])
        return mark_safe(f'<a href="{url}">{obj.post.title[:50]}</a>')
    post_link.short_description = 'Post'


@admin.register(Like, site=admin_site)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post_link', 'user_link', 'created_at')
    list_filter = ('created_at', 'user__is_staff')
    search_fields = ('post__title', 'user__username')
    date_hierarchy = 'created_at'
    list_per_page = 20
    readonly_fields = ('created_at',)

    def post_link(self, obj):
        if obj and obj.post and obj.post.id:
            url = reverse('admin:posts_post_change', args=[obj.post.id])
            return mark_safe(f'<a href="{url}">{obj.post.title}</a>')
        return "-"
    post_link.short_description = 'Post'
    post_link.admin_order_field = 'post__title'

    def user_link(self, obj):
        if obj and obj.user and obj.user.id:
            app_label = obj.user._meta.app_label
            model_name = obj.user._meta.model_name
            url = reverse(f'admin:{app_label}_{model_name}_change', args=[obj.user.id])
            return mark_safe(f'<a href="{url}">{obj.user.username}</a>')
        return "-"
    user_link.short_description = 'User'
    user_link.admin_order_field = 'user__username'
