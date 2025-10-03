"""
Consolidated QRCode Library

Generated automatically from python-qrcode using bundler.py
All internal imports have been resolved and removed.

This is a derivative work of python-qrcode:
https://github.com/lincolnloop/python-qrcode

Original LICENSE:
------------------------------------------------------------------------------
Copyright (c) 2011, Lincoln Loop
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the package name nor the names of its contributors may be
      used to endorse or promote products derived from this software without
      specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


-------------------------------------------------------------------------------


Original text and license from the pyqrnative package where this was forked
from (http://code.google.com/p/pyqrnative):

#Ported from the Javascript library by Sam Curren
#
#QRCode for Javascript
#http://d-project.googlecode.com/svn/trunk/misc/qrcode/js/qrcode.js
#
#Copyright (c) 2009 Kazuhiko Arase
#
#URL: http://www.d-project.com/
#
#Licensed under the MIT license:
#   http://www.opensource.org/licenses/mit-license.php
#
# The word "QR Code" is registered trademark of
# DENSO WAVE INCORPORATED
#   http://www.denso-wave.com/qrcode/faqpatent-e.html
------------------------------------------------------------------------------
"""

from __future__ import annotations

import abc
import datetime
import decimal
import math
import optparse
import os
import re
import sys
import warnings
import xml.etree.ElementTree

from bisect import bisect_left
from decimal import Decimal
from importlib import metadata
from importlib.util import find_spec
from itertools import chain
from pathlib import Path
from typing import Any
from typing import Generic
from typing import Literal
from typing import NamedTuple
from typing import NoReturn
from typing import Optional
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import cast
from typing import overload


# Optional dependencies (may not be installed)
try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = None
    ImageDraw = None

# Patch metadata.version to handle missing package metadata
_original_metadata_version = metadata.version
def _patched_metadata_version(name):
    try:
        return _original_metadata_version(name)
    except Exception:
        return 'consolidated'
metadata.version = _patched_metadata_version

# Namespace class to hold module-level definitions
class _ModuleNamespace:
    pass

# Create namespace hierarchy
qrcode = _ModuleNamespace()
qrcode.image = _ModuleNamespace()
qrcode.constants = _ModuleNamespace()
qrcode.exceptions = _ModuleNamespace()
qrcode.image.styles = _ModuleNamespace()
qrcode.image.styles.moduledrawers = _ModuleNamespace()
qrcode.image.styles.moduledrawers.base = _ModuleNamespace()
qrcode.image.base = _ModuleNamespace()
qrcode.image.pil = _ModuleNamespace()
qrcode.base = _ModuleNamespace()
qrcode.LUT = _ModuleNamespace()
qrcode.util = _ModuleNamespace()
qrcode.compat = _ModuleNamespace()
qrcode.compat.png = _ModuleNamespace()
qrcode.image.pure = _ModuleNamespace()
qrcode.main = _ModuleNamespace()
qrcode.console_scripts = _ModuleNamespace()
qrcode.__main__ = _ModuleNamespace()
qrcode.compat.etree = _ModuleNamespace()
qrcode.image.styles.colormasks = _ModuleNamespace()
qrcode.image.styles.moduledrawers.pil = _ModuleNamespace()
qrcode.image.styledpil = _ModuleNamespace()
qrcode.image.styles.moduledrawers.svg = _ModuleNamespace()
qrcode.image.svg = _ModuleNamespace()
qrcode.release = _ModuleNamespace()

# Create short name aliases for common module references
image = qrcode.image
constants = qrcode.constants
exceptions = qrcode.exceptions
base = qrcode.base
LUT = qrcode.LUT
util = qrcode.util
main = qrcode.main
console_scripts = qrcode.console_scripts
compat = qrcode.compat
release = qrcode.release
svg_drawers = qrcode.image.styles.moduledrawers.svg

# ============================================================
# Module: qrcode.image
# Original: python-qrcode/qrcode/image/__init__.py
# ============================================================



# ============================================================
# Module: qrcode.constants
# Original: python-qrcode/qrcode/constants.py
# ============================================================

ERROR_CORRECT_L = 1
ERROR_CORRECT_M = 0
ERROR_CORRECT_Q = 3
ERROR_CORRECT_H = 2
PIL_AVAILABLE = find_spec('PIL') is not None

# Populate namespace for qrcode.constants
qrcode.constants.ERROR_CORRECT_L = ERROR_CORRECT_L
qrcode.constants.ERROR_CORRECT_M = ERROR_CORRECT_M
qrcode.constants.ERROR_CORRECT_Q = ERROR_CORRECT_Q
qrcode.constants.ERROR_CORRECT_H = ERROR_CORRECT_H
qrcode.constants.PIL_AVAILABLE = PIL_AVAILABLE

# ============================================================
# Module: qrcode.exceptions
# Original: python-qrcode/qrcode/exceptions.py
# ============================================================

class DataOverflowError(Exception):
    pass

# Populate namespace for qrcode.exceptions
qrcode.exceptions.DataOverflowError = DataOverflowError

# ============================================================
# Module: qrcode.image.styles.moduledrawers.base
# Original: python-qrcode/qrcode/image/styles/moduledrawers/base.py
# ============================================================

class QRModuleDrawer(abc.ABC):
    """
    QRModuleDrawer exists to draw the modules of the QR Code onto images.

    For this, technically all that is necessary is a ``drawrect(self, box,
    is_active)`` function which takes in the box in which it is to draw,
    whether or not the box is "active" (a module exists there). If
    ``needs_neighbors`` is set to True, then the method should also accept a
    ``neighbors`` kwarg (the neighboring pixels).

    It is frequently necessary to also implement an "initialize" function to
    set up values that only the containing Image class knows about.

    For examples of what these look like, see doc/module_drawers.png
    """
    needs_neighbors = False

    def __init__(self, **kwargs):
        pass

    def initialize(self, img: 'BaseImage') -> None:
        self.img = img

    @abc.abstractmethod
    def drawrect(self, box, is_active) -> None:
        ...

# Populate namespace for qrcode.image.styles.moduledrawers.base
qrcode.image.styles.moduledrawers.base.QRModuleDrawer = QRModuleDrawer

# ============================================================
# Module: qrcode.image.base
# Original: python-qrcode/qrcode/image/base.py
# ============================================================

DrawerAliases = dict[str, tuple[type[QRModuleDrawer], dict[str, Any]]]

class BaseImage(abc.ABC):
    """
    Base QRCode image output class.
    """
    kind: str | None = None
    allowed_kinds: tuple[str, ...] | None = None
    needs_context = False
    needs_processing = False
    needs_drawrect = True

    def __init__(self, border, width, box_size, *args, **kwargs):
        self.border = border
        self.width = width
        self.box_size = box_size
        self.pixel_size = (self.width + self.border * 2) * self.box_size
        self.modules = kwargs.pop('qrcode_modules')
        self._img = self.new_image(**kwargs)
        self.init_new_image()

    @abc.abstractmethod
    def drawrect(self, row, col):
        """
        Draw a single rectangle of the QR code.
        """

    def drawrect_context(self, row: int, col: int, qr: QRCode):
        """
        Draw a single rectangle of the QR code given the surrounding context
        """
        raise NotImplementedError('BaseImage.drawrect_context')

    def process(self):
        """
        Processes QR code after completion
        """
        raise NotImplementedError('BaseImage.drawimage')

    @abc.abstractmethod
    def save(self, stream, kind=None):
        """
        Save the image file.
        """

    def pixel_box(self, row, col):
        """
        A helper method for pixel-based image generators that specifies the
        four pixel coordinates for a single rect.
        """
        x = (col + self.border) * self.box_size
        y = (row + self.border) * self.box_size
        return ((x, y), (x + self.box_size - 1, y + self.box_size - 1))

    @abc.abstractmethod
    def new_image(self, **kwargs) -> Any:
        """
        Build the image class. Subclasses should return the class created.
        """

    def init_new_image(self):
        pass

    def get_image(self, **kwargs):
        """
        Return the image class for further processing.
        """
        return self._img

    def check_kind(self, kind, transform=None):
        """
        Get the image type.
        """
        if kind is None:
            kind = self.kind
        allowed = not self.allowed_kinds or kind in self.allowed_kinds
        if transform:
            kind = transform(kind)
            if not allowed:
                allowed = kind in self.allowed_kinds
        if not allowed:
            raise ValueError(f'Cannot set {type(self).__name__} type to {kind}')
        return kind

    def is_eye(self, row: int, col: int):
        """
        Find whether the referenced module is in an eye.
        """
        return row < 7 and col < 7 or (row < 7 and self.width - col < 8) or (self.width - row < 8 and col < 7)

class BaseImageWithDrawer(BaseImage):
    default_drawer_class: type[QRModuleDrawer]
    drawer_aliases: DrawerAliases = {}

    def get_default_module_drawer(self) -> QRModuleDrawer:
        return self.default_drawer_class()

    def get_default_eye_drawer(self) -> QRModuleDrawer:
        return self.default_drawer_class()
    needs_context = True
    module_drawer: QRModuleDrawer
    eye_drawer: QRModuleDrawer

    def __init__(self, *args, module_drawer: QRModuleDrawer | str | None=None, eye_drawer: QRModuleDrawer | str | None=None, **kwargs):
        self.module_drawer = self.get_drawer(module_drawer) or self.get_default_module_drawer()
        self.eye_drawer = self.get_drawer(eye_drawer) or self.get_default_eye_drawer()
        super().__init__(*args, **kwargs)

    def get_drawer(self, drawer: QRModuleDrawer | str | None) -> QRModuleDrawer | None:
        if not isinstance(drawer, str):
            return drawer
        drawer_cls, kwargs = self.drawer_aliases[drawer]
        return drawer_cls(**kwargs)

    def init_new_image(self):
        self.module_drawer.initialize(img=self)
        self.eye_drawer.initialize(img=self)
        return super().init_new_image()

    def drawrect_context(self, row: int, col: int, qr: QRCode):
        box = self.pixel_box(row, col)
        drawer = self.eye_drawer if self.is_eye(row, col) else self.module_drawer
        is_active: bool | ActiveWithNeighbors = qr.active_with_neighbors(row, col) if drawer.needs_neighbors else bool(qr.modules[row][col])
        drawer.drawrect(box, is_active)

# Populate namespace for qrcode.image.base
qrcode.image.base.DrawerAliases = DrawerAliases
qrcode.image.base.BaseImage = BaseImage
qrcode.image.base.BaseImageWithDrawer = BaseImageWithDrawer

# ============================================================
# Module: qrcode.image.pil
# Original: python-qrcode/qrcode/image/pil.py
# ============================================================

class PilImage(qrcode.image.base.BaseImage):
    """
    PIL image builder, default format is PNG.
    """
    kind = 'PNG'

    def new_image(self, **kwargs):
        if not Image:
            raise ImportError('PIL library not found.')
        back_color = kwargs.get('back_color', 'white')
        fill_color = kwargs.get('fill_color', 'black')
        try:
            fill_color = fill_color.lower()
            back_color = back_color.lower()
        except AttributeError:
            pass
        if fill_color == 'black' and back_color == 'white':
            mode = '1'
            fill_color = 0
            if back_color == 'white':
                back_color = 255
        elif back_color == 'transparent':
            mode = 'RGBA'
            back_color = None
        else:
            mode = 'RGB'
        img = Image.new(mode, (self.pixel_size, self.pixel_size), back_color)
        self.fill_color = fill_color
        self._idr = ImageDraw.Draw(img)
        return img

    def drawrect(self, row, col):
        box = self.pixel_box(row, col)
        self._idr.rectangle(box, fill=self.fill_color)

    def save(self, stream, format=None, **kwargs):
        kind = kwargs.pop('kind', self.kind)
        if format is None:
            format = kind
        self._img.save(stream, format=format, **kwargs)

    def __getattr__(self, name):
        return getattr(self._img, name)

# Populate namespace for qrcode.image.pil
qrcode.image.pil.PilImage = PilImage

# ============================================================
# Module: qrcode.base
# Original: python-qrcode/qrcode/base.py
# ============================================================

EXP_TABLE = list(range(256))
LOG_TABLE = list(range(256))
for i in range(8):
    EXP_TABLE[i] = 1 << i
