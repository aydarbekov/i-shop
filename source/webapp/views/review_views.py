from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView
from webapp.models import Review, Product


class ReviewListView(ListView):
    context_object_name = 'reviews'
    model = Review
    ordering = ['-created_at']


class ReviewCreateView(CreateView):
    model = Review
    fields = ['text']

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs.get('pk'))
        review = Review(
            product=product,
            grade=self.request.POST.get('example'),
            text=form.cleaned_data['text'],
            author=self.request.user
        )
        review.save()
        return redirect('webapp:product_detail', pk=review.product.pk)

