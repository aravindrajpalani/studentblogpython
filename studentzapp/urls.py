from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateAccountView,CreateView,DetailsView,CreateLikeView,DetailsLikeView,GetLikes
from .models import Account
from .serializers import AccountSerializer





urlpatterns = {
   url(r'^users/', CreateAccountView.as_view(queryset=Account.objects.all(), serializer_class=AccountSerializer), name='user-list'),
   url(r'^blogposts/$', CreateView.as_view(), name="create"),
   url(r'^blogposts', DetailsView.as_view(), name="details"),
   url(r'^like/$', CreateLikeView.as_view(), name="create"),
   url(r'^like/(?P<postid>.+)/$', GetLikes.as_view(), name="details"),
  
 

}

urlpatterns = format_suffix_patterns(urlpatterns)

