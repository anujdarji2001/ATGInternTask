from django.urls import path
from accounts import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

urlpatterns = [
    path('home/',views.home,name='home'),
    path('',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('createblog/',views.createblog,name='createblog'),
    path('blogs/',views.blogs,name='blogs'),
    path('draft/',views.draft,name='draft'),
    path('myblog/',views.myblog,name='myblog'),
    path('editdraft/<int:id>/',views.editdraft,name='editdraft'),
    path('deleteblog/<int:id>/',views.deleteblog,name='deleteblog'),
]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
