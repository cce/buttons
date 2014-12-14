# Embedded file name: /Users/versonator/Jenkins/live/Binary/Core_Release_64_static/midi-remote-scripts/Push/MelodicPattern.py
# pylint: disable=W0232,C0111,C0301,F0401
from _Framework.Util import NamedTuple, lazy_attribute, memoize
import logging
logging.basicConfig(
    level=logging.DEBUG,
    filename='/Users/cce/push/MelodicPattern.log',
    format='%(asctime)s %(process)d %(name)s %(levelname)s %(message)s',
)
log = logging.getLogger(__name__)

import consts
NOTE_NAMES = ('C', 'D\x1b', 'D', 'E\x1b', 'E', 'F', 'G\x1b', 'G', 'A\x1b', 'A', 'B\x1b', 'B')

def pitch_index_to_string(index):
    if 0 <= index < 128:
        return NOTE_NAMES[index % 12] + str(index / 12 - 2)
    return consts.CHAR_ELLIPSIS


class Scale(NamedTuple):
    name = ''
    notes = []


class Modus(Scale):

    def __str__(self):
        return self.name

    def scale(self, base_note):
        return Scale(name=NOTE_NAMES[base_note], notes=[ base_note + x for x in self.notes ])

    @memoize
    def scales(self, base_notes):
        return [ self.scale(b) for b in base_notes ]


class NoteInfo(NamedTuple):
    index = None
    channel = 0
    color = 'NoteInvalid'
    def __str__(self):
        return ("NoteInfo(index=%r, channel=%r, color=%r)" %
                (self.index, self.channel, self.color))

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

class MelodicPattern(NamedTuple):
    steps = [0, 0]
    scale = range(12)
    base_note = 0
    origin = [0, 0]
    chromatic_mode = False
    custom_mode = None

    def __init__(self, *args, **kw):
        log.info("MelodicPattern() args %r kw %r", args, kw)
        super(MelodicPattern, self).__init__(*args, **kw)

    @lazy_attribute
    def extended_scale(self):
        if self.chromatic_mode:
            first_note = self.scale[0]
            return range(first_note, first_note + 12)
        else:
            return self.scale

    @property
    def is_aligned(self):
        return not self.origin[0] and not self.origin[1] and abs(self.base_note) % 12 == self.extended_scale[0]

    def _get_trombone(self, x, y, base_note, channel=0):
        tbn = TROMBONE[y][x]
        if (tbn % 12) == 0:
            color = 'NoteBase'
        elif (tbn % 12) in self.scale:
            color = 'NoteScale'
        else:
            color = 'NoteNotScale'
        ret = NoteInfo(index=tbn+base_note, channel=channel, color=color)
        log.info("_get_trombone(%r, %r, %r, %r) origin %r returning %s", x, y, base_note, channel, self.origin, ret)
        return ret

    def note(self, x, y):
        if self.custom_mode == 'etbn':
            ret = self._get_trombone(x, y, self.base_note, x+5)
        else:
            ret = self._get_note_info(self._octave_and_note(x, y), self.base_note, x + 5)
        log.info("note(%r, %r) returning %s", x, y, ret)
        return ret

    def __getitem__(self, i):
        base_note = self.base_note
        if base_note <= -12:
            base_note = 0 if self.is_aligned else -12
        if self.custom_mode == 'etbn':
            ret = self._get_trombone(i, 0, base_note)
        else:
            ret = self._get_note_info(self._octave_and_note_linear(i), base_note)
        log.info("__getitem__(%r) returning %s", i, ret)
        return ret

    def _octave_and_note_by_index(self, index):
        scale = self.extended_scale
        scale_size = len(scale)
        octave = index / scale_size
        note = scale[index % scale_size]
        log.info("_octave_and_note_by_index(%r) returning %r", index, (octave, note))
        return (octave, note)

    def _octave_and_note(self, x, y):
        index = self.steps[0] * (self.origin[0] + x) + self.steps[1] * (self.origin[1] + y)
        ret = self._octave_and_note_by_index(index)
        log.info("_octave_and_note(%r) returning %r", index, ret)
        return ret

    def _color_for_note(self, note):
        if note == self.scale[0]:
            return 'NoteBase'
        elif note in self.scale:
            return 'NoteScale'
        else:
            return 'NoteNotScale'

    def _get_note_info(self, (octave, note), base_note, channel = 0):
        note_index = 12 * octave + note + base_note
        if 0 <= note_index <= 127:
            return NoteInfo(index=note_index, channel=channel, color=self._color_for_note(note))
        else:
            return NoteInfo()

    def _octave_and_note_linear(self, i):
        origin = self.origin[0] or self.origin[1]
        index = origin + i
        return self._octave_and_note_by_index(index)
