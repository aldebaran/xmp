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
import os.path

# Xmp
from ..xmp import XMPFile

class XMPCommand:
	@staticmethod
	def show(args):
		throwIfAbsent(args.file)
		input_file_path = args.file
		with XMPFile(input_file_path) as xmp_file:
			print xmp_file

	@staticmethod
	def xml(args):
		throwIfAbsent(args.file)
		input_file_path = args.file
		with XMPFile(input_file_path) as xmp_file:
			print xmp_file.metadata.xml()

	@staticmethod
	def set(args):
		throwIfAbsent(args.file)
		print "Setting property {ns}:{p} of file {f} to {v}".format(
			ns = args.namespace,
			 p = args.property,
			 v = args.value,
			 f = args.file
		)
		input_file_path = args.file
		with XMPFile(input_file_path) as xmp_file:
			pass
			# TODO

	@staticmethod
	def delete(args):
		throwIfAbsent(args.file)
		print "Deleting property {ns}:{p} of file {f}".format(
			ns = args.namespace,
			 p = args.property,
			 v = args.value,
			 f = args.file
		)
		input_file_path = args.file
		with XMPFile(input_file_path) as xmp_file:
			pass
			# TODO

# ───────
# Helpers

def throwIfAbsent(file_path):
	if not os.path.isfile(file_path):
		import sys
		sys.exit("File "+file_path+" doesn't exist")
