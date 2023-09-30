from http.client import HTTPResponse

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm

# Create your views here.
from .models import Category, Product, ReviewRating


def categories(request):
    return {"categories": Category.objects.all()}


def all_products(request):
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "products/detail.html", {"product": product})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True)
    )
    return render(request, "products/category.html", {"category": category, "products": products})


def submit_review(request, product_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thank you! Your review has been updated.")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get("REMOTE_ADDR")
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted.")
                return redirect(url)


def search(request):
    if request.method == "POST":
        search = request.POST["search"]
        products = Product.objects.filter(title__contains=search)
        # products = Product.objects.filter(title__contains=search)
        # return HTTPResponse(products)
        return render(request, "store/search.html", {"search": search, "products": products})
    else:
        return render(request, "store/search.html", {})

    # return HTTPResponse('this is search')
