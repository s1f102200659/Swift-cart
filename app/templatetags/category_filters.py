from django import template

register = template.Library()

CATEGORY_MAP = {
    1: '食料品',
    2: '衣類',
    3: '小物',
    4: '生活用品',
    5: 'デバイス',
}

@register.filter
def category_name(value):
    return CATEGORY_MAP.get(value,) 