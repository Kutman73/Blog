from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from posts.models import Post, Hashtag, Comment
from posts.forms import PostCreateForm, CommentCreateForm
from users.utils import get_user_from_request


PAGINATION_LIMIT = 2


class PostView(ListView):
    model = Post
    template_name = 'posts/posts.html'

    def get_context_data(self, **kwargs):
        return {
            'posts': kwargs['posts'],
            'user': get_user_from_request(self.request),
            'max_page': range(1, kwargs['max_page'])
        }

    def get(self, request, *args, **kwargs):
        hashtag_id = request.GET.get('hashtag_id')
        search_text = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if hashtag_id:
            posts = Post.objects.filter(hashtags__in=[hashtag_id])
        else:
            posts = Post.objects.all()

        if search_text:
            posts = posts.filter(title__icontains=search_text)

        posts = [{
            'id': post.id,
            'title': post.title,
            'image': post.image,
            'description': post.description,
            'hashtags': post.hashtags.all()
        } for post in posts]

        max_page = round(posts.__len__() / PAGINATION_LIMIT)
        posts = posts[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        return render(request, self.template_name, context=self.get_context_data(
            posts=posts,
            max_page=max_page
        ))


def detail_post_view(requests, id):
    if requests.method == 'GET':
        post = Post.objects.get(id=id)
        comments = Comment.objects.filter(post_id=id)

        data = {
            'post': post,
            'hashtags': post.hashtags.all(),
            'comments': comments,
            'form': CommentCreateForm
        }
        # for c in comments:
        #     print(c)

        return render(requests, 'posts/detail.html', context=data)

    if requests.method == 'POST':
        form = CommentCreateForm(data=requests.POST)

        if form.is_valid():
            Comment.objects.create(
                author_id=2,
                text=form.cleaned_data.get('text'),
                post_id=id
                )
            return redirect(f'/posts/{id}/')

        else:
            post = Post.objects.get(id=id)
            comments = Comment.objects.filter(post_id=id)

            data = {
                    'post': post,
                    'hashtags': post.hashtags.all(),
                    'comments': comments,
                    'form': form
                }

            return render(requests, 'posts/detail.html', context=data)


class DetailPostView(DetailView):
    model = Post
    # context_object_name = 'post'
    template_name = 'posts/detail.html'

    def get_context_data(self, **kwargs):
        # comm = Comment.objects.filter(post_id=kwargs['object'])
        context = super(DetailPostView, self).get_context_data(**kwargs)
        context['form'] = CommentCreateForm
        context['comments'] = Comment.objects.all()
        # context['hashtags'] = self.model.hashtags.filter(post_id)
        # for c in context['comments']:
        #     if c.post_id:
        #         pass
        return context

    def post(self, request, *args, **kwargs):
        form = CommentCreateForm(data=request.POST)

        if form.is_valid():
            Comment.objects.create(
                author_id=request.user.id if not request.user.is_anonymous else 1,
                text=form.cleaned_data.get('text'),
                post_id=kwargs['pk']#[post.id for post in ]
            )
            return redirect(f'/posts/{kwargs["pk"]}/')

        else:
            post = Post.objects.get(id=self.model.pk)
            comments = Comment.objects.filter(post_id=self.model.pk)

            data = {
                'post': post,
                'hashtags': post.hashtags.all(),
                'comments': comments,
                'form': form
            }

            return render(request, self.template_name, context=data)


class HashtagsView(ListView):
    model = Hashtag
    template_name = 'hashtags/hashtags.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'hashtags': self.get_queryset(),
            'user': get_user_from_request(self.request)
        }



def post_create_view(request):
    if request.method == 'GET':
        data = {
            'form': PostCreateForm,
            'user': get_user_from_request(request)
        }

        return render(request, 'posts/../../Blog2/templates/posts/create.html', context=data)

    if request.method == 'POST':
        form = PostCreateForm(data=request.POST)

        if form.is_valid():
            Post.objects.create(
                author_id=1,
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description')
            )
            return redirect('/posts')
        else:
            data = {
                'form': form,
                'user': get_user_from_request(request)
            }
            return render(request, 'posts/../../Blog2/templates/posts/create.html', context=data)


# class PostCreateView(ListView, CreateView):
#     model = Post
#     template_name = PostCreateForm
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         return {
#             'user': get_user_from_request(self.request),
#             'form': kwargs['form'] if kwargs.get('form') else self.form_class,
#         }
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(data=request.POST)
#
#         if form.is_valid():
#             self.model.objects.create(
#                 author_id=request.user.id,
#                 title=form.cleaned_data.get('title'),
#                 description=form.cleaned_data.get('description')
#             )
#             return redirect('/posts/')
#         else:
#             return render(request, self.template_name, context=self.get_context_data(form=form))
