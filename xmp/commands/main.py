# -*- coding: utf-8 -*-

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
