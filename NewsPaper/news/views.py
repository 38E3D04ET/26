from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post, Category
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db.models.signals import post_save

from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)



class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 100

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "filter": self.get_filter(),
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'sample_app/post_detail.html'

    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        qwe = Category.objects.filter(pk=Post.objects.get(pk=id).category.id).values("subscribers__username")
        context['is_not_subscribe'] = not qwe.filter(subscribers__username=self.request.user).exists()
        context['is_subscribe'] = qwe.filter(subscribers__username=self.request.user).exists()
        return context


@login_required
def add_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'добавлен в подписчики категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/news/')


@login_required
def del_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'удален из подписчиков категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/news/')



class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'sample_app/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post',)
    success_url = '/news/'

#    def form_valid(self, form):
#        form.instance.username = Post.objects.get(author=self.request.user.id)
#        return super(PostCreate, self).form_valid(form)

#    def post(self, request, *args, **kwargs):
#        self.instance.username = Post.objects.get(author=self.request.user.id)
#        for subscribe in Subscribe.objects.filter(category=request.POST.get('category')):
#            msg = EmailMultiAlternatives(
#            subject=request.POST['title'],
#            body=request.POST['contents'],
#            from_email='ai333i@yandex.ru',
#            to=['alf.alexy@yandex.ru'],
#            #to=[subscribe.objects.subscriber.email],
#            )
#            html_content = render_to_string(
#                'subscribeletter.html',
#                {
#                    'post': request.POST,
#                    'recipient': subscribe.objects.subscriber
#                }
#            )

#            msg.attach_alternative(html_content, "text/html")
#            msg.send()
#            print('отослано')
#        return redirect('/')


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'sample_app/post_create.html'
    form_class = PostForm
    permission_required = ('news.change_post',)
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'sample_app/post_delete.html'
    queryset = Post.objects.all()
    permission_required = ('news.delete_post',)
    success_url = '/news/'



#class CategoryDetailView(DetailView):
#    model = Category
#    template_name = 'sample/post_detail.html'
#    context_object_name = 'category'
#    queryset = Category.objects.all()
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['time_now'] = datetime.now()
#        id = self.kwargs.get('pk')
#        cat = Category.objects.filter(pk=Post.objects.get(pk=id).postCategory.name). vaiues("subscribers")
#        context['is_not_subscribe'] = not cat.filter(subscribers=self.request.user).exist()
#        context['is_subscribe'] = cat.filter(subscribers=self.request.user).exist()
#        return context


#@login_required
#def add_subscribe(request, pk):
#    sub_user = User.objects.get(id=request.user.pk)
#    category_object = Category.objects.get(pk=pk)
#    category_object.subscribers.add(sub_user)
#    return redirect('/news/')


#@login_required
#def del_subscribe(request, pk):
#    sub_user = User.objects.get(id=request.user.pk)
#    category_object = Category.objects.get(pk=pk)
#    category_object.subscribers.remove(sub_user)
#    return redirect('/news/')

#class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
#    template_name = 'news_app/post_create.html'
#    form_class = PostForm
#    permission_required = ('news.add_post')
#
#    def post(self, request, *args, **kwargs):
#        send_mail(
#            subject=Post.title,
#            message=Post.text,
#            from_email='alf.alexy@yandex.ru',
#            recipient_list=['ai333i@yandex.ru'],
#        )

