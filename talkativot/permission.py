"""
Talkativot permission-related functions.
"""

import logging

from django.utils.text import slugify

log = logging.getLogger('talkativot')


class PermissionAlias:
    """ List of meta permissions to limit the access for a model object.
    """
    all = 'meta_all_members'
    subscribers = 'meta_subscribers'


def get_group_name(model, role=''):
    """ Create and return a permission group name as [model_name-model.id-role].

    :param model: model name
    :param role: permission group (owner, moderator, member, ...)
    :return: group name as [model_name-model.id-role]
    """
    return slugify("%s-%s-%s" % (str(type(model).__name__), str(model.id), role))


def decompose_group_name(group_name):
    """ Split group name into model-id-role and return them.

    :param group_name: group name as [model_name-model.id-role]
    :return: decomposed mode, id, and role
    """
    try:
        lst = group_name.split('-')
        model = lst.pop(0)
        role = lst.pop()
        id = '-'.join(lst)
        return model, id, role
    except IndexError:
        return None, None, None
