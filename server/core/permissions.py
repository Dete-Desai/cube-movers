# Simple tests to see if a user belongs to a particular Group


def is_superuser(user):
    return user.is_superuser


def can_view_inquiry(user):
    groups = ['customer_care']
    return user.groups.filter(name__in=groups).exists() or user.is_superuser


def can_view_pre_survey(user):
    groups = ['customer_care']
    return user.groups.filter(name__in=groups).exists() or user.is_superuser


def can_view_surveys(user):
    groups = ['customer_care', 'move_reps']
    return user.groups.filter(name__in=groups).exists() or user.is_superuser


def can_view_quotes(user):
    groups = ['customer_care', 'move_reps']
    return user.groups.filter(name__in=groups).exists() or user.is_superuser


def can_view_invoice(user):
    groups = ['manager', 'accountant']
    return user.groups.filter(name__in=groups).exists() or user.is_superuser


def can_view_pre_move(user):
    groups = ['move_manager']
    return user.groups.filter(name__in=groups).exists() or user.is_superuser


def can_view_move(user):
    groups = ['move_manager', 'move_supervisor', 'movers']
    return user.groups.filter(name__in=groups).exists() or user.is_superuser


def can_view_post_move(user):
    groups = [
        'move_manager', 'move_supervisor', 'quality_assuarance', 'movers'
    ]
    return user.groups.filter(name__in=groups).exists() or user.is_superuser


def can_view_complete_move(user):
    groups = [
        'move_manager', 'move_supervisor', 'quality_assuarance', 'movers'
    ]
    return user.groups.filter(name__in=groups).exists() or user.is_superuser
