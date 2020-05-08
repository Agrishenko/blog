from django .shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Tag
from .forms import PostForm, TagsForm
from django.shortcuts import redirect
from django.urls import reverse


class ObjectDetai:

    model = None
    templete = None

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        return render(request, self.templete, {self.model.__name__.lower(): obj, 'admin_obj': obj, 'detail': True})


class ObjectCreate:
    form_model = None
    template = None
    templeteReturn = None

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, {'form': form})

    def post(self, request):
        form = self.form_model(request.POST, files=request.FILES or None)
        if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                form.save_m2m()
                return redirect(self.templeteReturn)

        return render(request, self.template, {'form': form})

class ObjectEdit:
    model = None
    model_form = None
    template = None

    def get(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template, {'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        bound_form = self.model_form(request.POST, instance=obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return redirect(request, self.template, {'form': bound_form, self.model.__name__.lower(): obj})


class ObjectDelete:
    model = None
    templeteReturn = None
    templete = None

    def get(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        return render(request, self.templete, {self.model.__name__.lower(): obj})

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        obj.delete()
        return redirect(reverse(self.templeteReturn))
