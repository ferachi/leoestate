from django import template

from estate.models import Answer

register = template.Library()


@register.filter(name='likes')
def vote_likes(value, is_like=True):
    if type(value) == Answer:
        if is_like:
            likes = value.votes.filter(is_like=True)
        else:
            likes = value.votes.filter(is_like=False)
        return likes.count()
    return 0