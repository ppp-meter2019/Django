from django.views.generic import ListView, DetailView, CreateView, UpdateView
from showcase.models import Book, Genre
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import BookListInBasket,ReviewAuthor, Review
from .forms import ReviewForm
from django.http.response import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


class SelectedBooksList(ListView):
    model = Book
    context_object_name = 'selected_books'
    allow_empty = True
    template_name = "u_cabinet/basket.html"
    paginate_by = 3

    def get_queryset(self):
        if self.request.user.is_authenticated:
            book_ids = [item.book.id for item in BookListInBasket.objects.filter(user=self.request.user)]
        else:
            book_ids = self.request.session.get('selected_items')
        try:
            if self.kwargs["book_id"]:
                if self.kwargs["book_id"] in book_ids:
                    if self.request.user.is_authenticated:
                        BookListInBasket.objects.filter(book=self.kwargs["book_id"]).delete()
                        book_ids = [item.book.id for item in BookListInBasket.objects.filter(user=self.request.user)]
                    else:
                        book_ids.remove(self.kwargs["book_id"])
                self.request.session['selected_items'] = book_ids
        except Exception as e:
            pass

        if book_ids:
            qs = self.model.objects.filter(id__in=book_ids)
        else:
            qs = self.model.objects.filter(id=0)

        return qs


@method_decorator(login_required, name='dispatch')
class CreateReview(CreateView):
    form_class = ReviewForm
    model = Review
    template_name = 'u_cabinet/update_review.html'
    success_url = 'u_cabinet:my_reviews'

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(
            author=ReviewAuthor.objects.get(user=self.request.user),
            book=Book.objects.get(id=self.kwargs['pk']))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(reverse(self.success_url))  # success_url may be lazy

    def get(self, request, *args, **kwargs):
        self.extra_context = {'book': Book.objects.get(id=self.kwargs['pk'])}
        self.object = None
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class MyReviewsList(ListView):
    model = Review
    context_object_name = 'my_reviews'
    allow_empty = True
    template_name = "u_cabinet/my_reviews.html"
    #paginate_by = 3

    def get_queryset(self):

        qs = Review.objects.filter(author=ReviewAuthor.objects.get(user=self.request.user))
        return qs


@method_decorator(login_required, name='dispatch')
class UpdateReview(UpdateView):
    template_name = 'u_cabinet/create_review.html'
    form_class = ReviewForm
    model = Review

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(
            author=ReviewAuthor.objects.get(user=self.request.user),
            book=Book.objects.get(id=self.kwargs['pk']))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return str(reverse('u_cabinet:my_reviews'))

    def get(self, request, *args, **kwargs):
        self.extra_context = {'book': Book.objects.get(review__id=self.kwargs['pk'])}
        self.object = None
        return super().get(request, *args, **kwargs)


def set_to_session(request, book_id):
    if request.user.is_authenticated:
        saved_list = [item.book.id for item in BookListInBasket.objects.filter(user=request.user)]
    else:
        saved_list = request.session.get('selected_items', [])
    if book_id in saved_list:
        messages.add_message(request,
                             message='Вы уже добавили эту книгу ...',
                             level=messages.INFO)
    else:
        if request.user.is_authenticated:
            BookListInBasket.objects.create(user=request.user, book=Book.objects.get(id=book_id))
            saved_list = [item.book.id for item in BookListInBasket.objects.filter(user=request.user)]
        else:
            saved_list.append(book_id)
        request.session['selected_items'] = saved_list

    return redirect('showcase:bfi', pk=book_id)


