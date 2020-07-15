from singleton import GlobalSingletonDict


def get_application_variable(variable):
    instance = GlobalSingletonDict()
    return getattr(instance['app'], variable)


def get_settings_variable(variable):
    instance = GlobalSingletonDict()
    return getattr(instance['settings'], variable)


def get_event_variable(variable):
    instance = GlobalSingletonDict()
    return getattr(instance['event'], variable)


def get_event_method(method):
    instance = GlobalSingletonDict()
    return getattr(instance['event'], method)


def set_application_variable(variable, value):
    instance = GlobalSingletonDict()
    setattr(instance['app'], variable, value)

