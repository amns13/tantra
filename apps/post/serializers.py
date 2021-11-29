from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = (
            'uuid',
            'title',
            'body',
            'author',
            'created_at',
        )
        read_only_fields = (
            'author',
            'created_at',
        )
