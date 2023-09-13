from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import generic, View
from django.contrib.auth.views import LoginView, PasswordChangeView
from .models import Post, PostLike, Comment
from .forms import CustomUserCreationForm, CustomUserLoginForm, PostForm, CustomUserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(generic.ListView):
    template_name = 'board/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_active=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']
        post_like_count_dict = {}

        for post in posts:
            post_like_count = PostLike.objects.filter(post=post).count()
            post_like_count_dict[post] = post_like_count
        context['post_like_count_dict'] = post_like_count_dict

        current_page_num = context['page_obj'].number
        total_page = context['paginator'].num_pages

        x, y = divmod(current_page_num, self.paginate_by)
        if y == 0:
            x -= 1

        start_page = x * self.paginate_by + 1
        last_page = min(total_page, start_page + self.paginate_by - 1)

        context['start_page'] = start_page
        context['last_page'] = last_page
        context['page_range'] = range(start_page, 1 + last_page)
        context['have_next_range'] = total_page > last_page

        return context


class RegisterView(generic.CreateView):
    template_name = 'board/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('board:login')

    def form_valid(self, form):
        user = form.save(commit=False)

        profile_image = self.request.FILES.get('profile_image')
        if profile_image:
            user.profile_image = profile_image
        user.save()

        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'board/login.html'
    form_class = CustomUserLoginForm


class CustomUserUpdateView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'board/user_update.html'
    form_class = CustomUserUpdateForm
    success_url = reverse_lazy('board:index')


class CustomUserUpdateProfileImgView(LoginRequiredMixin, View):

    def get(self, request):
        template_name = 'board/user_update_profile_img.html'
        context = {"current_profile_image": request.user.profile_image}
        return render(request, template_name, context)

    def post(self, request):
        uploaded_image = request.FILES.get('profile_image')

        if uploaded_image:
            request.user.profile_image = uploaded_image
            request.user.save()
        return HttpResponseRedirect(reverse('board:index'))


class DeleteProfileImgView(LoginRequiredMixin, View):

    def post(self, request):
        request.user.profile_image = None
        request.user.save()
        return HttpResponseRedirect(reverse('board:index'))


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'board/post_create.html'
    form_class = PostForm
    success_url = reverse_lazy('board:index')

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "board/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = context['post']
        context["post_like_count"] = post.count_post_like()

        user = self.request.user
        context["like_post"] = False

        if user.is_authenticated:
            like_post = PostLike.objects.filter(user=user, post=post).exists()
            if like_post:
                context["like_post"] = True

        context['comments'] = post.get_comment()
        return context


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = "board/post_update.html"
    success_url = reverse_lazy('board:index')


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post

    success_url = reverse_lazy('board:index')


class PostLikeView(LoginRequiredMixin, View):

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        existing_like = PostLike.objects.filter(post=post, user=user)

        if not existing_like:
            PostLike.objects.create(post=post, user=user)
        else:
            existing_like.delete()

        return redirect('board:post_detail', pk=pk)


class CommentCreateView(LoginRequiredMixin, View):

    def post(self, request, board_id):
        comment_text = self.request.POST.get("comment_text")

        if comment_text:
            Comment.objects.create(
                content=comment_text,
                user=self.request.user,
                post=Post.objects.get(pk=board_id)
            )
        return redirect('board:post_detail', pk=board_id)


class CommentDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Comment

    def get_success_url(self):
        post = self.object.post
        return reverse('board:post_detail', kwargs={'pk': post.pk})
