# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from barcode.base import Barcode
from barcode.charsets import itf
from barcode.errors import *

"""Module: barcode.itf

:Provided barcodes: Interleaved 2 of 5
"""
__docformat__ = 'restructuredtext en'

MIN_SIZE = 0.2
MIN_QUIET_ZONE = 1


class ITF(Barcode):
    """Initializes a new ITF instance.

    :parameters:
        code : String
            ITF (Interleaved 2 of 5) numeric string
        writer : barcode.writer Instance
            The writer to render the barcode (default: SVGWriter).
        narrow: Integer
            Width of the narrow elements (default: 2)
        wide: Integer
            Width of the wide elements (default: 5)
            wide/narrow must be in the range 2..3
    """

    name = 'ITF'

    def __init__(self, code, writer=None, narrow=2, wide=5):
        if not code.isdigit():
            raise IllegalCharacterError('ITF code can only contain numbers.')
        # Length must be even, prepend 0 if necessary
        if len(code) % 2 != 0:
            code = '0' + code
        self.code = code
        self.writer = writer or Barcode.default_writer()
        self.narrow = narrow
        self.wide = wide

    def __unicode__(self):
        return self.code

    __str__ = __unicode__

    def get_fullcode(self):
        return self.code

    def build(self):
        data = itf.START
        for i in range(0, len(self.code), 2):
            bars_digit = int(self.code[i])
            spaces_digit = int(self.code[i + 1])
            for j in range(5):
                data += itf.CODES[bars_digit][j].upper()
                data += itf.CODES[spaces_digit][j].lower()
        data += itf.STOP
        raw = ''
        for e in data:
            if e == 'W':
                raw += '1' * self.wide
            if e == 'w':
                raw += '0' * self.wide
            if e == 'N':
                raw += '1' * self.narrow
            if e == 'n':
                raw += '0' * self.narrow
        return [raw]

    def render(self, writer_options, text=None):
        options = dict(
            module_width=MIN_SIZE / self.narrow,
            quiet_zone=MIN_QUIET_ZONE,
            text_distance=1,
            module_height=7
        )

        options.update(writer_options or {})
        return Barcode.render(self, options, text)
