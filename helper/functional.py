class Composition:

    def __init__(self, *fs):
        self.fs = fs

    def __call__(self, argument):
        x = argument
        for f in self.fs:
            x = f(x)
        return x