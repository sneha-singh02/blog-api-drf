from rest_framework import generics, status
from rest_framework.response import Response
from .models import BlogPost
from .serializers import BlogPostSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi





class BlogPostListCreate(generics.ListCreateAPIView):
    """
    get:
    Return a list of all blog posts.
    Supports filtering by title using a query parameter (?title=some-title).

    post:
    Create a new blog post with title and content.
    """
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        title = self.request.query_params.get("title", "")
        queryset = BlogPost.objects.all()

        if title:
            queryset = queryset.filter(title__icontains=title)

        return queryset.order_by("-published_date")

    # Swagger documentation for GET (list with filter)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'title',
                openapi.IN_QUERY,
                description="Filter blog posts by title (case-insensitive)",
                type=openapi.TYPE_STRING,
                required=False,
                example="Django"
            )
        ]
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # Swagger documentation for POST (create)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'content'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, example="My First Post"),
                'content': openapi.Schema(type=openapi.TYPE_STRING, example="This is the content of my first blog post."),
            },
        ),
        responses={
            201: openapi.Response(
                description="Blog post created successfully",
                schema=BlogPostSerializer()
            ),
            400: "Bad Request – Missing or invalid fields",
        }
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class BlogPostRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Retrieve a specific blog post by its ID.

    put:
    Update an existing blog post entirely.

    patch:
    Update one or more fields of an existing blog post.

    delete:
    Delete a blog post by its ID.
    """

    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = "pk"

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Blog post retrieved successfully",
                schema=BlogPostSerializer()
            ),
            404: "Not Found – Blog post with given ID does not exist",
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'content'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, example="Updated Title"),
                'content': openapi.Schema(type=openapi.TYPE_STRING, example="Updated content for the blog post."),
            },
        ),
        responses={
            200: openapi.Response(
                description="Blog post updated successfully",
                schema=BlogPostSerializer()
            ),
            400: "Bad Request Invalid input",
            404: "Not Found  Blog post not found",
        }
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, example="Optional new title"),
                'content': openapi.Schema(type=openapi.TYPE_STRING, example="Optional new content"),
            },
        ),
        responses={
            200: openapi.Response(
                description="Blog post partially updated",
                schema=BlogPostSerializer()
            ),
            400: "Bad Request – Invalid patch data",
            404: "Not Found – Blog post not found",
        }
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            204: "No Content – Blog post deleted successfully",
            404: "Not Found – Blog post not found",
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
