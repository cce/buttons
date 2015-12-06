import TestImp

def do_a_thing():
    reload(TestImp)
    c = TestImp.TestC(one=1, two=2)
