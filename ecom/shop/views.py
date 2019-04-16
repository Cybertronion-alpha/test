from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views .generic import ListView,DetailView,TemplateView
from .forms import gigform
from django.urls import reverse_lazy
from .models import Gigs,Category
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Category,Gigs
from accounts.models import merchantprofile
from django.core.exceptions import PermissionDenied


def home(request):
    cat=Category.CATEGORY_CHOICES

    return render(request,'account/home.html',{'cat':cat})

def about(request):
    return render(request,'shop/about.html')

def buy(request):
    return render(request,'categories.html')

#for merchant
class GigCreateView(CreateView):
    form_class=gigform
    template_name='shop/merchant/gigform.html'
    success_url=reverse_lazy('userprofile')

    def form_valid(self,form):
        form.save(commit=False)
        form.instance.user=self.request.user
        form.save()
        return super().form_valid(form)

class SellerGiglist(ListView):
    model=Gigs
    template_name='shop/merchant/seller-gigs.html'
    def get_queryset(self):
        obj=Gigs.objects.filter(user=self.request.user)
        return obj

class Gigdetail_seller(DetailView):
    model=Gigs
    template_name='shop/merchant/seller_gigdetail.html'

    def get_context_data(self,**kwargs):
        # gig_id=self.kwargs.get(kwargs['pk'])
        context={}
        context['obj']=Gigs.objects.get(pk=self.kwargs.get('pk'))
        return context

class Gigupdate(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Gigs
    form_class=gigform
    pk_url_kwarg='gigs_pk'
    template_name='shop/merchant/gigform.html'
    context_object_name='gig'
    success_url=reverse_lazy('shop:gigdetail')
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    def test_func(self):
        gig=self.get_object()
        if self.request.user==gig.user:
            return True
        else:
            return False


    def form_valid(self,form):
        gig=form.save()
        return redirect('shop:gigdetail',pk=gig.pk)

class gigdelete(DeleteView,LoginRequiredMixin):
    model=Gigs
    success_url=reverse_lazy('shop:giglist')
    template_name='shop/merchant/confirm_delete.html'

    def form_valid(self,**kwargs):
        if method=="POST" :
            obj=get_object_or_404(Gigs,id=pk)
            if  form.is_valid and obj.user==self.request.user:
                obj.delete()
                return redirect(reverse('shop:giglist'))
            else:
                raise PermissionDenied

        else:
            return redirect('shop:giglist')
            


# class Giglist(ListView):
#     model=Gigs
#     template_name='shop/seller-gigs.html'
#     def get_queryset(self,**kwargs):
#         obj=Gigs.objects.filter(Category.slug=self.kwargs.get('slug'))
#         return obj

# for customer

class category_sublist(TemplateView):
    model=Category
    template_name='shop/customer/subcat_list.html'
    def get_context_data(self,**kwargs):
        context=super(category_sublist,self).get_context_data(**kwargs)
        context['main_cat']=Category.CATEGORY_CHOICES
        context['sub_cat']=Category.objects.filter(parent=self.kwargs.get('maincat'))
        return context

    
class gig_sellerlist(TemplateView):
    model=Gigs
    template_name='shop/customer/gig_seller.html'
    

    def get_context_data(self,**kwargs):
        context=super(gig_sellerlist,self).get_context_data(**kwargs)
        context['main_cat']=Category.CATEGORY_CHOICES
        context['sub_cat']=Category.objects.filter(slug=self.kwargs.get('slug'))
        context['obj']=Gigs.objects.filter(category=Category.objects.get(slug=self.kwargs.get('slug')))
        return context
    # def get_queryset(self,**kwargs):
    #     obj=Gigs.objects.filter(category=Category.objects.get(slug=self.kwargs.get('slug')))
    #     print(obj)
    #     return obj

class gigdetail(TemplateView):
    model=Gigs
    template_name='shop/customer/gigdetail.html'

    def get_context_data(self,**kwargs):
        context=super(gigdetail,self).get_context_data(**kwargs)
        context['main_cat']=Category.CATEGORY_CHOICES
        context['sub_cat']=Category.objects.filter(slug=self.kwargs.get('subcat'))
        context['gig_obj']=Gigs.objects.get(id=self.kwargs.get('gig_id'))
        return context


    