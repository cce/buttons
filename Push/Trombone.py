from _Framework.Util import NamedTuple
from MelodicPattern import NoteInfo, log
import os, time
VERSION = "1-" + time.strftime('%Y-%m-%d-%H:%M:%S', time.gmtime(os.path.getmtime(os.path.abspath(__file__))))

TROMBONE = [
    [ 0, -1, -2, -3, -4, -5, -6, -7], # y=0
    [ 7,  6,  5,  4,  3,  2,  1,  0],
    [12, 11, 10,  9,  8,  7,  6,  5],
    [16, 15, 14, 13, 12, 11, 10,  9],
    [19, 18, 17, 16, 15, 14, 13, 12],
    [22, 21, 20, 19, 18, 17, 16, 15],
    [24, 23, 22, 21, 20, 19, 18, 17],
    [28, 27, 26, 25, 24, 23, 22, 21], # y=7
]

class TrombonePattern(NamedTuple):
    first_note = 0
    steps = [0, 0]
    scale = range(12)
    octave = 0
    origin = [0, 0]
    is_diatonic = True
    is_absolute = False
    left_handed = False

    def __init__(self, *args, **kw):
        kw['left_handed'] = kw.get('direction') == 'rl'
        # avoids TypeError http://stackoverflow.com/a/18476192/112380
        super(self.__class__, self).__init__(*args, **kw)
        log.debug("TrombonePattern() args %r kw %r", args, kw)

    def _get_trombone(self, x, y, channel=0):
        Bb = 46
        C = 48
        Bb_off = 10

        if self.left_handed:
            x = -(x+1) % 8

        if self.is_absolute: # fixed 0,0 = Bb
            octave_off = 3
            index = TROMBONE[y][x] + Bb
        else: # transpose trombone to selected key
            octave_off = 4 if (self.scale[0] >= 10) else 3
            index = TROMBONE[y][x] + C + self.scale[0]
        index +=  + (self.octave - octave_off) * 12

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
        if x==0 and y==0:
            log.info("_get_trombone(%r, %r, %r)\tabs %r\torigin %r\tret %s", x, y, channel,
                     self.is_absolute, self.origin, ret)
        return ret

    def note(self, x, y):
        ret = self._get_trombone(x, y, x+5)
        #log.debug("TP.note(%r, %r) returning %s", x, y, ret)
        return ret

    def __getitem__(self, i):
        ret = self._get_trombone(i, 0)
        #log.debug("TP.__getitem__(%r) returning %s", i, ret)
        return ret
