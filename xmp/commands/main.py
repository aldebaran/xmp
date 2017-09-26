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

# Argparse
import argparse
try:
	import argcomplete
	has_argcomplete = True
except ImportError:
	has_argcomplete = False

# xmp
from .xmp import XMPCommand
from .. import version

DESCRIPTION = "Manipulate XMP metadata"

def make_command_parser(parent_parser=argparse.ArgumentParser(description=DESCRIPTION)):
	subparsers = parent_parser.add_subparsers()

	parent_parser.add_argument("-v", "--version", action=version.VersionAction, nargs=0,
	                           help="print xmp release version number")

	# ────────────────
	# show sub-command

	show_parser = subparsers.add_parser("show", description="show XMP")
	file_argument = show_parser.add_argument("file", help="what to examine")
	if has_argcomplete: file_argument.completer = argcomplete.completers.FilesCompleter()
	show_parser.set_defaults(func=XMPCommand.show)

	# ───────────────
	# xml sub-command

	xml_parser = subparsers.add_parser("xml", description="show XMP as XML")
	file_argument = xml_parser.add_argument("file", help="what to examine")
	if has_argcomplete: file_argument.completer = argcomplete.completers.FilesCompleter()
	xml_parser.set_defaults(func=XMPCommand.xml)

	# ───────────────
	# set sub-command

	set_parser = subparsers.add_parser("set", description="modify an XMP property")
	file_argument      = set_parser.add_argument("file", help="file to modify")
	namespace_argument = set_parser.add_argument("namespace", help="namespace to operate on")
	property_argument  = set_parser.add_argument("property", help="XMP property to set")
	value_argument     = set_parser.add_argument("value", help="XMP property to set")
	if has_argcomplete: file_argument.completer = argcomplete.completers.FilesCompleter()
	set_parser.set_defaults(func=XMPCommand.set)

	# ──────────────────
	# delete sub-command

	delete_parser = subparsers.add_parser("delete", description="delete an XMP property")
	file_argument      = delete_parser.add_argument("file", help="file to modify")
	namespace_argument = delete_parser.add_argument("namespace", help="namespace to operate on")
	property_argument  = delete_parser.add_argument("property", help="XMP property to set")
	if has_argcomplete: file_argument.completer = argcomplete.completers.FilesCompleter()
	delete_parser.set_defaults(func=XMPCommand.delete)

	return parent_parser

main_parser = make_command_parser()
