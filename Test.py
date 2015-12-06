import TestImp

def main():
    reload(TestImp)
    c = TestImp.TestC(one=1, two=2)
    print "c", c._eq_dict
    cls = getattr(TestImp, 'TestC')
    d = cls(one=4, two=3)
    print "d", d._eq_dict

if __name__ == '__main__':
    main()
