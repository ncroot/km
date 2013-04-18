from inspect import getmembers, ismethod

def monkey_mix(cls, mixin):
    for name, method in getmembers(mixin, ismethod):
        setattr(cls, name, method.im_func)
