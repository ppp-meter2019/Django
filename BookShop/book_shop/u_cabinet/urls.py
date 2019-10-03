from django.urls import path, include, re_path
from . import views, auth_routine
from django.contrib.auth.views import  LogoutView

#, auth_views


app_name = 'u_cabinet'
urlpatterns = [
    path('profile/<int:pk>/', auth_routine.UserProfile.as_view(), name='profile'),
    path('profile/user/reviews-list/', views.MyReviewsList.as_view(), name='my_reviews'),
    path('profile/user/update-review/<int:pk>', views.UpdateReview.as_view(), name='update_review'),
    path('profile/user/new_review/<int:pk>', views.CreateReview.as_view(), name='new_review'),
    path('basket/', views.SelectedBooksList.as_view(), name='basket'),
    path('basket-remove/<int:book_id>', views.SelectedBooksList.as_view(), name='basket-remove'),
    path('basket-add/<int:book_id>', views.set_to_session, name='basket-add'),
]

auth_urls = [
    path('register', auth_routine.RegisterUser.as_view(), name='register'),
    path('login/', auth_routine.BookShopLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    ]
#
urlpatterns += auth_urls
