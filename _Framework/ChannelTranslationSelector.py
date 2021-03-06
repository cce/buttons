# Embedded file name: /Users/versonator/Jenkins/live/Binary/Core_Release_64_static/midi-remote-scripts/_Framework/ChannelTranslationSelector.py
from __future__ import absolute_import
from .InputControlElement import InputControlElement
from .ModeSelectorComponent import ModeSelectorComponent

class ChannelTranslationSelector(ModeSelectorComponent):
    """ Class switches modes by translating the given controls' message channel """

    def __init__(self, num_modes = 0, *a, **k):
        super(ChannelTranslationSelector, self).__init__(*a, **k)
        self._controls_to_translate = None
        self._initial_num_modes = num_modes
        return

    def disconnect(self):
        ModeSelectorComponent.disconnect(self)
        self._controls_to_translate = None
        return

    def set_controls_to_translate(self, controls):
        raise self._controls_to_translate == None or AssertionError
        raise controls != None or AssertionError
        raise isinstance(controls, tuple) or AssertionError
        for control in controls:
            raise isinstance(control, InputControlElement) or AssertionError

        self._controls_to_translate = controls
        return

    def number_of_modes(self):
        result = self._initial_num_modes
        if result == 0 and self._modes_buttons != None:
            result = len(self._modes_buttons)
        return result

    def update(self):
        super(ChannelTranslationSelector, self).update()
        if self._controls_to_translate != None:
            for control in self._controls_to_translate:
                control.use_default_message()
                if self.is_enabled():
                    control.set_channel((control.message_channel() + self._mode_index) % 16)

        return