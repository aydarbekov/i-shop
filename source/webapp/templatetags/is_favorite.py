from django import template
register = template.Library()


@register.filter
def is_favorite(product, user):
    return user.favorites.filter(product=product.pk).count() > 0

