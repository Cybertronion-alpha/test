from django.conf.urls import url
from shop.views import home,about,buy,GigCreateView,SellerGiglist,Gigdetail_seller,Gigupdate,category_sublist,gig_sellerlist,gigdetail,gigdelete


app_name='shop'


urlpatterns=[
    url('^about/$',about,name='about'),
    url('^buy/$',buy,name='buy'),
    url(r'^creategig/',GigCreateView.as_view(),name='gigcreate'),
    url(r'^seller_giglist/',SellerGiglist.as_view(),name='giglist'),
    url(r'^gig/(?P<gigs_pk>\d+)/update/',Gigupdate.as_view(),name='gigupdate'),
    url(r'^gig/(?P<pk>\d+)/$',Gigdetail_seller.as_view(),name='seller_gigdetail'),
    url(r'^gig/(?P<pk>\d+)/delete/',gigdelete.as_view(),name='gigdelete'),

    url(r'^(?P<maincat>\w+)/(?P<subcat>\w+)/(?P<gig_id>\w+)',gigdetail.as_view(),name='gigdetail'),

    url(r'^(?P<maincat>\w+)/(?P<slug>\w+)/',gig_sellerlist.as_view(),name='gigsellerlist'),

    url(r'^(?P<maincat>\w+)/',category_sublist.as_view(),name='sublist'),
    
    
    
    
    url('^',home,name='home'),
]