from _Framework.Util import NamedTuple
from MelodicPattern import NoteInfo, log

TROMBONE = [
    [ 0, -1, -2, -3, -4, -5, -6, -7], # y=0
    [ 7,  6,  5,  4,  3,  2,  1,  0],
    [12, 11, 10,  9,  8,  7,  6,  5],
    [16, 15, 14, 13, 12, 11, 10,  9],
    [19, 18, 17, 16, 15, 14, 13, 12],
    [22, 21, 20, 19, 18, 17, 16, 15],
    [24, 23, 22, 21, 20, 19, 18, 17],
    [28, 27, 26, 25, 24, 23, 22, 21], #, 20, 19], # y=7
]

class TrombonePattern(NamedTuple):
    steps = [0, 0]
    scale = range(12)
    base_note = 0
    origin = [0, 0]
    chromatic_mode = False
    is_absolute = None

    def __init__(self, *args, **kw):
        log.debug("TrombonePattern() args %r kw %r", args, kw)
        super(self.__class__, self).__init__(*args, **kw)

    def _get_trombone(self, x, y, base_note, channel=0):
        if self.is_absolute:
            Bb = 46 # XXX octave
            tbn = TROMBONE[y][x] + Bb

        tbn = TROMBONE[y][x] + self.origin[0]
        if (tbn % 12) == self.scale[0]:
            color = 'NoteBase'
        elif (tbn % 12) in self.scale:
            color = 'NoteScale'
        else:
            color = 'NoteNotScale'
        ret = NoteInfo(index=tbn+base_note, channel=channel, color=color)
        log.info("_get_trombone(%r, %r, %r, %r) origin %r returning %s", x, y, base_note, channel, self.origin, ret)
        return ret

    def note(self, x, y):
        ret = self._get_trombone(x, y, self.base_note, x+5)
        log.info("TP.note(%r, %r) returning %s", x, y, ret)
        return ret

    def __getitem__(self, i):
        base_note = self.base_note
        if base_note <= -12:
            base_note = 0 if self.is_aligned else -12
        ret = self._get_trombone(i, 0, base_note)
        log.info("TP.__getitem__(%r) returning %s", i, ret)
        return ret
