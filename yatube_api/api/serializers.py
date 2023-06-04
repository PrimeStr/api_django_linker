from posts.models import Comment, Post, Group, Follow, User
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (ModelSerializer,
                                        CurrentUserDefault,
                                        UniqueTogetherValidator,
                                        ValidationError,
                                        PrimaryKeyRelatedField)


class PostSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    
    class Meta:
        fields = ('id', 'author', 'group', 'text', 'pub_date', 'image')
        model = Post


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class FollowSerializer(ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=CurrentUserDefault()
    )
    following = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )
    
    class Meta:
        fields = ('user', 'following')
        model = Follow
        # UniqueTogetherValidator используется для проверки кортежа;
        # Который должен составлять уникальный набор полей.
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                message='You can\'t subscribe to yourself.',
                fields=('user', 'following',),
            )
        ]
    
    def validate(self, data):
        following = data.get('following')
        user = self.context['request'].user
        if user == following:
            raise ValidationError(
                'Don\'t you subscribe to yourself?'
            )
        return data
