from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
#from .views import running, favicon, predict

urlpatterns = [
    path('', views.running, name='running'),
    path('favicon.png', views.favicon, name='favicon'),
    path('predict/', views.predict, name='predict'),
    path('classify_image/', views.classify_image, name='classify_image'),  # Add this line for image classificatio
]

# urlpatterns = [
#     path('', views.upload_file, name='upload_file'),
#     path('next',views.next_page,name='next_page'),
#     # Other URL patterns
# ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
