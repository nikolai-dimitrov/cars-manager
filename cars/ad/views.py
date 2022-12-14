from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.paginator import Paginator

from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, FormView, DetailView, UpdateView, DeleteView, CreateView

from cars.ad.forms import AdCreateForm, AdEditForm
from cars.ad.models import Ad, Bookmark
from cars.core.decorators import profile_required
from cars.core.mixins import AssignDataUpdateAdForm
from cars.profiles.models import Profile
import json


# Create your views here.

class AdCreateView(CreateView, AssignDataUpdateAdForm):
    model = Ad
    template_name = 'ad/ad-make.html'
    form_class = AdCreateForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        ad = form.save(commit=False)
        ad.profile = Profile.objects.get(pk=self.request.user.pk)
        self.update_images(ad, form)
        ad.save()
        return redirect(self.success_url)

    def get_user_profile(self):
        profile = Profile.objects.get(pk=self.request.user.pk)
        return profile


@method_decorator(profile_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ShowAdsView(FormView, Paginator):
    template_name = 'ad/show-ads.html'
    form_class = AdCreateForm

    __ALLOWED_FIELDS = [
        'model',
        'car',
        'title',
        'price',
        'year_of_manufacture',
        'body_type',
        'transmission',
        'city',
        'fuel'
    ]

    # def filter_ads(self, title, ads):
    #     pass
    def get(self, request, *args, **kwargs):
        obj_list = self.get_context_data()

        paginator = Paginator(obj_list['cars'], 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'ad_set': obj_list['cars'],
            'form': obj_list['form'],

        }
        return self.render_to_response(context)
    def render_to_response(self, context, **response_kwargs):
        return super().render_to_response()
    def get_context_data(self, **kwargs):
        filters = self.request.session.get('last_filters') or '{}'
        filters = json.loads(filters)

        cars = Ad.objects.filter(**filters)
        cars = cars.filter(profile__is_banned=False)

        self.extra_context = {'cars': cars}
        return super().get_context_data()

    def form_valid(self, form):
        filters = {k: v for k, v in form.data.items() if k in self.__ALLOWED_FIELDS and v}
        flt = json.dumps(filters)
        self.request.session['last_filters'] = flt
        return self.get(self.request, filters=filters)

    def form_invalid(self, form):
        return self.form_valid(form=form)


@method_decorator(profile_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AdEditView(UpdateView, AssignDataUpdateAdForm):
    form_class = AdEditForm
    model = Ad
    template_name = 'ad/ad-edit.html'

    def get_success_url(self):
        return reverse_lazy('details ad', kwargs={'pk': self.object.pk})

    def get(self, request, *args, **kwargs):
        try:
            ad = Ad.objects.get(pk=self.kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404()
        if ad not in request.user.profile.ad_set.all():
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.save(commit=False)
        ad = Ad.objects.get(pk=data.pk)
        self.asign_data(ad, form)
        self.update_images(ad, form)
        ad.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ad'] = self.get_object()
        return context


@method_decorator(profile_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AdDeleteView(DeleteView):
    template_name = 'ad/ad-delete.html'
    model = Ad
    success_url = reverse_lazy('details profile')

    def get(self, request, *args, **kwargs):
        try:
            ad = Ad.objects.get(pk=self.kwargs['pk'])
        except ObjectDoesNotExist:
            raise Http404()

        if ad not in request.user.profile.ad_set.all():
            raise PermissionDenied()

        return super().get(request, *args, **kwargs)


@method_decorator(profile_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AdDetailsView(DetailView):
    model = Ad
    template_name = 'ad/ad-details.html'

    def get(self, request, *args, **kwargs):
        ad = self.get_object()
        if ad.profile.is_banned:
            raise Http404()
        else:
            return super().get(self, request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class CreateDeleteBookmarkView(View):
    model = Bookmark

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=request.user.pk)
        ad_pk = request.GET.get('ad_pk')

        if ad_pk is None:
            return redirect('show ads')

        ad = Ad.objects.get(pk=ad_pk)
        bookmarks = self.model.objects.filter(profile=profile, ad=ad)

        if not bookmarks:
            self.model.objects.create(ad=ad, profile=profile)
        else:
            bookmarks[0].delete()
        return redirect('show ads')


@method_decorator(profile_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ListBookmarksView(ListView):
    model = Bookmark
    template_name = 'ad/ad-favourites.html'
    paginate_by = 3

    def get_queryset(self):
        bookmarks = Bookmark.objects.filter(profile_id=self.request.user.pk)

        queryset = Ad.objects.filter(bookmark__in=bookmarks)
        queryset = queryset.filter(profile__is_banned=False)

        return queryset


def remove_bookmark(request, pk):
    profile = Profile.objects.get(pk=request.user.pk)

    bookmark = Bookmark.objects.get(ad=pk, profile=profile)
    bookmark.delete()

    return redirect('list bookmarks')