for i in range(8, 256):
    EXP_TABLE[i] = EXP_TABLE[i - 4] ^ EXP_TABLE[i - 5] ^ EXP_TABLE[i - 6] ^ EXP_TABLE[i - 8]
for i in range(255):
    LOG_TABLE[EXP_TABLE[i]] = i
RS_BLOCK_OFFSET = {constants.ERROR_CORRECT_L: 0, constants.ERROR_CORRECT_M: 1, constants.ERROR_CORRECT_Q: 2, constants.ERROR_CORRECT_H: 3}
RS_BLOCK_TABLE = ((1, 26, 19), (1, 26, 16), (1, 26, 13), (1, 26, 9), (1, 44, 34), (1, 44, 28), (1, 44, 22), (1, 44, 16), (1, 70, 55), (1, 70, 44), (2, 35, 17), (2, 35, 13), (1, 100, 80), (2, 50, 32), (2, 50, 24), (4, 25, 9), (1, 134, 108), (2, 67, 43), (2, 33, 15, 2, 34, 16), (2, 33, 11, 2, 34, 12), (2, 86, 68), (4, 43, 27), (4, 43, 19), (4, 43, 15), (2, 98, 78), (4, 49, 31), (2, 32, 14, 4, 33, 15), (4, 39, 13, 1, 40, 14), (2, 121, 97), (2, 60, 38, 2, 61, 39), (4, 40, 18, 2, 41, 19), (4, 40, 14, 2, 41, 15), (2, 146, 116), (3, 58, 36, 2, 59, 37), (4, 36, 16, 4, 37, 17), (4, 36, 12, 4, 37, 13), (2, 86, 68, 2, 87, 69), (4, 69, 43, 1, 70, 44), (6, 43, 19, 2, 44, 20), (6, 43, 15, 2, 44, 16), (4, 101, 81), (1, 80, 50, 4, 81, 51), (4, 50, 22, 4, 51, 23), (3, 36, 12, 8, 37, 13), (2, 116, 92, 2, 117, 93), (6, 58, 36, 2, 59, 37), (4, 46, 20, 6, 47, 21), (7, 42, 14, 4, 43, 15), (4, 133, 107), (8, 59, 37, 1, 60, 38), (8, 44, 20, 4, 45, 21), (12, 33, 11, 4, 34, 12), (3, 145, 115, 1, 146, 116), (4, 64, 40, 5, 65, 41), (11, 36, 16, 5, 37, 17), (11, 36, 12, 5, 37, 13), (5, 109, 87, 1, 110, 88), (5, 65, 41, 5, 66, 42), (5, 54, 24, 7, 55, 25), (11, 36, 12, 7, 37, 13), (5, 122, 98, 1, 123, 99), (7, 73, 45, 3, 74, 46), (15, 43, 19, 2, 44, 20), (3, 45, 15, 13, 46, 16), (1, 135, 107, 5, 136, 108), (10, 74, 46, 1, 75, 47), (1, 50, 22, 15, 51, 23), (2, 42, 14, 17, 43, 15), (5, 150, 120, 1, 151, 121), (9, 69, 43, 4, 70, 44), (17, 50, 22, 1, 51, 23), (2, 42, 14, 19, 43, 15), (3, 141, 113, 4, 142, 114), (3, 70, 44, 11, 71, 45), (17, 47, 21, 4, 48, 22), (9, 39, 13, 16, 40, 14), (3, 135, 107, 5, 136, 108), (3, 67, 41, 13, 68, 42), (15, 54, 24, 5, 55, 25), (15, 43, 15, 10, 44, 16), (4, 144, 116, 4, 145, 117), (17, 68, 42), (17, 50, 22, 6, 51, 23), (19, 46, 16, 6, 47, 17), (2, 139, 111, 7, 140, 112), (17, 74, 46), (7, 54, 24, 16, 55, 25), (34, 37, 13), (4, 151, 121, 5, 152, 122), (4, 75, 47, 14, 76, 48), (11, 54, 24, 14, 55, 25), (16, 45, 15, 14, 46, 16), (6, 147, 117, 4, 148, 118), (6, 73, 45, 14, 74, 46), (11, 54, 24, 16, 55, 25), (30, 46, 16, 2, 47, 17), (8, 132, 106, 4, 133, 107), (8, 75, 47, 13, 76, 48), (7, 54, 24, 22, 55, 25), (22, 45, 15, 13, 46, 16), (10, 142, 114, 2, 143, 115), (19, 74, 46, 4, 75, 47), (28, 50, 22, 6, 51, 23), (33, 46, 16, 4, 47, 17), (8, 152, 122, 4, 153, 123), (22, 73, 45, 3, 74, 46), (8, 53, 23, 26, 54, 24), (12, 45, 15, 28, 46, 16), (3, 147, 117, 10, 148, 118), (3, 73, 45, 23, 74, 46), (4, 54, 24, 31, 55, 25), (11, 45, 15, 31, 46, 16), (7, 146, 116, 7, 147, 117), (21, 73, 45, 7, 74, 46), (1, 53, 23, 37, 54, 24), (19, 45, 15, 26, 46, 16), (5, 145, 115, 10, 146, 116), (19, 75, 47, 10, 76, 48), (15, 54, 24, 25, 55, 25), (23, 45, 15, 25, 46, 16), (13, 145, 115, 3, 146, 116), (2, 74, 46, 29, 75, 47), (42, 54, 24, 1, 55, 25), (23, 45, 15, 28, 46, 16), (17, 145, 115), (10, 74, 46, 23, 75, 47), (10, 54, 24, 35, 55, 25), (19, 45, 15, 35, 46, 16), (17, 145, 115, 1, 146, 116), (14, 74, 46, 21, 75, 47), (29, 54, 24, 19, 55, 25), (11, 45, 15, 46, 46, 16), (13, 145, 115, 6, 146, 116), (14, 74, 46, 23, 75, 47), (44, 54, 24, 7, 55, 25), (59, 46, 16, 1, 47, 17), (12, 151, 121, 7, 152, 122), (12, 75, 47, 26, 76, 48), (39, 54, 24, 14, 55, 25), (22, 45, 15, 41, 46, 16), (6, 151, 121, 14, 152, 122), (6, 75, 47, 34, 76, 48), (46, 54, 24, 10, 55, 25), (2, 45, 15, 64, 46, 16), (17, 152, 122, 4, 153, 123), (29, 74, 46, 14, 75, 47), (49, 54, 24, 10, 55, 25), (24, 45, 15, 46, 46, 16), (4, 152, 122, 18, 153, 123), (13, 74, 46, 32, 75, 47), (48, 54, 24, 14, 55, 25), (42, 45, 15, 32, 46, 16), (20, 147, 117, 4, 148, 118), (40, 75, 47, 7, 76, 48), (43, 54, 24, 22, 55, 25), (10, 45, 15, 67, 46, 16), (19, 148, 118, 6, 149, 119), (18, 75, 47, 31, 76, 48), (34, 54, 24, 34, 55, 25), (20, 45, 15, 61, 46, 16))

def glog(n):
    if n < 1:
        raise ValueError(f'glog({n})')
    return LOG_TABLE[n]

def gexp(n):
    return EXP_TABLE[n % 255]

class Polynomial:

    def __init__(self, num, shift):
        if not num:
            raise ValueError(f'{len(num)}/{shift}')
        offset = 0
        for offset in range(len(num)):
            if num[offset] != 0:
                break
        self.num = num[offset:] + [0] * shift

    def __getitem__(self, index):
        return self.num[index]

    def __iter__(self):
        return iter(self.num)

    def __len__(self):
        return len(self.num)

    def __mul__(self, other):
        num = [0] * (len(self) + len(other) - 1)
        for i, item in enumerate(self):
            for j, other_item in enumerate(other):
                num[i + j] ^= gexp(glog(item) + glog(other_item))
        return Polynomial(num, 0)

    def __mod__(self, other):
        difference = len(self) - len(other)
        if difference < 0:
            return self
        ratio = glog(self[0]) - glog(other[0])
        num = [item ^ gexp(glog(other_item) + ratio) for item, other_item in zip(self, other)]
        if difference:
            num.extend(self[-difference:])
        return Polynomial(num, 0) % other

class RSBlock(NamedTuple):
    total_count: int
    data_count: int

def rs_blocks(version, error_correction):
    if error_correction not in RS_BLOCK_OFFSET:
        raise ValueError(f'bad rs block @ version: {version} / error_correction: {error_correction}')
    offset = RS_BLOCK_OFFSET[error_correction]
    rs_block = RS_BLOCK_TABLE[(version - 1) * 4 + offset]
    blocks = []
    for i in range(0, len(rs_block), 3):
        count, total_count, data_count = rs_block[i:i + 3]
        for _ in range(count):
            blocks.append(RSBlock(total_count, data_count))
    return blocks

# Populate namespace for qrcode.base
qrcode.base.EXP_TABLE = EXP_TABLE
qrcode.base.LOG_TABLE = LOG_TABLE
qrcode.base.RS_BLOCK_OFFSET = RS_BLOCK_OFFSET
qrcode.base.RS_BLOCK_TABLE = RS_BLOCK_TABLE
qrcode.base.glog = glog
qrcode.base.gexp = gexp
qrcode.base.Polynomial = Polynomial
qrcode.base.RSBlock = RSBlock
qrcode.base.rs_blocks = rs_blocks

# ============================================================
# Module: qrcode.LUT
# Original: python-qrcode/qrcode/LUT.py
# ============================================================

rsPoly_LUT = {7: [1, 127, 122, 154, 164, 11, 68, 117], 10: [1, 216, 194, 159, 111, 199, 94, 95, 113, 157, 193], 13: [1, 137, 73, 227, 17, 177, 17, 52, 13, 46, 43, 83, 132, 120], 15: [1, 29, 196, 111, 163, 112, 74, 10, 105, 105, 139, 132, 151, 32, 134, 26], 16: [1, 59, 13, 104, 189, 68, 209, 30, 8, 163, 65, 41, 229, 98, 50, 36, 59], 17: [1, 119, 66, 83, 120, 119, 22, 197, 83, 249, 41, 143, 134, 85, 53, 125, 99, 79], 18: [1, 239, 251, 183, 113, 149, 175, 199, 215, 240, 220, 73, 82, 173, 75, 32, 67, 217, 146], 20: [1, 152, 185, 240, 5, 111, 99, 6, 220, 112, 150, 69, 36, 187, 22, 228, 198, 121, 121, 165, 174], 22: [1, 89, 179, 131, 176, 182, 244, 19, 189, 69, 40, 28, 137, 29, 123, 67, 253, 86, 218, 230, 26, 145, 245], 24: [1, 122, 118, 169, 70, 178, 237, 216, 102, 115, 150, 229, 73, 130, 72, 61, 43, 206, 1, 237, 247, 127, 217, 144, 117], 26: [1, 246, 51, 183, 4, 136, 98, 199, 152, 77, 56, 206, 24, 145, 40, 209, 117, 233, 42, 135, 68, 70, 144, 146, 77, 43, 94], 28: [1, 252, 9, 28, 13, 18, 251, 208, 150, 103, 174, 100, 41, 167, 12, 247, 56, 117, 119, 233, 127, 181, 100, 121, 147, 176, 74, 58, 197], 30: [1, 212, 246, 77, 73, 195, 192, 75, 98, 5, 70, 103, 177, 22, 217, 138, 51, 181, 246, 72, 25, 18, 46, 228, 74, 216, 195, 11, 106, 130, 150]}

# Populate namespace for qrcode.LUT
qrcode.LUT.rsPoly_LUT = rsPoly_LUT

# ============================================================
# Module: qrcode.util
# Original: python-qrcode/qrcode/util.py
# ============================================================

