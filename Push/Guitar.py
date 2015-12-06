from _Framework.Util import NamedTuple
from MelodicPattern import NoteInfo, log
import os, time
VERSION = "1-" + time.strftime('%Y-%m-%d-%H:%M:%S', time.gmtime(os.path.getmtime(os.path.abspath(__file__))))

GUITAR = [
    [-5, -4, -3, -2, -1,  0,  1,  2], # y=0
    [ 0,  1,  2,  3,  4,  5,  6,  7],
    [ 5,  6,  7,  8,  9, 10, 11, 12],
    [10, 11, 12, 13, 14, 15, 16, 17],
    [15, 16, 17, 18, 19, 20, 21, 22],
    [19, 20, 21, 22, 23, 24, 25, 26],
    [24, 25, 26, 27, 28, 29, 30, 31],
    [29, 30, 31, 32, 33, 34, 35, 36], # y=7
]

class GuitarPattern(NamedTuple):
    first_note = 0
    steps = [0, 0]
    scale = range(12)
    octave = 0
    origin = [0, 0]
    is_diatonic = True
    is_absolute = False

    def __init__(self, *args, **kw):
        super(self.__class__, self).__init__(*args, **kw) # avoids TypeError http://stackoverflow.com/a/18476192/112380
        log.debug("GuitarPattern() args %r kw %r", args, kw)

    def _get(self, x, y, channel=0):
        #if self.left_handed:
        #    x = -(x+1) % 8

        if self.is_absolute:
            E = 40 # 44
            index = GUITAR[y][x] + E + (self.octave - 3) * 12
        else: # chromatic or diatonic
            index = GUITAR[y][x] + self.first_note

        # pick color
        if (index % 12) == (self.scale[0] % 12):
            color = 'NoteBase'
        elif (index % 12) == ((self.scale[0] + 7) % 12):
            color = 'NoteFifth'
        elif not self.is_diatonic or (index % 12) in ((i % 12) for i in self.scale):
            color = 'NoteScale'
        else:
            color = 'NoteNotScale'

        ret = NoteInfo(index=index, channel=channel, color=color)
        log.info("_get(%r, %r, %r)\tabs %r\torigin %r\tret %s", x, y, channel,
                 self.is_absolute, self.origin, ret)
        return ret

    def note(self, x, y):
        ret = self._get(x, y, x+5)
        #log.debug("TP.note(%r, %r) returning %s", x, y, ret)
        return ret

    def __getitem__(self, i):
        ret = self._get(i, 0)
        #log.debug("TP.__getitem__(%r) returning %s", i, ret)
        return ret
