from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView

from django.views.decorators.cache import cache_control

from .models import Post

import logging

logger = logging.getLogger("pybo")

# logger.debug("Hey there it works!!1")
# logger.info("Hey there it works!!2")
# logger.error("Hey there it works!!3")


# User = get_user_model()
#
#
# class UserDetailView(LoginRequiredMixin, DetailView):
#     model = User
#     slug_field = "username"
#     slug_url_kwarg = "username"
#
#
# user_detail_view = UserDetailView.as_view()
#
#
# class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = User
#     fields = ["name"]
#     success_message = _("Information successfully updated")
#
#     def get_success_url(self):
#         assert (
#             self.request.user.is_authenticated
#         )  # for mypy to know that the user is authenticated
#         return self.request.user.get_absolute_url()
#
#     def get_object(self):
#         return self.request.user
#
#
# user_update_view = UserUpdateView.as_view()
#
#
# class UserRedirectView(LoginRequiredMixin, RedirectView):
#     permanent = False
#
#     def get_redirect_url(self):
#         return reverse("users:detail", kwargs={"username": self.request.user.username})
#
#
# user_redirect_view = UserRedirectView.as_view()
#
#
# class PostListView(TemplateView):  # 게시글 목록
#     template_name = 'pages/post_list.html'
#     queryset = Post.objects.all()
#
#     @cache_control(private=True)
#     def get(self, request, *args, **kwargs):
#         logger.debug(self.queryset)
#         ctx = {
#             "data": self.get_queryset
#         }  # 템플릿에 전달할 데이터
#         return self.render_to_response(ctx)
#
#     def get_queryset(self):
#         # if not self.queryset:
#         #     self.queryset = Post.objects.all()
#         # return self.queryset
#         self.queryset = Post.objects.all()
#         return self.queryset
#
#
# class PostDetailView(TemplateView):  # 게시글 상세
#     template_name = 'pages/post_detail.html'
#     queryset = Post.objects.all()
#
#     pk_url_kwargs = 'pk'
#
#     def get_object(self, queryset=None):
#         queryset = queryset or self.queryset
#         logger.debug(self.kwargs)
#         pk = self.kwargs.get(self.pk_url_kwargs)
#         logger.debug(pk)
#         return queryset.filter(pk=pk).first()
#
#     def get(self, request, *args, **kwargs):
#         logger.debug(self.kwargs)
#         post = self.get_object()
#         logger.debug(post)
#         if not post:
#             raise Http404('invalid pk')
#
#         ctx = {
#             "view": self.__class__.__name__,
#             "data": post
#         }  # 템플릿에 전달할 데이터
#         return self.render_to_response(ctx)
#
#
# class PostCreateUpdateView(TemplateView):
#     template_name = 'pages/post.html'
#     queryset = Post.objects.all()
#     pk_url_kwargs = 'pk'
#
#     def get_object(self, queryset=None):
#         queryset = queryset or self.queryset
#         pk = self.kwargs.get(self.pk_url_kwargs)
#         post = queryset.filter(pk=pk).first()
#
#         if pk and not post:
#             raise Http404("invalid pk")
#         return post
#
#     def get(self, request, *args, **kwargs):
#         post = self.get_object()
#
#         ctx = {
#             "post": post
#         }  # 템플릿에 전달할 데이터
#         return self.render_to_response(ctx)
#
#     def post(self, request, *args, **kwargs):
#         action = request.POST.get('action')
#         post_data = {key: request.POST.get(key) for key in ('title', 'contents')}
#         for key in post_data:
#             logger.debug(key)
#             if not post_data[key]:
#                 messages.error(self.request, '{} 값이 존재하지 않습니다.'.format(key), extra_tags='danger')
#
#         if len(messages.get_messages(request)) == 0:
#             if action == 'create':
#                 post = Post.objects.create(**post_data)
#                 messages.success(self.request, '게시글이 저장되었습니다.')
#             elif action == 'update':
#                 post = self.get_object()
#                 for key, value in post_data.items():
#                     setattr(post, key, value)
#                 post.save()
#                 messages.success(self.request, '게시글이 저장되었습니다.')
#             else:
#                 messages.error(self.request, '알 수 없는 요청입니다.', extra_tags='danger')
#
#             return HttpResponseRedirect('/board/')  # 정상적인 저장이 완료되면 '/board/'로 이동됨
#
#         ctx = {
#             'article': self.get_object() if action == 'update' else None
#         }
#         return self.render_to_response(ctx)
