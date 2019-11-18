class Bunch(dict):
    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        if key not in self:
            return None
        return self[key]


def apply(func, args):
    for arg in args:
        func(arg)
