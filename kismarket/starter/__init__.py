# -*- coding: utf-8 -*-

from django.contrib.auth import create_superuser
from django.contrib.auth.models import User, AnonymousUser
from django.db.models import signals
from django.contrib.auth import models as auth_models
from kismarket.starter.helper.monkey import monkey_mix
from kismarket.starter.helper.user_mixin import UserMixin, AnonymousUserMixin

signals.post_syncdb.disconnect(create_superuser, sender=auth_models, dispatch_uid="django.contrib.auth.management.create_superuser")

monkey_mix(User, UserMixin)
monkey_mix(AnonymousUser, AnonymousUserMixin)
