"""Root URL configuration for bwa project."""

# from django.contrib import admin  # Comment out the default admin import
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import AboutView

# Import our custom admin site
from accounts.admin_site import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),  # Use our custom admin site
    path('about/', AboutView.as_view(), name='about'),  # Moved before posts.urls
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('', include(('posts.urls', 'posts'), namespace='posts')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