MODE_NUMBER = 1 << 0
MODE_ALPHA_NUM = 1 << 1
MODE_8BIT_BYTE = 1 << 2
MODE_KANJI = 1 << 3
MODE_SIZE_SMALL = {MODE_NUMBER: 10, MODE_ALPHA_NUM: 9, MODE_8BIT_BYTE: 8, MODE_KANJI: 8}
MODE_SIZE_MEDIUM = {MODE_NUMBER: 12, MODE_ALPHA_NUM: 11, MODE_8BIT_BYTE: 16, MODE_KANJI: 10}
MODE_SIZE_LARGE = {MODE_NUMBER: 14, MODE_ALPHA_NUM: 13, MODE_8BIT_BYTE: 16, MODE_KANJI: 12}
ALPHA_NUM = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:'
RE_ALPHA_NUM = re.compile(b'^[' + re.escape(ALPHA_NUM) + b']*\\Z')
NUMBER_LENGTH = {3: 10, 2: 7, 1: 4}
PATTERN_POSITION_TABLE = [[], [6, 18], [6, 22], [6, 26], [6, 30], [6, 34], [6, 22, 38], [6, 24, 42], [6, 26, 46], [6, 28, 50], [6, 30, 54], [6, 32, 58], [6, 34, 62], [6, 26, 46, 66], [6, 26, 48, 70], [6, 26, 50, 74], [6, 30, 54, 78], [6, 30, 56, 82], [6, 30, 58, 86], [6, 34, 62, 90], [6, 28, 50, 72, 94], [6, 26, 50, 74, 98], [6, 30, 54, 78, 102], [6, 28, 54, 80, 106], [6, 32, 58, 84, 110], [6, 30, 58, 86, 114], [6, 34, 62, 90, 118], [6, 26, 50, 74, 98, 122], [6, 30, 54, 78, 102, 126], [6, 26, 52, 78, 104, 130], [6, 30, 56, 82, 108, 134], [6, 34, 60, 86, 112, 138], [6, 30, 58, 86, 114, 142], [6, 34, 62, 90, 118, 146], [6, 30, 54, 78, 102, 126, 150], [6, 24, 50, 76, 102, 128, 154], [6, 28, 54, 80, 106, 132, 158], [6, 32, 58, 84, 110, 136, 162], [6, 26, 54, 82, 110, 138, 166], [6, 30, 58, 86, 114, 142, 170]]
G15 = 1 << 10 | 1 << 8 | 1 << 5 | 1 << 4 | 1 << 2 | 1 << 1 | 1 << 0
G18 = 1 << 12 | 1 << 11 | 1 << 10 | 1 << 9 | 1 << 8 | 1 << 5 | 1 << 2 | 1 << 0
G15_MASK = 1 << 14 | 1 << 12 | 1 << 10 | 1 << 4 | 1 << 1
PAD0 = 236
PAD1 = 17

def _data_count(block):
    return block.data_count
BIT_LIMIT_TABLE = [[0] + [8 * sum(map(_data_count, base.rs_blocks(version, error_correction))) for version in range(1, 41)] for error_correction in range(4)]

def BCH_type_info(data):
    d = data << 10
    while BCH_digit(d) - BCH_digit(G15) >= 0:
        d ^= G15 << BCH_digit(d) - BCH_digit(G15)
    return (data << 10 | d) ^ G15_MASK

def BCH_type_number(data):
    d = data << 12
    while BCH_digit(d) - BCH_digit(G18) >= 0:
        d ^= G18 << BCH_digit(d) - BCH_digit(G18)
    return data << 12 | d

def BCH_digit(data):
    digit = 0
    while data != 0:
        digit += 1
        data >>= 1
    return digit

def pattern_position(version):
    return PATTERN_POSITION_TABLE[version - 1]

def mask_func(pattern):
    """
    Return the mask function for the given mask pattern.
    """
    if pattern == 0:
        return lambda i, j: (i + j) % 2 == 0
    if pattern == 1:
        return lambda i, j: i % 2 == 0
    if pattern == 2:
        return lambda i, j: j % 3 == 0
    if pattern == 3:
        return lambda i, j: (i + j) % 3 == 0
    if pattern == 4:
        return lambda i, j: (math.floor(i / 2) + math.floor(j / 3)) % 2 == 0
    if pattern == 5:
        return lambda i, j: i * j % 2 + i * j % 3 == 0
    if pattern == 6:
        return lambda i, j: (i * j % 2 + i * j % 3) % 2 == 0
    if pattern == 7:
        return lambda i, j: (i * j % 3 + (i + j) % 2) % 2 == 0
    raise TypeError('Bad mask pattern: ' + pattern)

def mode_sizes_for_version(version):
    if version < 10:
        return MODE_SIZE_SMALL
    if version < 27:
        return MODE_SIZE_MEDIUM
    return MODE_SIZE_LARGE

def length_in_bits(mode, version):
    if mode not in (MODE_NUMBER, MODE_ALPHA_NUM, MODE_8BIT_BYTE, MODE_KANJI):
        raise TypeError(f'Invalid mode ({mode})')
    check_version(version)
    return mode_sizes_for_version(version)[mode]

def check_version(version):
    if version < 1 or version > 40:
        raise ValueError(f'Invalid version (was {version}, expected 1 to 40)')

def lost_point(modules):
    modules_count = len(modules)
    lost_point = 0
    lost_point = _lost_point_level1(modules, modules_count)
    lost_point += _lost_point_level2(modules, modules_count)
    lost_point += _lost_point_level3(modules, modules_count)
    lost_point += _lost_point_level4(modules, modules_count)
    return lost_point

def _lost_point_level1(modules, modules_count):
    lost_point = 0
    modules_range = range(modules_count)
    container = [0] * (modules_count + 1)
    for row in modules_range:
        this_row = modules[row]
        previous_color = this_row[0]
        length = 0
        for col in modules_range:
            if this_row[col] == previous_color:
                length += 1
            else:
                if length >= 5:
                    container[length] += 1
                length = 1
                previous_color = this_row[col]
        if length >= 5:
            container[length] += 1
    for col in modules_range:
        previous_color = modules[0][col]
        length = 0
        for row in modules_range:
            if modules[row][col] == previous_color:
                length += 1
            else:
                if length >= 5:
                    container[length] += 1
                length = 1
                previous_color = modules[row][col]
        if length >= 5:
            container[length] += 1
    lost_point += sum((container[each_length] * (each_length - 2) for each_length in range(5, modules_count + 1)))
    return lost_point

def _lost_point_level2(modules, modules_count):
    lost_point = 0
    modules_range = range(modules_count - 1)
    for row in modules_range:
        this_row = modules[row]
        next_row = modules[row + 1]
        modules_range_iter = iter(modules_range)
        for col in modules_range_iter:
            top_right = this_row[col + 1]
            if top_right != next_row[col + 1]:
                next(modules_range_iter, None)
            elif top_right != this_row[col] or top_right != next_row[col]:
                continue
            else:
                lost_point += 3
    return lost_point

def _lost_point_level3(modules, modules_count):
    modules_range = range(modules_count)
    modules_range_short = range(modules_count - 10)
    lost_point = 0
    for row in modules_range:
        this_row = modules[row]
        modules_range_short_iter = iter(modules_range_short)
        col = 0
        for col in modules_range_short_iter:
            if not this_row[col + 1] and this_row[col + 4] and (not this_row[col + 5]) and this_row[col + 6] and (not this_row[col + 9]) and (this_row[col + 0] and this_row[col + 2] and this_row[col + 3] and (not this_row[col + 7]) and (not this_row[col + 8]) and (not this_row[col + 10]) or (not this_row[col + 0] and (not this_row[col + 2]) and (not this_row[col + 3]) and this_row[col + 7] and this_row[col + 8] and this_row[col + 10])):
                lost_point += 40
            if this_row[col + 10]:
                next(modules_range_short_iter, None)
    for col in modules_range:
        modules_range_short_iter = iter(modules_range_short)
        row = 0
        for row in modules_range_short_iter:
            if not modules[row + 1][col] and modules[row + 4][col] and (not modules[row + 5][col]) and modules[row + 6][col] and (not modules[row + 9][col]) and (modules[row + 0][col] and modules[row + 2][col] and modules[row + 3][col] and (not modules[row + 7][col]) and (not modules[row + 8][col]) and (not modules[row + 10][col]) or (not modules[row + 0][col] and (not modules[row + 2][col]) and (not modules[row + 3][col]) and modules[row + 7][col] and modules[row + 8][col] and modules[row + 10][col])):
                lost_point += 40
            if modules[row + 10][col]:
                next(modules_range_short_iter, None)
    return lost_point

def _lost_point_level4(modules, modules_count):
    dark_count = sum(map(sum, modules))
    percent = float(dark_count) / modules_count ** 2
    rating = int(abs(percent * 100 - 50) / 5)
    return rating * 10

def optimal_data_chunks(data, minimum=4):
    """
    An iterator returning QRData chunks optimized to the data content.

    :param minimum: The minimum number of bytes in a row to split as a chunk.
    """
    data = to_bytestring(data)
    num_pattern = b'\\d'
    alpha_pattern = b'[' + re.escape(ALPHA_NUM) + b']'
    if len(data) <= minimum:
        num_pattern = re.compile(b'^' + num_pattern + b'+$')
        alpha_pattern = re.compile(b'^' + alpha_pattern + b'+$')
    else:
        re_repeat = b'{' + str(minimum).encode('ascii') + b',}'
        num_pattern = re.compile(num_pattern + re_repeat)
        alpha_pattern = re.compile(alpha_pattern + re_repeat)
    num_bits = _optimal_split(data, num_pattern)
    for is_num, chunk in num_bits:
        if is_num:
            yield QRData(chunk, mode=MODE_NUMBER, check_data=False)
        else:
            for is_alpha, sub_chunk in _optimal_split(chunk, alpha_pattern):
                mode = MODE_ALPHA_NUM if is_alpha else MODE_8BIT_BYTE
                yield QRData(sub_chunk, mode=mode, check_data=False)

def _optimal_split(data, pattern):
    while data:
        match = re.search(pattern, data)
        if not match:
            break
        start, end = (match.start(), match.end())
        if start:
            yield (False, data[:start])
        yield (True, data[start:end])
        data = data[end:]
    if data:
        yield (False, data)

def to_bytestring(data):
    """
    Convert data to a (utf-8 encoded) byte-string if it isn't a byte-string
    already.
    """
    if not isinstance(data, bytes):
        data = str(data).encode('utf-8')
    return data

def optimal_mode(data):
    """
    Calculate the optimal mode for this chunk of data.
    """
    if data.isdigit():
        return MODE_NUMBER
    if RE_ALPHA_NUM.match(data):
        return MODE_ALPHA_NUM
    return MODE_8BIT_BYTE

class QRData:
    """
    Data held in a QR compatible format.

    Doesn't currently handle KANJI.
    """

    def __init__(self, data, mode=None, check_data=True):
        """
        If ``mode`` isn't provided, the most compact QR data type possible is
        chosen.
        """
        if check_data:
            data = to_bytestring(data)
        if mode is None:
            self.mode = optimal_mode(data)
        else:
            self.mode = mode
            if mode not in (MODE_NUMBER, MODE_ALPHA_NUM, MODE_8BIT_BYTE):
                raise TypeError(f'Invalid mode ({mode})')
            if check_data and mode < optimal_mode(data):
                raise ValueError(f'Provided data can not be represented in mode {mode}')
        self.data = data

    def __len__(self):
        return len(self.data)

    def write(self, buffer):
        if self.mode == MODE_NUMBER:
            for i in range(0, len(self.data), 3):
                chars = self.data[i:i + 3]
                bit_length = NUMBER_LENGTH[len(chars)]
                buffer.put(int(chars), bit_length)
        elif self.mode == MODE_ALPHA_NUM:
            for i in range(0, len(self.data), 2):
                chars = self.data[i:i + 2]
                if len(chars) > 1:
                    buffer.put(ALPHA_NUM.find(chars[0]) * 45 + ALPHA_NUM.find(chars[1]), 11)
                else:
                    buffer.put(ALPHA_NUM.find(chars), 6)
        else:
            data = self.data
            for c in data:
                buffer.put(c, 8)

    def __repr__(self):
        return repr(self.data)

class BitBuffer:

    def __init__(self):
        self.buffer: list[int] = []
        self.length = 0

    def __repr__(self):
        return '.'.join([str(n) for n in self.buffer])

    def get(self, index):
        buf_index = math.floor(index / 8)
        return self.buffer[buf_index] >> 7 - index % 8 & 1 == 1

    def put(self, num, length):
        for i in range(length):
            self.put_bit(num >> length - i - 1 & 1 == 1)

    def __len__(self):
        return self.length

    def put_bit(self, bit):
        buf_index = self.length // 8
        if len(self.buffer) <= buf_index:
            self.buffer.append(0)
        if bit:
            self.buffer[buf_index] |= 128 >> self.length % 8
        self.length += 1

