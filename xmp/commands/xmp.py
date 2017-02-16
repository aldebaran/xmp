# -*- coding: utf-8 -*-

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
