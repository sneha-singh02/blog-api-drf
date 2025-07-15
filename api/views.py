from rest_framework import generics, status
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer

class BlogPostListCreate(generics.ListCreateAPIView):
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        title = self.request.query_params.get("title", "")
        queryset = BlogPost.objects.all()

        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset.order_by("-published_date")
    
    
class BlogPostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = "pk"