def create_bytes(buffer: BitBuffer, rs_blocks: list[RSBlock]):
    offset = 0
    maxDcCount = 0
    maxEcCount = 0
    dcdata: list[list[int]] = []
    ecdata: list[list[int]] = []
    for rs_block in rs_blocks:
        dcCount = rs_block.data_count
        ecCount = rs_block.total_count - dcCount
        maxDcCount = max(maxDcCount, dcCount)
        maxEcCount = max(maxEcCount, ecCount)
        current_dc = [255 & buffer.buffer[i + offset] for i in range(dcCount)]
        offset += dcCount
        if ecCount in LUT.rsPoly_LUT:
            rsPoly = base.Polynomial(LUT.rsPoly_LUT[ecCount], 0)
        else:
            rsPoly = base.Polynomial([1], 0)
            for i in range(ecCount):
                rsPoly = rsPoly * base.Polynomial([1, base.gexp(i)], 0)
        rawPoly = base.Polynomial(current_dc, len(rsPoly) - 1)
        modPoly = rawPoly % rsPoly
        current_ec = []
        mod_offset = len(modPoly) - ecCount
        for i in range(ecCount):
            modIndex = i + mod_offset
            current_ec.append(modPoly[modIndex] if modIndex >= 0 else 0)
        dcdata.append(current_dc)
        ecdata.append(current_ec)
    data = []
    for i in range(maxDcCount):
        for dc in dcdata:
            if i < len(dc):
                data.append(dc[i])
    for i in range(maxEcCount):
        for ec in ecdata:
            if i < len(ec):
                data.append(ec[i])
    return data

def create_data(version, error_correction, data_list):
    buffer = BitBuffer()
    for data in data_list:
        buffer.put(data.mode, 4)
        buffer.put(len(data), length_in_bits(data.mode, version))
        data.write(buffer)
    rs_blocks = base.rs_blocks(version, error_correction)
    bit_limit = sum((block.data_count * 8 for block in rs_blocks))
    if len(buffer) > bit_limit:
        raise exceptions.DataOverflowError(f'Code length overflow. Data size ({len(buffer)}) > size available ({bit_limit})')
    for _ in range(min(bit_limit - len(buffer), 4)):
        buffer.put_bit(False)
    delimit = len(buffer) % 8
    if delimit:
        for _ in range(8 - delimit):
            buffer.put_bit(False)
    bytes_to_fill = (bit_limit - len(buffer)) // 8
    for i in range(bytes_to_fill):
        if i % 2 == 0:
            buffer.put(PAD0, 8)
        else:
            buffer.put(PAD1, 8)
    return create_bytes(buffer, rs_blocks)

# Populate namespace for qrcode.util
qrcode.util.MODE_NUMBER = MODE_NUMBER
qrcode.util.MODE_ALPHA_NUM = MODE_ALPHA_NUM
qrcode.util.MODE_8BIT_BYTE = MODE_8BIT_BYTE
qrcode.util.MODE_KANJI = MODE_KANJI
qrcode.util.MODE_SIZE_SMALL = MODE_SIZE_SMALL
qrcode.util.MODE_SIZE_MEDIUM = MODE_SIZE_MEDIUM
qrcode.util.MODE_SIZE_LARGE = MODE_SIZE_LARGE
qrcode.util.ALPHA_NUM = ALPHA_NUM
qrcode.util.RE_ALPHA_NUM = RE_ALPHA_NUM
qrcode.util.NUMBER_LENGTH = NUMBER_LENGTH
qrcode.util.PATTERN_POSITION_TABLE = PATTERN_POSITION_TABLE
qrcode.util.G15 = G15
qrcode.util.G18 = G18
qrcode.util.G15_MASK = G15_MASK
qrcode.util.PAD0 = PAD0
qrcode.util.PAD1 = PAD1
qrcode.util._data_count = _data_count
qrcode.util.BIT_LIMIT_TABLE = BIT_LIMIT_TABLE
qrcode.util.BCH_type_info = BCH_type_info
qrcode.util.BCH_type_number = BCH_type_number
qrcode.util.BCH_digit = BCH_digit
qrcode.util.pattern_position = pattern_position
qrcode.util.mask_func = mask_func
qrcode.util.mode_sizes_for_version = mode_sizes_for_version
qrcode.util.length_in_bits = length_in_bits
qrcode.util.check_version = check_version
qrcode.util.lost_point = lost_point
qrcode.util._lost_point_level1 = _lost_point_level1
qrcode.util._lost_point_level2 = _lost_point_level2
qrcode.util._lost_point_level3 = _lost_point_level3
qrcode.util._lost_point_level4 = _lost_point_level4
qrcode.util.optimal_data_chunks = optimal_data_chunks
qrcode.util._optimal_split = _optimal_split
qrcode.util.to_bytestring = to_bytestring
qrcode.util.optimal_mode = optimal_mode
qrcode.util.QRData = QRData
qrcode.util.BitBuffer = BitBuffer
qrcode.util.create_bytes = create_bytes
qrcode.util.create_data = create_data

# ============================================================
# Module: qrcode.compat.png
# Original: python-qrcode/qrcode/compat/png.py
# ============================================================

PngWriter = None
try:
    from png import Writer as PngWriter
except ImportError:
    pass

# Populate namespace for qrcode.compat.png
qrcode.compat.png.PngWriter = PngWriter

# ============================================================
# Module: qrcode.image.pure
# Original: python-qrcode/qrcode/image/pure.py
# ============================================================

class PyPNGImage(BaseImage):
    """
    pyPNG image builder.
    """
    kind = 'PNG'
    allowed_kinds = ('PNG',)
    needs_drawrect = False

    def new_image(self, **kwargs):
        if not PngWriter:
            raise ImportError('PyPNG library not installed.')
        return PngWriter(self.pixel_size, self.pixel_size, greyscale=True, bitdepth=1)

    def drawrect(self, row, col):
        """
        Not used.
        """

    def save(self, stream, kind=None):
        if isinstance(stream, str):
            stream = Path(stream).open('wb')
        self._img.write(stream, self.rows_iter())

    def rows_iter(self):
        yield from self.border_rows_iter()
        border_col = [1] * (self.box_size * self.border)
        for module_row in self.modules:
            row = border_col + list(chain.from_iterable(([not point] * self.box_size for point in module_row))) + border_col
            for _ in range(self.box_size):
                yield row
        yield from self.border_rows_iter()

    def border_rows_iter(self):
        border_row = [1] * (self.box_size * (self.width + self.border * 2))
        for _ in range(self.border * self.box_size):
            yield border_row
PymagingImage = PyPNGImage

# Populate namespace for qrcode.image.pure
qrcode.image.pure.PyPNGImage = PyPNGImage
qrcode.image.pure.PymagingImage = PymagingImage

# ============================================================
# Module: qrcode.main
# Original: python-qrcode/qrcode/main.py
# ============================================================

ModulesType = list[list[Optional[bool]]]
precomputed_qr_blanks: dict[int, ModulesType] = {}

def make(data=None, **kwargs):
    qr = QRCode(**kwargs)
    qr.add_data(data)
    return qr.make_image()

def _check_box_size(size):
    if int(size) <= 0:
        raise ValueError(f'Invalid box size (was {size}, expected larger than 0)')

def _check_border(size):
    if int(size) < 0:
        raise ValueError(f'Invalid border value (was {size}, expected 0 or larger than that)')

def _check_mask_pattern(mask_pattern):
    if mask_pattern is None:
        return
    if not isinstance(mask_pattern, int):
        raise TypeError(f'Invalid mask pattern (was {type(mask_pattern)}, expected int)')
    if mask_pattern < 0 or mask_pattern > 7:
        raise ValueError(f'Mask pattern should be in range(8) (got {mask_pattern})')

def copy_2d_array(x):
    return [row[:] for row in x]

class ActiveWithNeighbors(NamedTuple):
    NW: bool
    N: bool
    NE: bool
    W: bool
    me: bool
    E: bool
    SW: bool
    S: bool
    SE: bool

    def __bool__(self) -> bool:
        return self.me
GenericImage = TypeVar('GenericImage', bound=BaseImage)
GenericImageLocal = TypeVar('GenericImageLocal', bound=BaseImage)

