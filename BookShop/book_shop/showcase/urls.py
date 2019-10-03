from django.urls import path, include
from . import views
from django.contrib.auth import views as authviews


app_name = 'showcase'

urlpatterns = [
    path('', views.AllBookList.as_view(), name='index'),
    path('<int:g_filter>', views.AllBookList.as_view(), name='filtered'),
    path('books/', views.AllBookList.as_view(), name='all_books'),
    path('books_info/<int:pk>/', views.BookDetailedView.as_view(), name='bfi'),
    path('basket_books_info/<int:pk>/', views.BookDetailedView.as_view(), {'basket': True}, name='info_in_basket'),
    path('sale/<int:g_filter>', views.AllBookList.as_view(), {'on_sale':True}, name='sale'),
    path('about/', views.about, name='about_us'),
    path('allreviews/', views.AllReviewedBook.as_view(), name='all_reviews'),
    path('reviews_by_book/<int:book_id>', views.AllReviewsByBook.as_view(), name='reviews_by_book'),
    path('reviews_by_book/read_review/<int:pk>', views.ReadReview.as_view(), name='read_review'),
]

