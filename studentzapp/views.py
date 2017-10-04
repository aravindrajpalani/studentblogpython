from rest_framework import generics, permissions
from .serializers import AccountSerializer
from .models import Account
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import facebook
from rest_framework import generics
from .serializers import BlogPostSerializer,LikeSerializer,UserFollowingSerializer
from .models import BlogPost,Like,UserFollowing
from .permissions import IsOwner
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist

class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwner)


    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        print ("user="+self.request.user.displayname)
        print(serializer.validated_data)
        print(dir(serializer))
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

class CreateLikeView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwner)


    def post(self, request, *args, **kwargs):
        
        data = self.request.data
        a=BlogPost.objects.get(id=data['postid'])
        try:
            likeobj=Like.objects.get(postid=data['postid'],ownerfbid=self.request.user)
            if likeobj.isliked:
               likeobj.isliked=False
               a.likescount=a.likescount-1
               a.likes.remove(likeobj)
               print("isliked=true")
            else:
               likeobj.isliked=True
               a.likescount=a.likescount+1
               a.likes.add(likeobj)
               print("isliked=false")
            likeobj.post=a
            likeobj.save()
            a.save()
            test = {"isliked":likeobj.isliked}
            return Response(test, status=200)


        except Like.DoesNotExist:
            likeobj=Like.objects.create(post=a,postid=data['postid'],ownerfbid=self.request.user,ownername=self.request.user,isliked=True,user=self.request.user)
            a.likescount=a.likescount+1
            a.likes.add(likeobj)
            a.save()
            test = {"isliked":likeobj.isliked}
            return Response(test, status=200)
        

        

        
        # obj, created = Like.objects.update_or_create(postid=data['postid'],ownerfbid=self.request.user,ownername=self.request.user,defaults={'postid': data['postid'],'ownerfbid': self.request.user,'ownername': self.request.user,'isliked':islikeds})
        # a=BlogPost.objects.get(id=data['postid'])
        # if data['postid']:
        #   a.likescount=a.likescount+1
        # else:
        #   a.likescount=a.likescount-1
        # a.save()
        
class CreateUserFollowingView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = UserFollowing.objects.all()
    serializer_class = UserFollowingSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwner)

    def post(self, request, *args, **kwargs):
       
        data = self.request.data
        serializer = self.get_serializer(data=request.data)
        ids=self.kwargs['userid']
        print ("="+ids)  
        # instance =serializer.save(displayname=profile['name'],fbid=profile['id'],accesstoken="")
        test = {"token":""}
        return Response(test, status=200)






class DetailsView(APIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwner)

    def get(self, request, format=None):
        dishes = BlogPost.objects.all()
        return_list = []
        likeslist=[]
        for dish in dishes:
          ad=dish.like_set.filter(user=request.user).values('postid')
          print (ad[0]['postid'])
          for f in ad:
            print (f['postid'])
            likeslist.append(f['postid'])
          return_list.append(({'postid': dish.id,'likedusers': likeslist}))

        return Response(return_list,status=200)
           
   

class DetailsLikeView(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        postid = self.kwargs['postid']
        return Like.objects.filter(postid=postid)

class GetLikes(generics.ListAPIView):
    serializer_class = LikeSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        postid = self.kwargs['postid']
        return Like.objects.filter(postid=postid,isliked=True)

class CreateAccountView(generics.ListCreateAPIView):
    """This class handles the GET and POSt requests of our rest api."""
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def post(self, request, *args, **kwargs):
        print("post method")
        data = self.request.data
        serializer = self.get_serializer(data=request.data)
        print ("="+data['accesstoken'] )
        graph=facebook.GraphAPI(data['accesstoken'])
        args={'fields':'id,name,email'}
        profile=graph.get_object('me',**args)
        print ("dict="+profile['name'] )
        serializer.is_valid(raise_exception=True)
        instance =serializer.save(displayname=profile['name'],fbid=profile['id'],accesstoken="")
        token=Token.objects.get(user=instance)
        print ("viewtoken="+token.key)
        test = {"token":token.key}
        return Response(test, status=200)

    # def perform_create(self, serializer):
    #     """Save the post data when creating a new bucketlist."""
    #     data = self.request.data
    #     print ("="+data['accesstoken'] )
    #     graph=facebook.GraphAPI(data['accesstoken'])
    #     args={'fields':'id,name,email'}
    #     profile=graph.get_object('me',**args)
    #     print ("dict="+profile['name'] )
        
    #     instance =serializer.save(displayname=profile['name'],fbid=profile['id'])
    #     token=Token.objects.get(user=instance)
    #     print ("viewtoken="+token.key)