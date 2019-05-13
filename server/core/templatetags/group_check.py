from django import template

register = template.Library()


@register.filter
def group_check(user, args):
    if args is None:
        return False
    groups = [arg.strip() for arg in args.split(',')]
    return user.groups.filter(name__in=groups).exists() or user.is_superuser