class QRCode(Generic[GenericImage]):
    modules: ModulesType
    _version: int | None = None

    def __init__(self, version=None, error_correction=constants.ERROR_CORRECT_M, box_size=10, border=4, image_factory: type[GenericImage] | None=None, mask_pattern=None):
        _check_box_size(box_size)
        _check_border(border)
        self.version = version
        self.error_correction = int(error_correction)
        self.box_size = int(box_size)
        self.border = int(border)
        self.mask_pattern = mask_pattern
        self.image_factory = image_factory
        if image_factory is not None:
            assert issubclass(image_factory, BaseImage)
        self.clear()

    @property
    def version(self) -> int:
        if self._version is None:
            self.best_fit()
        return cast('int', self._version)

    @version.setter
    def version(self, value) -> None:
        if value is not None:
            value = int(value)
            util.check_version(value)
        self._version = value

    @property
    def mask_pattern(self):
        return self._mask_pattern

    @mask_pattern.setter
    def mask_pattern(self, pattern):
        _check_mask_pattern(pattern)
        self._mask_pattern = pattern

    def clear(self):
        """
        Reset the internal data.
        """
        self.modules = [[]]
        self.modules_count = 0
        self.data_cache = None
        self.data_list = []

    def add_data(self, data, optimize=20):
        """
        Add data to this QR Code.

        :param optimize: Data will be split into multiple chunks to optimize
            the QR size by finding to more compressed modes of at least this
            length. Set to ``0`` to avoid optimizing at all.
        """
        if isinstance(data, util.QRData):
            self.data_list.append(data)
        elif optimize:
            self.data_list.extend(util.optimal_data_chunks(data, minimum=optimize))
        else:
            self.data_list.append(util.QRData(data))
        self.data_cache = None

    def make(self, fit=True):
        """
        Compile the data into a QR Code array.

        :param fit: If ``True`` (or if a size has not been provided), find the
            best fit for the data to avoid data overflow errors.
        """
        if fit or self.version is None:
            self.best_fit(start=self.version)
        if self.mask_pattern is None:
            self.makeImpl(False, self.best_mask_pattern())
        else:
            self.makeImpl(False, self.mask_pattern)

    def makeImpl(self, test, mask_pattern):
        self.modules_count = self.version * 4 + 17
        if self.version in precomputed_qr_blanks:
            self.modules = copy_2d_array(precomputed_qr_blanks[self.version])
        else:
            self.modules = [[None] * self.modules_count for i in range(self.modules_count)]
            self.setup_position_probe_pattern(0, 0)
            self.setup_position_probe_pattern(self.modules_count - 7, 0)
            self.setup_position_probe_pattern(0, self.modules_count - 7)
            self.setup_position_adjust_pattern()
            self.setup_timing_pattern()
            precomputed_qr_blanks[self.version] = copy_2d_array(self.modules)
        self.setup_type_info(test, mask_pattern)
        if self.version >= 7:
            self.setup_type_number(test)
        if self.data_cache is None:
            self.data_cache = util.create_data(self.version, self.error_correction, self.data_list)
        self.map_data(self.data_cache, mask_pattern)

    def setup_position_probe_pattern(self, row, col):
        for r in range(-1, 8):
            if row + r <= -1 or self.modules_count <= row + r:
                continue
            for c in range(-1, 8):
                if col + c <= -1 or self.modules_count <= col + c:
                    continue
                if 0 <= r <= 6 and c in {0, 6} or (0 <= c <= 6 and r in {0, 6}) or (2 <= r <= 4 and 2 <= c <= 4):
                    self.modules[row + r][col + c] = True
                else:
                    self.modules[row + r][col + c] = False

    def best_fit(self, start=None):
        """
        Find the minimum size required to fit in the data.
        """
        if start is None:
            start = 1
        util.check_version(start)
        mode_sizes = util.mode_sizes_for_version(start)
        buffer = util.BitBuffer()
        for data in self.data_list:
            buffer.put(data.mode, 4)
            buffer.put(len(data), mode_sizes[data.mode])
            data.write(buffer)
        needed_bits = len(buffer)
        self.version = bisect_left(util.BIT_LIMIT_TABLE[self.error_correction], needed_bits, start)
        if self.version == 41:
            raise exceptions.DataOverflowError
        if mode_sizes is not util.mode_sizes_for_version(self.version):
            self.best_fit(start=self.version)
        return self.version

    def best_mask_pattern(self):
        """
        Find the most efficient mask pattern.
        """
        min_lost_point = 0
        pattern = 0
        for i in range(8):
            self.makeImpl(True, i)
            lost_point = util.lost_point(self.modules)
            if i == 0 or min_lost_point > lost_point:
                min_lost_point = lost_point
                pattern = i
        return pattern

    def print_tty(self, out=None):
        """
        Output the QR Code only using TTY colors.

        If the data has not been compiled yet, make it first.
        """
        if out is None:
            out = sys.stdout
        if not out.isatty():
            raise OSError('Not a tty')
        if self.data_cache is None:
            self.make()
        modcount = self.modules_count
        out.write('\x1b[1;47m' + ' ' * (modcount * 2 + 4) + '\x1b[0m\n')
        for r in range(modcount):
            out.write('\x1b[1;47m  \x1b[40m')
            for c in range(modcount):
                if self.modules[r][c]:
                    out.write('  ')
                else:
                    out.write('\x1b[1;47m  \x1b[40m')
            out.write('\x1b[1;47m  \x1b[0m\n')
        out.write('\x1b[1;47m' + ' ' * (modcount * 2 + 4) + '\x1b[0m\n')
        out.flush()

    def print_ascii(self, out=None, tty=False, invert=False):
        """
        Output the QR Code using ASCII characters.

        :param tty: use fixed TTY color codes (forces invert=True)
        :param invert: invert the ASCII characters (solid <-> transparent)
        """
        if out is None:
            out = sys.stdout
        if tty and (not out.isatty()):
            raise OSError('Not a tty')
        if self.data_cache is None:
            self.make()
        modcount = self.modules_count
        codes = [bytes((code,)).decode('cp437') for code in (255, 223, 220, 219)]
        if tty:
            invert = True
        if invert:
            codes.reverse()

        def get_module(x, y) -> int:
            if invert and self.border and (max(x, y) >= modcount + self.border):
                return 1
            if min(x, y) < 0 or max(x, y) >= modcount:
                return 0
            return cast('int', self.modules[x][y])
        for r in range(-self.border, modcount + self.border, 2):
            if tty:
                if not invert or r < modcount + self.border - 1:
                    out.write('\x1b[48;5;232m')
                out.write('\x1b[38;5;255m')
            for c in range(-self.border, modcount + self.border):
                pos = get_module(r, c) + (get_module(r + 1, c) << 1)
                out.write(codes[pos])
            if tty:
                out.write('\x1b[0m')
            out.write('\n')
        out.flush()

    @overload
    def make_image(self, image_factory: Literal[None]=None, **kwargs) -> GenericImage:
        ...

    @overload
    def make_image(self, image_factory: type[GenericImageLocal] | None=None, **kwargs) -> GenericImageLocal:
        ...

    def make_image(self, image_factory=None, **kwargs):
        """
        Make an image from the QR Code data.

        If the data has not been compiled yet, make it first.
        """
        if kwargs.get('embeded_image_path') or kwargs.get('embeded_image'):
            warnings.warn("The 'embeded_*' parameters are deprecated. Use 'embedded_image_path' or 'embedded_image' instead. The 'embeded_*' parameters will be removed in v9.0.", category=DeprecationWarning, stacklevel=2)
        if (kwargs.get('embedded_image_path') or kwargs.get('embedded_image') or kwargs.get('embeded_image_path') or kwargs.get('embeded_image')) and self.error_correction != constants.ERROR_CORRECT_H:
            raise ValueError('Error correction level must be ERROR_CORRECT_H if an embedded image is provided')
        _check_box_size(self.box_size)
        if self.data_cache is None:
            self.make()
        if image_factory is not None:
            assert issubclass(image_factory, BaseImage)
        else:
            image_factory = self.image_factory
            if image_factory is None:
                image_factory = PilImage if Image else PyPNGImage
        im = image_factory(self.border, self.modules_count, self.box_size, qrcode_modules=self.modules, **kwargs)
        if im.needs_drawrect:
            for r in range(self.modules_count):
                for c in range(self.modules_count):
                    if im.needs_context:
                        im.drawrect_context(r, c, qr=self)
                    elif self.modules[r][c]:
                        im.drawrect(r, c)
        if im.needs_processing:
            im.process()
        return im

    def is_constrained(self, row: int, col: int) -> bool:
        return row >= 0 and row < len(self.modules) and (col >= 0) and (col < len(self.modules[row]))

    def setup_timing_pattern(self):
        for r in range(8, self.modules_count - 8):
            if self.modules[r][6] is not None:
                continue
            self.modules[r][6] = r % 2 == 0
        for c in range(8, self.modules_count - 8):
            if self.modules[6][c] is not None:
                continue
            self.modules[6][c] = c % 2 == 0

    def setup_position_adjust_pattern(self):
        pos = util.pattern_position(self.version)
        for i in range(len(pos)):
            row = pos[i]
            for j in range(len(pos)):
                col = pos[j]
                if self.modules[row][col] is not None:
                    continue
                for r in range(-2, 3):
                    for c in range(-2, 3):
                        if r in (-2, 2) or c in (-2, 2) or (r == 0 and c == 0):
                            self.modules[row + r][col + c] = True
                        else:
                            self.modules[row + r][col + c] = False

    def setup_type_number(self, test):
        bits = util.BCH_type_number(self.version)
        for i in range(18):
            mod = not test and bits >> i & 1 == 1
            self.modules[i // 3][i % 3 + self.modules_count - 8 - 3] = mod
        for i in range(18):
            mod = not test and bits >> i & 1 == 1
            self.modules[i % 3 + self.modules_count - 8 - 3][i // 3] = mod

    def setup_type_info(self, test, mask_pattern):
        data = self.error_correction << 3 | mask_pattern
        bits = util.BCH_type_info(data)
        for i in range(15):
            mod = not test and bits >> i & 1 == 1
            if i < 6:
                self.modules[i][8] = mod
            elif i < 8:
                self.modules[i + 1][8] = mod
            else:
                self.modules[self.modules_count - 15 + i][8] = mod
        for i in range(15):
            mod = not test and bits >> i & 1 == 1
            if i < 8:
                self.modules[8][self.modules_count - i - 1] = mod
            elif i < 9:
                self.modules[8][15 - i - 1 + 1] = mod
            else:
                self.modules[8][15 - i - 1] = mod
        self.modules[self.modules_count - 8][8] = not test

    def map_data(self, data, mask_pattern):
        inc = -1
        row = self.modules_count - 1
        bitIndex = 7
        byteIndex = 0
        mask_func = util.mask_func(mask_pattern)
        data_len = len(data)
        for col in range(self.modules_count - 1, 0, -2):
            if col <= 6:
                col -= 1
            col_range = (col, col - 1)
            while True:
                for c in col_range:
                    if self.modules[row][c] is None:
                        dark = False
                        if byteIndex < data_len:
                            dark = data[byteIndex] >> bitIndex & 1 == 1
                        if mask_func(row, c):
                            dark = not dark
                        self.modules[row][c] = dark
                        bitIndex -= 1
                        if bitIndex == -1:
                            byteIndex += 1
                            bitIndex = 7
                row += inc
                if row < 0 or self.modules_count <= row:
                    row -= inc
                    inc = -inc
                    break

    def get_matrix(self):
        """
        Return the QR Code as a multidimensional array, including the border.

        To return the array without a border, set ``self.border`` to 0 first.
        """
        if self.data_cache is None:
            self.make()
        if not self.border:
            return self.modules
        width = len(self.modules) + self.border * 2
        code = [[False] * width] * self.border
        x_border = [False] * self.border
        for module in self.modules:
            code.append(x_border + cast('list[bool]', module) + x_border)
        code += [[False] * width] * self.border
        return code

    def active_with_neighbors(self, row: int, col: int) -> ActiveWithNeighbors:
        context: list[bool] = []
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                context.append(self.is_constrained(r, c) and bool(self.modules[r][c]))
        return ActiveWithNeighbors(*context)

# Populate namespace for qrcode.main
qrcode.main.ModulesType = ModulesType
qrcode.main.make = make
qrcode.main._check_box_size = _check_box_size
qrcode.main._check_border = _check_border
qrcode.main._check_mask_pattern = _check_mask_pattern
qrcode.main.copy_2d_array = copy_2d_array
qrcode.main.ActiveWithNeighbors = ActiveWithNeighbors
qrcode.main.GenericImage = GenericImage
qrcode.main.GenericImageLocal = GenericImageLocal
qrcode.main.QRCode = QRCode

# ============================================================
# Module: qrcode
# Original: python-qrcode/qrcode/__init__.py
# ============================================================

__all__ = ['ERROR_CORRECT_H', 'ERROR_CORRECT_L', 'ERROR_CORRECT_M', 'ERROR_CORRECT_Q', 'QRCode', 'image', 'make', 'run_example']

def run_example(data='http://www.lincolnloop.com', *args, **kwargs):
    """
    Build an example QR Code and display it.

    There's an even easier way than the code here though: just use the ``make``
    shortcut.
    """
    qr = QRCode(*args, **kwargs)
    qr.add_data(data)
    im = qr.make_image()
    im.show()

# Populate namespace for qrcode
qrcode.__all__ = __all__
qrcode.run_example = run_example

# Add convenience aliases for top-level qrcode module (from __all__)
qrcode.ERROR_CORRECT_H = ERROR_CORRECT_H
qrcode.ERROR_CORRECT_L = ERROR_CORRECT_L
qrcode.ERROR_CORRECT_M = ERROR_CORRECT_M
qrcode.ERROR_CORRECT_Q = ERROR_CORRECT_Q
qrcode.QRCode = QRCode
qrcode.make = make
qrcode.run_example = run_example

# ============================================================
# Module: qrcode.console_scripts
# Original: python-qrcode/qrcode/console_scripts.py
# ============================================================

"""
qr - Convert stdin (or the first argument) to a QR Code.

When stdout is a tty the QR Code is printed to the terminal and when stdout is
a pipe to a file an image is written. The default image format is PNG.
"""
if sys.platform.startswith(('win', 'cygwin')):
    import colorama
    colorama.init()
default_factories = {'pil': 'qrcode.image.pil.PilImage', 'png': 'qrcode.image.pure.PyPNGImage', 'svg': 'qrcode.image.svg.SvgImage', 'svg-fragment': 'qrcode.image.svg.SvgFragmentImage', 'svg-path': 'qrcode.image.svg.SvgPathImage', 'pymaging': 'qrcode.image.pure.PymagingImage'}
error_correction = {'L': qrcode.ERROR_CORRECT_L, 'M': qrcode.ERROR_CORRECT_M, 'Q': qrcode.ERROR_CORRECT_Q, 'H': qrcode.ERROR_CORRECT_H}

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    version = metadata.version('qrcode')
    parser = optparse.OptionParser(usage=(__doc__ or '').strip(), version=version)

    def raise_error(msg: str) -> NoReturn:
        parser.error(msg)
        raise
    parser.add_option('--factory', help=f'Full python path to the image factory class to create the image with. You can use the following shortcuts to the built-in image factory classes: {commas(default_factories)}.')
    parser.add_option('--factory-drawer', help=f'Use an alternate drawer. {get_drawer_help()}.')
    parser.add_option('--optimize', type=int, help='Optimize the data by looking for chunks of at least this many characters that could use a more efficient encoding method. Use 0 to turn off chunk optimization.')
    parser.add_option('--error-correction', type='choice', choices=sorted(error_correction.keys()), default='M', help='The error correction level to use. Choices are L (7%), M (15%, default), Q (25%), and H (30%).')
    parser.add_option('--ascii', help='Print as ascii even if stdout is piped.', action='store_true')
    parser.add_option('--output', help='The output file. If not specified, the image is sent to the standard output.')
    opts, args = parser.parse_args(args)
    if opts.factory:
        module = default_factories.get(opts.factory, opts.factory)
        try:
            image_factory = get_factory(module)
        except ValueError as e:
            raise_error(str(e))
    else:
        image_factory = None
    qr = qrcode.QRCode(error_correction=error_correction[opts.error_correction], image_factory=image_factory)
    if args:
        data = args[0]
        data = data.encode(errors='surrogateescape')
    else:
        data = sys.stdin.buffer.read()
    if opts.optimize is None:
        qr.add_data(data)
    else:
        qr.add_data(data, optimize=opts.optimize)
    if opts.output:
        img = qr.make_image()
        with Path(opts.output).open('wb') as out:
            img.save(out)
    else:
        if image_factory is None and (os.isatty(sys.stdout.fileno()) or opts.ascii):
            qr.print_ascii(tty=not opts.ascii)
            return
        kwargs = {}
        aliases: DrawerAliases | None = getattr(qr.image_factory, 'drawer_aliases', None)
        if opts.factory_drawer:
            if not aliases:
                raise_error('The selected factory has no drawer aliases.')
            if opts.factory_drawer not in aliases:
                raise_error(f'{opts.factory_drawer} factory drawer not found. Expected {commas(aliases)}')
            drawer_cls, drawer_kwargs = aliases[opts.factory_drawer]
            kwargs['module_drawer'] = drawer_cls(**drawer_kwargs)
        img = qr.make_image(**kwargs)
        sys.stdout.flush()
        img.save(sys.stdout.buffer)

def get_factory(module: str) -> type[BaseImage]:
    if '.' not in module:
        raise ValueError('The image factory is not a full python path')
    module, name = module.rsplit('.', 1)
    imp = __import__(module, {}, {}, [name])
    return getattr(imp, name)

def get_drawer_help() -> str:
    help: dict[str, set] = {}
    for alias, module in default_factories.items():
        try:
            image = get_factory(module)
        except ImportError:
            continue
        aliases: DrawerAliases | None = getattr(image, 'drawer_aliases', None)
        if not aliases:
            continue
        factories = help.setdefault(commas(aliases), set())
        factories.add(alias)
    return '. '.join((f"For {commas(factories, 'and')}, use: {aliases}" for aliases, factories in help.items()))

def commas(items: Iterable[str], joiner='or') -> str:
    items = tuple(items)
    if not items:
        return ''
    if len(items) == 1:
        return items[0]
    return f"{', '.join(items[:-1])} {joiner} {items[-1]}"

# Populate namespace for qrcode.console_scripts
qrcode.console_scripts.default_factories = default_factories
qrcode.console_scripts.error_correction = error_correction
qrcode.console_scripts.main = main
qrcode.console_scripts.get_factory = get_factory
qrcode.console_scripts.get_drawer_help = get_drawer_help
qrcode.console_scripts.commas = commas

# ============================================================
# Module: qrcode.compat
# Original: python-qrcode/qrcode/compat/__init__.py
# ============================================================



# ============================================================
# Module: qrcode.compat.etree
# Original: python-qrcode/qrcode/compat/etree.py
# ============================================================

try:
    import lxml.etree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# ============================================================
# Module: qrcode.image.styles.colormasks
# Original: python-qrcode/qrcode/image/styles/colormasks.py
# ============================================================

class QRColorMask:
    """
    QRColorMask is used to color in the QRCode.

    By the time apply_mask is called, the QRModuleDrawer of the StyledPilImage
    will have drawn all of the modules on the canvas (the color of these
    modules will be mostly black, although antialiasing may result in
    gradients) In the base class, apply_mask is implemented such that the
    background color will remain, but the foreground pixels will be replaced by
    a color determined by a call to get_fg_pixel. There is additional
    calculation done to preserve the gradient artifacts of antialiasing.

    All QRColorMask objects should be careful about RGB vs RGBA color spaces.

    For examples of what these look like, see doc/color_masks.png
    """
    back_color = (255, 255, 255)
    has_transparency = False
    paint_color = back_color

    def initialize(self, styledPilImage, image):
        self.paint_color = styledPilImage.paint_color

    def apply_mask(self, image, use_cache=False):
        width, height = image.size
        pixels = image.load()
        fg_color_cache = {} if use_cache else None
        for x in range(width):
            for y in range(height):
                current_color = pixels[x, y]
                if current_color == self.back_color:
                    continue
                if use_cache and current_color in fg_color_cache:
                    pixels[x, y] = fg_color_cache[current_color]
                    continue
                norm = self.extrap_color(self.back_color, self.paint_color, current_color)
                if norm is not None:
                    new_color = self.interp_color(self.get_bg_pixel(image, x, y), self.get_fg_pixel(image, x, y), norm)
                    pixels[x, y] = new_color
                    if use_cache:
                        fg_color_cache[current_color] = new_color
                else:
                    pixels[x, y] = self.get_bg_pixel(image, x, y)

    def get_fg_pixel(self, image, x, y):
        raise NotImplementedError('QRModuleDrawer.paint_fg_pixel')

    def get_bg_pixel(self, image, x, y):
        return self.back_color

    def interp_num(self, n1, n2, norm):
        return int(n2 * norm + n1 * (1 - norm))

    def interp_color(self, col1, col2, norm):
        return tuple((self.interp_num(col1[i], col2[i], norm) for i in range(len(col1))))

    def extrap_num(self, n1, n2, interped_num):
        if n2 == n1:
            return None
        return (interped_num - n1) / (n2 - n1)

    def extrap_color(self, col1, col2, interped_color):
        normed = []
        for c1, c2, ci in zip(col1, col2, interped_color):
            extrap = self.extrap_num(c1, c2, ci)
            if extrap is not None:
                normed.append(extrap)
        if not normed:
            return None
        return sum(normed) / len(normed)

class SolidFillColorMask(QRColorMask):
    """
    Just fills in the background with one color and the foreground with another
    """

    def __init__(self, back_color=(255, 255, 255), front_color=(0, 0, 0)):
        self.back_color = back_color
        self.front_color = front_color
        self.has_transparency = len(self.back_color) == 4

    def apply_mask(self, image):
        if self.back_color == (255, 255, 255) and self.front_color == (0, 0, 0):
            pass
        else:
            QRColorMask.apply_mask(self, image, use_cache=True)

    def get_fg_pixel(self, image, x, y):
        return self.front_color

class RadialGradiantColorMask(QRColorMask):
    """
    Fills in the foreground with a radial gradient from the center to the edge
    """

    def __init__(self, back_color=(255, 255, 255), center_color=(0, 0, 0), edge_color=(0, 0, 255)):
        self.back_color = back_color
        self.center_color = center_color
        self.edge_color = edge_color
        self.has_transparency = len(self.back_color) == 4

    def get_fg_pixel(self, image, x, y):
        width, _ = image.size
        normedDistanceToCenter = math.sqrt((x - width / 2) ** 2 + (y - width / 2) ** 2) / (math.sqrt(2) * width / 2)
        return self.interp_color(self.center_color, self.edge_color, normedDistanceToCenter)

class SquareGradiantColorMask(QRColorMask):
    """
    Fills in the foreground with a square gradient from the center to the edge
    """

    def __init__(self, back_color=(255, 255, 255), center_color=(0, 0, 0), edge_color=(0, 0, 255)):
        self.back_color = back_color
        self.center_color = center_color
        self.edge_color = edge_color
        self.has_transparency = len(self.back_color) == 4

    def get_fg_pixel(self, image, x, y):
        width, _ = image.size
        normedDistanceToCenter = max(abs(x - width / 2), abs(y - width / 2)) / (width / 2)
        return self.interp_color(self.center_color, self.edge_color, normedDistanceToCenter)

class HorizontalGradiantColorMask(QRColorMask):
    """
    Fills in the foreground with a gradient sweeping from the left to the right
    """

    def __init__(self, back_color=(255, 255, 255), left_color=(0, 0, 0), right_color=(0, 0, 255)):
        self.back_color = back_color
        self.left_color = left_color
        self.right_color = right_color
        self.has_transparency = len(self.back_color) == 4

    def get_fg_pixel(self, image, x, y):
        width, _ = image.size
        return self.interp_color(self.left_color, self.right_color, x / width)

class VerticalGradiantColorMask(QRColorMask):
    """
    Fills in the forefround with a gradient sweeping from the top to the bottom
    """

    def __init__(self, back_color=(255, 255, 255), top_color=(0, 0, 0), bottom_color=(0, 0, 255)):
        self.back_color = back_color
        self.top_color = top_color
        self.bottom_color = bottom_color
        self.has_transparency = len(self.back_color) == 4

    def get_fg_pixel(self, image, x, y):
        width, _ = image.size
        return self.interp_color(self.top_color, self.bottom_color, y / width)

class ImageColorMask(QRColorMask):
    """
    Fills in the foreground with pixels from another image, either passed by
    path or passed by image object.
    """

    def __init__(self, back_color=(255, 255, 255), color_mask_path=None, color_mask_image=None):
        self.back_color = back_color
        if color_mask_image:
            self.color_img = color_mask_image
        else:
            self.color_img = Image.open(color_mask_path)
        self.has_transparency = len(self.back_color) == 4

    def initialize(self, styledPilImage, image):
        self.paint_color = styledPilImage.paint_color
        self.color_img = self.color_img.resize(image.size)

    def get_fg_pixel(self, image, x, y):
        width, _ = image.size
        return self.color_img.getpixel((x, y))

# Populate namespace for qrcode.image.styles.colormasks
qrcode.image.styles.colormasks.QRColorMask = QRColorMask
qrcode.image.styles.colormasks.SolidFillColorMask = SolidFillColorMask
qrcode.image.styles.colormasks.RadialGradiantColorMask = RadialGradiantColorMask
qrcode.image.styles.colormasks.SquareGradiantColorMask = SquareGradiantColorMask
qrcode.image.styles.colormasks.HorizontalGradiantColorMask = HorizontalGradiantColorMask
qrcode.image.styles.colormasks.VerticalGradiantColorMask = VerticalGradiantColorMask
qrcode.image.styles.colormasks.ImageColorMask = ImageColorMask

# ============================================================
# Module: qrcode.image.styles.moduledrawers.pil
# Original: python-qrcode/qrcode/image/styles/moduledrawers/pil.py
# ============================================================

ANTIALIASING_FACTOR = 4

class StyledPilQRModuleDrawer(QRModuleDrawer):
    """
    A base class for StyledPilImage module drawers.

    NOTE: the color that this draws in should be whatever is equivalent to
    black in the color space, and the specified QRColorMask will handle adding
    colors as necessary to the image
    """
    img: 'StyledPilImage'

class SquareModuleDrawer(StyledPilQRModuleDrawer):
    """
    Draws the modules as simple squares
    """

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.imgDraw = ImageDraw.Draw(self.img._img)

    def drawrect(self, box, is_active: bool):
        if is_active:
            self.imgDraw.rectangle(box, fill=self.img.paint_color)

class GappedSquareModuleDrawer(StyledPilQRModuleDrawer):
    """
    Draws the modules as simple squares that are not contiguous.

    The size_ratio determines how wide the squares are relative to the width of
    the space they are printed in
    """

    def __init__(self, size_ratio=0.8):
        self.size_ratio = size_ratio

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.imgDraw = ImageDraw.Draw(self.img._img)
        self.delta = (1 - self.size_ratio) * self.img.box_size / 2

    def drawrect(self, box, is_active: bool):
        if is_active:
            smaller_box = (box[0][0] + self.delta, box[0][1] + self.delta, box[1][0] - self.delta, box[1][1] - self.delta)
            self.imgDraw.rectangle(smaller_box, fill=self.img.paint_color)

class CircleModuleDrawer(StyledPilQRModuleDrawer):
    """
    Draws the modules as circles
    """
    circle = None

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        box_size = self.img.box_size
        fake_size = box_size * ANTIALIASING_FACTOR
        self.circle = Image.new(self.img.mode, (fake_size, fake_size), self.img.color_mask.back_color)
        ImageDraw.Draw(self.circle).ellipse((0, 0, fake_size, fake_size), fill=self.img.paint_color)
        self.circle = self.circle.resize((box_size, box_size), Image.Resampling.LANCZOS)

    def drawrect(self, box, is_active: bool):
        if is_active:
            self.img._img.paste(self.circle, (box[0][0], box[0][1]))

class GappedCircleModuleDrawer(StyledPilQRModuleDrawer):
    """
    Draws the modules as circles that are not contiguous.

    The size_ratio determines how wide the circles are relative to the width of
    the space they are printed in
    """
    circle = None

    def __init__(self, size_ratio=0.9):
        self.size_ratio = size_ratio

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        box_size = self.img.box_size
        fake_size = box_size * ANTIALIASING_FACTOR
        self.circle = Image.new(self.img.mode, (fake_size, fake_size), self.img.color_mask.back_color)
        ImageDraw.Draw(self.circle).ellipse((0, 0, fake_size, fake_size), fill=self.img.paint_color)
        smaller_size = int(self.size_ratio * box_size)
        self.circle = self.circle.resize((smaller_size, smaller_size), Image.Resampling.LANCZOS)

    def drawrect(self, box, is_active: bool):
        if is_active:
            self.img._img.paste(self.circle, (box[0][0], box[0][1]))

class RoundedModuleDrawer(StyledPilQRModuleDrawer):
    """
    Draws the modules with all 90 degree corners replaced with rounded edges.

    radius_ratio determines the radius of the rounded edges - a value of 1
    means that an isolated module will be drawn as a circle, while a value of 0
    means that the radius of the rounded edge will be 0 (and thus back to 90
    degrees again).
    """
    needs_neighbors = True

    def __init__(self, radius_ratio=1):
        self.radius_ratio = radius_ratio

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.corner_width = int(self.img.box_size / 2)
        self.setup_corners()

    def setup_corners(self):
        mode = self.img.mode
        back_color = self.img.color_mask.back_color
        front_color = self.img.paint_color
        self.SQUARE = Image.new(mode, (self.corner_width, self.corner_width), front_color)
        fake_width = self.corner_width * ANTIALIASING_FACTOR
        radius = self.radius_ratio * fake_width
        diameter = radius * 2
        base = Image.new(mode, (fake_width, fake_width), back_color)
        base_draw = ImageDraw.Draw(base)
        base_draw.ellipse((0, 0, diameter, diameter), fill=front_color)
        base_draw.rectangle((radius, 0, fake_width, fake_width), fill=front_color)
        base_draw.rectangle((0, radius, fake_width, fake_width), fill=front_color)
        self.NW_ROUND = base.resize((self.corner_width, self.corner_width), Image.Resampling.LANCZOS)
        self.SW_ROUND = self.NW_ROUND.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        self.SE_ROUND = self.NW_ROUND.transpose(Image.Transpose.ROTATE_180)
        self.NE_ROUND = self.NW_ROUND.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    def drawrect(self, box: list[list[int]], is_active: 'ActiveWithNeighbors'):
        if not is_active:
            return
        nw_rounded = not is_active.W and (not is_active.N)
        ne_rounded = not is_active.N and (not is_active.E)
        se_rounded = not is_active.E and (not is_active.S)
        sw_rounded = not is_active.S and (not is_active.W)
        nw = self.NW_ROUND if nw_rounded else self.SQUARE
        ne = self.NE_ROUND if ne_rounded else self.SQUARE
        se = self.SE_ROUND if se_rounded else self.SQUARE
        sw = self.SW_ROUND if sw_rounded else self.SQUARE
        self.img._img.paste(nw, (box[0][0], box[0][1]))
        self.img._img.paste(ne, (box[0][0] + self.corner_width, box[0][1]))
        self.img._img.paste(se, (box[0][0] + self.corner_width, box[0][1] + self.corner_width))
        self.img._img.paste(sw, (box[0][0], box[0][1] + self.corner_width))

class VerticalBarsDrawer(StyledPilQRModuleDrawer):
    """
    Draws vertically contiguous groups of modules as long rounded rectangles,
    with gaps between neighboring bands (the size of these gaps is inversely
    proportional to the horizontal_shrink).
    """
    needs_neighbors = True

    def __init__(self, horizontal_shrink=0.8):
        self.horizontal_shrink = horizontal_shrink

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.half_height = int(self.img.box_size / 2)
        self.delta = int((1 - self.horizontal_shrink) * self.half_height)
        self.setup_edges()

    def setup_edges(self):
        mode = self.img.mode
        back_color = self.img.color_mask.back_color
        front_color = self.img.paint_color
        height = self.half_height
        width = height * 2
        shrunken_width = int(width * self.horizontal_shrink)
        self.SQUARE = Image.new(mode, (shrunken_width, height), front_color)
        fake_width = width * ANTIALIASING_FACTOR
        fake_height = height * ANTIALIASING_FACTOR
        base = Image.new(mode, (fake_width, fake_height), back_color)
        base_draw = ImageDraw.Draw(base)
        base_draw.ellipse((0, 0, fake_width, fake_height * 2), fill=front_color)
        self.ROUND_TOP = base.resize((shrunken_width, height), Image.Resampling.LANCZOS)
        self.ROUND_BOTTOM = self.ROUND_TOP.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

    def drawrect(self, box, is_active: 'ActiveWithNeighbors'):
        if is_active:
            top_rounded = not is_active.N
            bottom_rounded = not is_active.S
            top = self.ROUND_TOP if top_rounded else self.SQUARE
            bottom = self.ROUND_BOTTOM if bottom_rounded else self.SQUARE
            self.img._img.paste(top, (box[0][0] + self.delta, box[0][1]))
            self.img._img.paste(bottom, (box[0][0] + self.delta, box[0][1] + self.half_height))

class HorizontalBarsDrawer(StyledPilQRModuleDrawer):
    """
    Draws horizontally contiguous groups of modules as long rounded rectangles,
    with gaps between neighboring bands (the size of these gaps is inversely
    proportional to the vertical_shrink).
    """
    needs_neighbors = True

    def __init__(self, vertical_shrink=0.8):
        self.vertical_shrink = vertical_shrink

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        self.half_width = int(self.img.box_size / 2)
        self.delta = int((1 - self.vertical_shrink) * self.half_width)
        self.setup_edges()

    def setup_edges(self):
        mode = self.img.mode
        back_color = self.img.color_mask.back_color
        front_color = self.img.paint_color
        width = self.half_width
        height = width * 2
        shrunken_height = int(height * self.vertical_shrink)
        self.SQUARE = Image.new(mode, (width, shrunken_height), front_color)
        fake_width = width * ANTIALIASING_FACTOR
        fake_height = height * ANTIALIASING_FACTOR
        base = Image.new(mode, (fake_width, fake_height), back_color)
        base_draw = ImageDraw.Draw(base)
        base_draw.ellipse((0, 0, fake_width * 2, fake_height), fill=front_color)
        self.ROUND_LEFT = base.resize((width, shrunken_height), Image.Resampling.LANCZOS)
        self.ROUND_RIGHT = self.ROUND_LEFT.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    def drawrect(self, box, is_active: 'ActiveWithNeighbors'):
        if is_active:
            left_rounded = not is_active.W
            right_rounded = not is_active.E
            left = self.ROUND_LEFT if left_rounded else self.SQUARE
            right = self.ROUND_RIGHT if right_rounded else self.SQUARE
            self.img._img.paste(left, (box[0][0], box[0][1] + self.delta))
            self.img._img.paste(right, (box[0][0] + self.half_width, box[0][1] + self.delta))

# Populate namespace for qrcode.image.styles.moduledrawers.pil
qrcode.image.styles.moduledrawers.pil.ANTIALIASING_FACTOR = ANTIALIASING_FACTOR
qrcode.image.styles.moduledrawers.pil.StyledPilQRModuleDrawer = StyledPilQRModuleDrawer
qrcode.image.styles.moduledrawers.pil.SquareModuleDrawer = SquareModuleDrawer
qrcode.image.styles.moduledrawers.pil.GappedSquareModuleDrawer = GappedSquareModuleDrawer
qrcode.image.styles.moduledrawers.pil.CircleModuleDrawer = CircleModuleDrawer
qrcode.image.styles.moduledrawers.pil.GappedCircleModuleDrawer = GappedCircleModuleDrawer
qrcode.image.styles.moduledrawers.pil.RoundedModuleDrawer = RoundedModuleDrawer
qrcode.image.styles.moduledrawers.pil.VerticalBarsDrawer = VerticalBarsDrawer
qrcode.image.styles.moduledrawers.pil.HorizontalBarsDrawer = HorizontalBarsDrawer

# ============================================================
# Module: qrcode.image.styledpil
# Original: python-qrcode/qrcode/image/styledpil.py
# ============================================================

class StyledPilImage(qrcode.image.base.BaseImageWithDrawer):
    """
    Styled PIL image builder, default format is PNG.

    This differs from the PilImage in that there is a module_drawer, a
    color_mask, and an optional image

    The module_drawer should extend the QRModuleDrawer class and implement the
    drawrect_context(self, box, active, context), and probably also the
    initialize function. This will draw an individual "module" or square on
    the QR code.

    The color_mask will extend the QRColorMask class and will at very least
    implement the get_fg_pixel(image, x, y) function, calculating a color to
    put on the image at the pixel location (x,y) (more advanced functionality
    can be gotten by instead overriding other functions defined in the
    QRColorMask class)

    The Image can be specified either by path or with a Pillow Image, and if it
    is there will be placed in the middle of the QR code. No effort is done to
    ensure that the QR code is still legible after the image has been placed
    there; Q or H level error correction levels are recommended to maintain
    data integrity A resampling filter can be specified (defaulting to
    PIL.Image.Resampling.LANCZOS) for resizing; see PIL.Image.resize() for possible
    options for this parameter.
    The image size can be controlled by `embedded_image_ratio` which is a ratio
    between 0 and 1 that's set in relation to the overall width of the QR code.
    """
    kind = 'PNG'
    needs_processing = True
    color_mask: QRColorMask
    default_drawer_class = SquareModuleDrawer

    def __init__(self, *args, **kwargs):
        self.color_mask = kwargs.get('color_mask', SolidFillColorMask())
        if kwargs.get('embeded_image_path') or kwargs.get('embeded_image'):
            warnings.warn("The 'embeded_*' parameters are deprecated. Use 'embedded_image_path' or 'embedded_image' instead. The 'embeded_*' parameters will be removed in v9.0.", category=DeprecationWarning, stacklevel=2)
        embedded_image_path = kwargs.get('embedded_image_path', kwargs.get('embeded_image_path'))
        self.embedded_image = kwargs.get('embedded_image', kwargs.get('embeded_image'))
        self.embedded_image_ratio = kwargs.get('embedded_image_ratio', kwargs.get('embeded_image_ratio', 0.25))
        self.embedded_image_resample = kwargs.get('embedded_image_resample', kwargs.get('embeded_image_resample', Image.Resampling.LANCZOS))
        if not self.embedded_image and embedded_image_path:
            self.embedded_image = Image.open(embedded_image_path)
        self.paint_color = tuple((0 for i in self.color_mask.back_color))
        if self.color_mask.has_transparency:
            self.paint_color = (*self.color_mask.back_color[:3], 255)
        super().__init__(*args, **kwargs)

    @overload
    def drawrect(self, row, col):
        """
        Not used.
        """

    def new_image(self, **kwargs):
        mode = 'RGBA' if self.color_mask.has_transparency or (self.embedded_image and 'A' in self.embedded_image.getbands()) else 'RGB'
        back_color = self.color_mask.back_color
        return Image.new(mode, (self.pixel_size, self.pixel_size), back_color)

    def init_new_image(self):
        self.color_mask.initialize(self, self._img)
        super().init_new_image()

    def process(self):
        self.color_mask.apply_mask(self._img)
        if self.embedded_image:
            self.draw_embedded_image()

    def draw_embeded_image(self):
        return self.draw_embedded_image()

    def draw_embedded_image(self):
        if not self.embedded_image:
            return
        total_width, _ = self._img.size
        total_width = int(total_width)
        logo_width_ish = int(total_width * self.embedded_image_ratio)
        logo_offset = int((int(total_width / 2) - int(logo_width_ish / 2)) / self.box_size) * self.box_size
        logo_position = (logo_offset, logo_offset)
        logo_width = total_width - logo_offset * 2
        region = self.embedded_image
        region = region.resize((logo_width, logo_width), self.embedded_image_resample)
        if 'A' in region.getbands():
            self._img.alpha_composite(region, logo_position)
        else:
            self._img.paste(region, logo_position)

    def save(self, stream, format=None, **kwargs):
        if format is None:
            format = kwargs.get('kind', self.kind)
        kwargs.pop('kind', None)
        self._img.save(stream, format=format, **kwargs)

    def __getattr__(self, name):
        return getattr(self._img, name)

# Populate namespace for qrcode.image.styledpil
qrcode.image.styledpil.StyledPilImage = StyledPilImage

# ============================================================
# Module: qrcode.image.styles
# Original: python-qrcode/qrcode/image/styles/__init__.py
# ============================================================



# ============================================================
# Module: qrcode.image.styles.moduledrawers
# Original: python-qrcode/qrcode/image/styles/moduledrawers/__init__.py
# ============================================================

"""
Module for lazy importing of PIL drawers with a deprecation warning.

Currently, importing a PIL drawer from this module is allowed for backwards
compatibility but will raise a DeprecationWarning.

This will be removed in v9.0.
"""

def __getattr__(name):
    """Lazy import with deprecation warning for PIL drawers."""
    pil_drawers = {'CircleModuleDrawer', 'GappedCircleModuleDrawer', 'GappedSquareModuleDrawer', 'HorizontalBarsDrawer', 'RoundedModuleDrawer', 'SquareModuleDrawer', 'VerticalBarsDrawer'}
    if name in pil_drawers:
        if PIL_AVAILABLE:
            warnings.warn(f"Importing '{name}' directly from this module is deprecated.Please use 'from qrcode.image.styles.moduledrawers.pil import {name}' instead. This backwards compatibility import will be removed in v9.0.", DeprecationWarning, stacklevel=2)
        return getattr(pil, name)
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')

# Populate namespace for qrcode.image.styles.moduledrawers
qrcode.image.styles.moduledrawers.__getattr__ = __getattr__

# ============================================================
# Module: qrcode.image.styles.moduledrawers.svg
# Original: python-qrcode/qrcode/image/styles/moduledrawers/svg.py
# ============================================================

ANTIALIASING_FACTOR = 4

class Coords(NamedTuple):
    x0: Decimal
    y0: Decimal
    x1: Decimal
    y1: Decimal
    xh: Decimal
    yh: Decimal

class BaseSvgQRModuleDrawer(QRModuleDrawer):
    img: 'SvgFragmentImage'

    def __init__(self, *, size_ratio: Decimal=Decimal(1), **kwargs):
        super().__init__(**kwargs)
        self.size_ratio = size_ratio

    def initialize(self, *args, **kwargs) -> None:
        super().initialize(*args, **kwargs)
        self.box_delta = (1 - self.size_ratio) * self.img.box_size / 2
        self.box_size = Decimal(self.img.box_size) * self.size_ratio
        self.box_half = self.box_size / 2

    def coords(self, box) -> Coords:
        row, col = box[0]
        x = row + self.box_delta
        y = col + self.box_delta
        return Coords(x, y, x + self.box_size, y + self.box_size, x + self.box_half, y + self.box_half)

class SvgQRModuleDrawer(BaseSvgQRModuleDrawer):
    tag = 'rect'

    def initialize(self, *args, **kwargs) -> None:
        super().initialize(*args, **kwargs)

    def drawrect(self, box, is_active: bool):
        if not is_active:
            return
        self.img._img.append(self.el(box))

    @abc.abstractmethod
    def el(self, box):
        ...

class SvgSquareDrawer(SvgQRModuleDrawer):

    def initialize(self, *args, **kwargs) -> None:
        super().initialize(*args, **kwargs)
        self.unit_size = self.img.units(self.box_size)

    def el(self, box):
        coords = self.coords(box)
        return ET.Element(self.tag, x=self.img.units(coords.x0), y=self.img.units(coords.y0), width=self.unit_size, height=self.unit_size)

class SvgCircleDrawer(SvgQRModuleDrawer):
    tag = 'circle'

    def initialize(self, *args, **kwargs) -> None:
        super().initialize(*args, **kwargs)
        self.radius = self.img.units(self.box_half)

    def el(self, box):
        coords = self.coords(box)
        return ET.Element(self.tag, cx=self.img.units(coords.xh), cy=self.img.units(coords.yh), r=self.radius)

class SvgPathQRModuleDrawer(BaseSvgQRModuleDrawer):
    img: 'SvgPathImage'

    def drawrect(self, box, is_active: bool):
        if not is_active:
            return
        self.img._subpaths.append(self.subpath(box))

    @abc.abstractmethod
    def subpath(self, box) -> str:
        ...

class SvgPathSquareDrawer(SvgPathQRModuleDrawer):

    def subpath(self, box) -> str:
        coords = self.coords(box)
        x0 = self.img.units(coords.x0, text=False)
        y0 = self.img.units(coords.y0, text=False)
        x1 = self.img.units(coords.x1, text=False)
        y1 = self.img.units(coords.y1, text=False)
        return f'M{x0},{y0}H{x1}V{y1}H{x0}z'

class SvgPathCircleDrawer(SvgPathQRModuleDrawer):

    def initialize(self, *args, **kwargs) -> None:
        super().initialize(*args, **kwargs)

    def subpath(self, box) -> str:
        coords = self.coords(box)
        x0 = self.img.units(coords.x0, text=False)
        yh = self.img.units(coords.yh, text=False)
        h = self.img.units(self.box_half - self.box_delta, text=False)
        x1 = self.img.units(coords.x1, text=False)
        return f'M{x0},{yh}A{h},{h} 0 0 0 {x1},{yh}A{h},{h} 0 0 0 {x0},{yh}z'

# Populate namespace for qrcode.image.styles.moduledrawers.svg
qrcode.image.styles.moduledrawers.svg.ANTIALIASING_FACTOR = ANTIALIASING_FACTOR
qrcode.image.styles.moduledrawers.svg.Coords = Coords
qrcode.image.styles.moduledrawers.svg.BaseSvgQRModuleDrawer = BaseSvgQRModuleDrawer
qrcode.image.styles.moduledrawers.svg.SvgQRModuleDrawer = SvgQRModuleDrawer
qrcode.image.styles.moduledrawers.svg.SvgSquareDrawer = SvgSquareDrawer
qrcode.image.styles.moduledrawers.svg.SvgCircleDrawer = SvgCircleDrawer
qrcode.image.styles.moduledrawers.svg.SvgPathQRModuleDrawer = SvgPathQRModuleDrawer
qrcode.image.styles.moduledrawers.svg.SvgPathSquareDrawer = SvgPathSquareDrawer
qrcode.image.styles.moduledrawers.svg.SvgPathCircleDrawer = SvgPathCircleDrawer

# ============================================================
# Module: qrcode.image.svg
# Original: python-qrcode/qrcode/image/svg.py
# ============================================================

class SvgFragmentImage(qrcode.image.base.BaseImageWithDrawer):
    """
    SVG image builder

    Creates a QR-code image as a SVG document fragment.
    """
    _SVG_namespace = 'http://www.w3.org/2000/svg'
    kind = 'SVG'
    allowed_kinds = ('SVG',)
    default_drawer_class: type[QRModuleDrawer] = svg_drawers.SvgSquareDrawer

    def __init__(self, *args, **kwargs):
        ET.register_namespace('svg', self._SVG_namespace)
        super().__init__(*args, **kwargs)
        self.unit_size = self.units(self.box_size)

    @overload
    def drawrect(self, row, col):
        """
        Not used.
        """

    @overload
    def units(self, pixels: int | Decimal, text: Literal[False]) -> Decimal:
        ...

    @overload
    def units(self, pixels: int | Decimal, text: Literal[True]=True) -> str:
        ...

    def units(self, pixels, text=True):
        """
        A box_size of 10 (default) equals 1mm.
        """
        units = Decimal(pixels) / 10
        if not text:
            return units
        units = units.quantize(Decimal('0.001'))
        context = decimal.Context(traps=[decimal.Inexact])
        try:
            for d in (Decimal('0.01'), Decimal('0.1'), Decimal(0)):
                units = units.quantize(d, context=context)
        except decimal.Inexact:
            pass
        return f'{units}mm'

    def save(self, stream, kind=None):
        self.check_kind(kind=kind)
        self._write(stream)

    def to_string(self, **kwargs):
        return ET.tostring(self._img, **kwargs)

    def new_image(self, **kwargs):
        return self._svg(**kwargs)

    def _svg(self, tag=None, version='1.1', **kwargs):
        if tag is None:
            tag = ET.QName(self._SVG_namespace, 'svg')
        dimension = self.units(self.pixel_size)
        return ET.Element(tag, width=dimension, height=dimension, version=version, **kwargs)

    def _write(self, stream):
        ET.ElementTree(self._img).write(stream, xml_declaration=False)

class SvgImage(SvgFragmentImage):
    """
    Standalone SVG image builder

    Creates a QR-code image as a standalone SVG document.
    """
    background: str | None = None
    drawer_aliases: qrcode.image.base.DrawerAliases = {'circle': (svg_drawers.SvgCircleDrawer, {}), 'gapped-circle': (svg_drawers.SvgCircleDrawer, {'size_ratio': Decimal('0.8')}), 'gapped-square': (svg_drawers.SvgSquareDrawer, {'size_ratio': Decimal('0.8')})}

    def _svg(self, tag='svg', **kwargs):
        svg = super()._svg(tag=tag, **kwargs)
        svg.set('xmlns', self._SVG_namespace)
        if self.background:
            svg.append(ET.Element('rect', fill=self.background, x='0', y='0', width='100%', height='100%'))
        return svg

    def _write(self, stream):
        ET.ElementTree(self._img).write(stream, encoding='UTF-8', xml_declaration=True)

class SvgPathImage(SvgImage):
    """
    SVG image builder with one single <path> element (removes white spaces
    between individual QR points).
    """
    QR_PATH_STYLE = {'fill': '#000000', 'fill-opacity': '1', 'fill-rule': 'nonzero', 'stroke': 'none'}
    needs_processing = True
    path: ET.Element | None = None
    default_drawer_class: type[QRModuleDrawer] = svg_drawers.SvgPathSquareDrawer
    drawer_aliases = {'circle': (svg_drawers.SvgPathCircleDrawer, {}), 'gapped-circle': (svg_drawers.SvgPathCircleDrawer, {'size_ratio': Decimal('0.8')}), 'gapped-square': (svg_drawers.SvgPathSquareDrawer, {'size_ratio': Decimal('0.8')})}

    def __init__(self, *args, **kwargs):
        self._subpaths: list[str] = []
        super().__init__(*args, **kwargs)

    def _svg(self, viewBox=None, **kwargs):
        if viewBox is None:
            dimension = self.units(self.pixel_size, text=False)
            viewBox = f'0 0 {dimension} {dimension}'
        return super()._svg(viewBox=viewBox, **kwargs)

    def process(self):
        self.path = ET.Element(ET.QName('path'), d=''.join(self._subpaths), **self.QR_PATH_STYLE)
        self._subpaths = []
        self._img.append(self.path)

class SvgFillImage(SvgImage):
    """
    An SvgImage that fills the background to white.
    """
    background = 'white'

class SvgPathFillImage(SvgPathImage):
    """
    An SvgPathImage that fills the background to white.
    """
    background = 'white'

# Populate namespace for qrcode.image.svg
qrcode.image.svg.SvgFragmentImage = SvgFragmentImage
qrcode.image.svg.SvgImage = SvgImage
qrcode.image.svg.SvgPathImage = SvgPathImage
qrcode.image.svg.SvgFillImage = SvgFillImage
qrcode.image.svg.SvgPathFillImage = SvgPathFillImage

# ============================================================
# Module: qrcode.release
# Original: python-qrcode/qrcode/release.py
# ============================================================

"""
This file provides zest.releaser entrypoints using when releasing new
qrcode versions.
"""

def update_manpage(data):
    """
    Update the version in the manpage document.
    """
    if data['name'] != 'qrcode':
        return
    base_dir = Path(__file__).parent.parent.resolve()
    filename = base_dir / 'doc' / 'qr.1'
    with filename.open('r') as f:
        lines = f.readlines()
    changed = False
    for i, line in enumerate(lines):
        if not line.startswith('.TH '):
            continue
        parts = re.split('"([^"]*)"', line)
        if len(parts) < 5:
            continue
        changed = parts[3] != data['new_version']
        if changed:
            parts[3] = data['new_version']
            parts[1] = datetime.datetime.now(tz=datetime.timezone.utc).strftime('%-d %b %Y')
            lines[i] = '"'.join(parts)
        break
    if changed:
        with filename.open('w') as f:
            for line in lines:
                f.write(line)

# Populate namespace for qrcode.release
qrcode.release.update_manpage = update_manpage

# Entry point for CLI usage
if __name__ == '__main__':
    main()
