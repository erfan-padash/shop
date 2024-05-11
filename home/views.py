from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product, Category
from . import tasks
from django.contrib import messages
from .forms import UploadFileForm
from utils import IsAdminUserMixin
from orders.forms import CartAddForm


class HomeView(View):

    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render(request, 'home/home.html', {'products': products, 'categories': categories})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm
        return render(request, 'home/detail.html', {'product': product, 'form': form})


class BucketView(IsAdminUserMixin, View):
    template_name = 'home/bucket.html'

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects})


class DeleteBucketObject(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.delete_obj_task.delay(key)
        messages.success(request, 'your object will delete soon', 'info')
        return redirect('home:bucket')


class DownloadBucketObject(IsAdminUserMixin, View):

    def get(self, request, key):
        tasks.download_obj_task.delay(key)
        messages.success(request, 'your file will download soon', 'success')
        return redirect('home:bucket')


class UploadBucketObject(IsAdminUserMixin, View):
    form_class = UploadFileForm
    template_name = 'home/upload.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            tasks.upload_obj_task.delay(filename=request.FILES['file'], objectname=cd['name_file'])
            messages.success(request, 'your file uploaded successfully', 'success')
            return redirect('home:bucket')
        return render(request, self.template_name, {'form': form})
