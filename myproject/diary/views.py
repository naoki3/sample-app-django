from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import PageForm
from .models import Page
from datetime import datetime
from zoneinfo import ZoneInfo

class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "diary/index.html")

class PageCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = PageForm()
        return render(request, "diary/page_form.html", {"form": form})

    def post(self, request):
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("diary:index")
        return render(request, "diary/page_form.html", {"form": form})

class PageListView(LoginRequiredMixin, View):
    def get(self, request):
        page_list = Page.objects.order_by("page_date")
        # for page in page_list:
        #     try:
        #         page.page_date = datetime.strptime(page.page_date, "%Y年%m月%d日")
        #     except (ValueError, TypeError):
        #         # すでにdatetime型またはフォーマットが異なる場合はスキップ
        #         pass
        return render(request, "diary/page_list.html", {"page_list": page_list})

class PageDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        page = get_object_or_404(Page, id=id)
        return render(request, "diary/page_detail.html", {"page": page})

class PageUpdateView(LoginRequiredMixin, View):
    def get(self, request, id):
        page = get_object_or_404(Page, id=id)
        form = PageForm(instance=page)
        return render(request, "diary/page_update.html", {"form": form})

    def post(self, request, id):
        page = get_object_or_404(Page, id=id)
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            return redirect("diary:page_detail", id=id)
        return render(request, "diary/page_form.html", {"form": form})

class PageDeleteView(LoginRequiredMixin, View):
    def get(self, request, id):
        page = get_object_or_404(Page, id=id)
        return render(request, "diary/page_confirm_delete.html", {"page": page})

    def post(self, request, id):
        page = get_object_or_404(Page, id=id)
        page.delete()
        return redirect('diary:page_list')

index = IndexView.as_view()
page_create = PageCreateView.as_view()
page_list = PageListView.as_view()
page_detail = PageDetailView.as_view()
page_update = PageUpdateView.as_view()
page_delete = PageDeleteView.as_view()