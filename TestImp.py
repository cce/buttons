
class TestC(object):
    one = None
    two = None
    def __init__(self, *a, **kw):
        super(self.__class__, self).__init__(*a, **kw)
        #super(TestC, self).__init__(*a, **kw)
