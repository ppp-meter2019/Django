from django.shortcuts import render , redirect
from django.urls import reverse
from .models import Book, Genre
from u_cabinet.models import Comment
from u_cabinet.models import Review
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.db.models import Count
from u_cabinet.forms import CommentForm
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured
# Create your views here.



# #### Test CBV classes

class GenreWithUrl(Genre):

    viewcontext=''
    class Meta:
        proxy = True

    def get_absolute_url(self):
        return reverse(self.viewcontext, kwargs={'g_filter': self.id})

    @classmethod
    def set_viewcontext(сls,viewcontext):
        сls.viewcontext = viewcontext


class AllBookList(ListView):
    model = Book
    context_object_name = 'all_books'
    allow_empty = True
    template_name = "showcase/main.html"
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super(AllBookList, self).get_context_data(**kwargs)
        try:
            if self.kwargs['on_sale']:
                GenreWithUrl.set_viewcontext('showcase:sale')
                context['curr_tub'] = 'sale'
                context['menu_head_url'] = reverse('showcase:sale', kwargs={'g_filter': 0})

        except Exception as e:
            GenreWithUrl.set_viewcontext('showcase:filtered')
            context['menu_head_url'] = reverse('showcase:filtered', kwargs={'g_filter': 0})
            context['curr_tub'] = 'index'
            context['curr_id'] = 0
        try:
            context['curr_id'] = self.kwargs['g_filter']
            context['curr_tub'] = ''
        except Exception as e:
            pass

        context['all_genres'] = GenreWithUrl.objects.all().order_by('name')
        return context

    def get_queryset(self):
        qs = self.model.objects.all()
        try:
            filter_arg = self.kwargs['g_filter']
            if filter_arg:
                qs = qs.filter(genre=filter_arg)

        except:
            pass
        try:
            if self.kwargs['on_sale']:
                qs = qs.filter(is_sale=True)
        except:
            pass
        qs = qs.order_by('short_title')  # you don't need this if you set up your ordering on the model
        return qs


class BookDetailedView(DetailView):
    model = Book
    context_object_name = 'book_instance'
    template_name = 'showcase/full_spec.html'

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        try:
            basket = self.kwargs['basket']
            if basket:
                self.extra_context = {'basket': True}
            else:
                self.extra_context = {}
        except Exception as e:
            pass
        context = {}
        if self.object:
            context['object'] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        return super().get_context_data(**context)


def about(request):
    ctx = {}
    ctx['curr_tub'] = 'about_us'
    return render(request, 'showcase/about.html', ctx)


class AllReviewedBook(ListView):
    model = Book
    context_object_name = 'books_with_reviews'
    allow_empty = True
    template_name = "showcase/reviews-list.html"
    paginate_by = 8

    def get_queryset(self):
        reviwed_book = set(Review.objects.filter(status='publish').values_list('book', flat=True))
        qs = self.model.objects.filter(id__in=reviwed_book).annotate(num_reviews=Count('review', distinct=True))
        return qs


class AllReviewsByBook(ListView):
    model = Review
    context_object_name = 'books_reviews'
    allow_empty = False
    template_name = "showcase/reviews-list-bybook.html"

    def get_queryset(self):
        try:
            book_instance = Book.objects.get(id=self.kwargs['book_id'])
        except Exception as e:
            book_instance = None
            print('---------------book_instance = ', book_instance)
        self.extra_context = {'book': book_instance}
        qs = self.model.objects.filter(book=book_instance)
        return qs


class ReadReview(CreateView):
    model = Comment
    context_object_name = 'review_instance'
    template_name = 'showcase/read-review.html'
    form_class = CommentForm
    success_url = 'showcase:read_review'

    def get(self, request, *args, **kwargs):
        self.extra_context = {'review_instance': Review.objects.get(id=kwargs['pk'])}
        self.object = None
        return super().get(request, *args, **kwargs)


    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save(
            from_user=User.objects.get(id=self.request.user.id),
            for_book=Review.objects.get(id=self.kwargs['pk']))

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        if not self.success_url:
            raise ImproperlyConfigured("No URL to redirect to. Provide a success_url.")
        return str(reverse(self.success_url, kwargs={'pk': self.kwargs['pk']}))