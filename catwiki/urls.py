from django.urls import include, path, re_path
from rest_framework import routers
from . import views
from rest_framework.authtoken import views as viewsRest
from rest_framework.urlpatterns import format_suffix_patterns



router = routers.DefaultRouter()
router.register(r'homes', views.HomeViewSet, basename='home')
router.register(r'humans', views.HumanViewSet, basename='human')
router.register(r'breeds', views.BreedViewSet, basename='breed')
router.register(r'cats', views.CatViewSet, basename='cat')

urlpatterns = [

# Django rest framework project
    path('rest/', include(router.urls), name='rest_index'),
    path('homes/<int:pk>/highlight/', views.HomeHighlight.as_view(),name='home-highlight'),
    path('api-token-auth/', views.CustomAuthToken.as_view()),
    path('auth/', views.RestView.as_view()),
    path('api/login', views.login, name='login'),
    path('api/sampleapi', views.SampleApi.as_view()),
    path('cat_list2/', views.CatList2.as_view(),name='cat-list2'),
    path('cats/<int:pk>/', views.CatDetail2.as_view(),name='cat-detail2'),
    path('humans/', views.HumanList2.as_view(),name='human-list2'),
    path('humans/<int:pk>/', views.HumanDetail2.as_view(),name='human-detail2'),
    path('breeds/', views.BreedList2.as_view(),name='breed-list2'),
    path('breeds/<int:pk>/', views.BreedDetail2.as_view(),name='breed-detail2'),


# Django project
    path('index/', views.index, name='django_index'),
    path('home_list/', views.HomeView.as_view(), name='home_list'),
    path('human_list/', views.HumanView.as_view(), name='human_list'),
    path('breed_list/', views.BreedView.as_view(), name='breed_list'),
    path('cat_list/', views.CatView.as_view(), name='cat_list'),
    path('home_detail/<int:pk>/', views.Home_DetailView.as_view(), name='home_detail'),
    path('human_detail/<int:pk>/', views.Human_DetailView.as_view(), name='human_detail'),
    path('breed_detail/<int:pk>/', views.Breed_DetailView.as_view(), name='breed_detail'),
    path('cat_detail/<int:pk>/', views.Cat_DetailView.as_view(), name='cat_detail'),
    path('home_create/', views.create_home, name='home_create'),
    path('human_create/', views.create_human, name='human_create'),
    path('cat_create/', views.create_cat, name='cat_create'),
    path('breed_create/', views.create_breed, name='breed_create'),
    path('home_edit/<int:pk>/', views.edit_home, name='home_edit'),
    path('breed_edit/<int:pk>/', views.edit_breed, name='breed_edit'),
    path('cat_edit/<int:pk>/', views.edit_cat, name='cat_edit'),
    path('human_edit/<int:pk>/', views.edit_human, name='human_edit'),
    path('home_confirm_delete/<int:pk>/', views.Home_DeleteView.as_view(), name='home_confirm_delete'),
    path('human_confirm_delete/<int:pk>/', views.Human_DeleteView.as_view(), name='human_confirm_delete'),
    path('breed_confirm_delete/<int:pk>/', views.Breed_DeleteView.as_view(), name='breed_confirm_delete'),
    path('cat_confirm_delete/<int:pk>/', views.Cat_DeleteView.as_view(), name='cat_confirm_delete'),


]

