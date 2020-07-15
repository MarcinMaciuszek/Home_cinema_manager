def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class GlobalSingletonDict():
    def __init__(self, *args, **kwargs):
        self.storages = {}

    def __getitem__(self, key):
        return self.storages[key]

    def __setitem__(self, key, value):
        self.storages[key] = value

    def __missing__(self, key):
        self.storages[key] = []
        return self.storages[key]
