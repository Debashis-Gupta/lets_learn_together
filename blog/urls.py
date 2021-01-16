from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import request
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from marketing.views import email_list_signup
from contact.views import contact,message,loginPage,register,logoutUser,ActivateAccountView
from portfolio.views import portfolio
from posts.views import (index,
                         search,
    # post_list,
    # post_detail,
                         post_create,
                         # post_update,
                         post_delete,
                         IndexView,
                         PostListView,
                         PostDetailView,
                         PostCreateView,
                         PostUpdateView,
                         PostDeleteView,
                         CatDetailView, cat_detail)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', index),
    path('', IndexView.as_view(), name='home'),
    # path('accounts/profile/', IndexView.as_view()),
    # path('blog/', post_list, name='post-list'),
    path('blog/', PostListView.as_view(), name='post-list'),
    path('search/', search, name='search'),
    path('email-signup/', email_list_signup, name='email-list-signup'),
    # path('create/', post_create, name='post-create'),
    path('create/',permission_required('post_create')(PostCreateView.as_view()) , name='post-create'),
    # path('post/<id>/', post_detail, name='post-detail'),
    path('post/<pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/<id>/update/', post_update, name='post-update'),
    path('post/<pk>/update/',permission_required('post_update')(PostUpdateView.as_view()), name='post-update'),
    # path('post/<id>/delete/', post_delete, name='post-delete'),
    path('post/<pk>/delete/', permission_required('post-delete')(PostDeleteView.as_view()), name='post-delete'),
    path('tinymce/', include('tinymce.urls')),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path('accounts/', include('allauth.urls')),

    #self try categories
    path('category/<slug:cat>',cat_detail,name='cat-detail'),

    #contact
    path('contact',contact,name="contact"),
    path('message',message,name="message"),
    path('login',loginPage,name='login'),
    path('register',register,name='register'),
    path('logout',logoutUser,name='logout'),

#     Email activation
    path('activate/<uid>/<token>',ActivateAccountView.as_view(),name='activate'),
#  portfolio
    path('portfolio',portfolio,name='portfolio')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
