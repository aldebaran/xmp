# -*- coding: utf-8 -*-

# Copyright (c) 2017, Softbank Robotics Europe
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Standard Library
import errno
import os
import shutil
# libXMP
import libxmp.consts

# ──────────
# Parameters

DATA_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/")
SANDBOX_FOLDER = "/tmp/qidata/"

# ───────────
# Groundtruth

JPG_PHOTO = "SpringNebula.jpg"
JPG_PHOTO_NS_UIDS = [
	libxmp.consts.XMP_NS_EXIF,
	libxmp.consts.XMP_NS_TIFF,
	libxmp.consts.XMP_NS_XMP,
	libxmp.consts.XMP_NS_Photoshop
]
JPG_PHOTO_NS_LEN = {
	libxmp.consts.XMP_NS_EXIF      : 31,
	libxmp.consts.XMP_NS_TIFF      : 7,
	libxmp.consts.XMP_NS_XMP       : 3,
	libxmp.consts.XMP_NS_Photoshop : 1,
}

# ─────────
# Utilities

def createSandbox():
	try:
		os.mkdir(SANDBOX_FOLDER)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise

def sandboxedData(file_path):
	"""
	Makes a copy of the given file in /tmp and returns its path.
	"""
	createSandbox()
	source_path = os.path.join(DATA_FOLDER,    file_path)
	tmp_path    = os.path.join(SANDBOX_FOLDER, file_path)
	shutil.copyfile(source_path, tmp_path)

	return tmp_path
