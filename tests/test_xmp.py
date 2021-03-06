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
import collections
import errno
import os
import unittest
import shutil
# libXMP
import libxmp.consts
# Xmp
from xmp.xmp import (XMPFile, XMPMetadata,
                     XMPElement,   XMPVirtualElement,
                     XMPNamespace, XMPStructure, XMPArray, XMPSet, XMPValue,
                     registerNamespace)
import fixtures

TEST_NS = u"http://test.com/xmp/test/1"
PREFIX = "test"
registerNamespace(TEST_NS, PREFIX)

def sha1(file_path):
	import hashlib
	hasher = hashlib.sha1()
	with open(file_path,'rb') as file:
		file_data = file.read()
	hasher.update(file_data)
	return hasher.hexdigest()

class XMPFileTests(unittest.TestCase):
	def setUp(self):
		self.jpg_path = fixtures.sandboxedData(fixtures.JPG_PHOTO)

		fixtures.createSandbox()
		self.xmp_extension_path = os.path.join(fixtures.SANDBOX_FOLDER, "test.xmp")
		if os.path.exists(self.xmp_extension_path):
			os.remove(self.xmp_extension_path)

	def test_contextmanager_noop(self):
		original_sha1 = sha1(self.jpg_path)
		with XMPFile(self.jpg_path):
			pass
		noop_sha1 = sha1(self.jpg_path)
		self.assertEqual(original_sha1, noop_sha1)

	def test_modify_readonly(self):
		import warnings
		with warnings.catch_warnings(record=True) as w:
			warnings.simplefilter("always")
			with XMPFile(self.jpg_path) as f:
				tst_prefix = f.libxmp_metadata.get_prefix_for_namespace(TEST_NS)
				f.libxmp_metadata.set_property(schema_ns=TEST_NS,
				                               prop_name=tst_prefix+"Property",
				                               prop_value="Value")
			self.assertEqual(len(w), 1)
			self.assertEqual(w[-1].category, RuntimeWarning)

	def test_modify_readwrite(self):
		original_sha1 = sha1(self.jpg_path)
		with XMPFile(self.jpg_path, rw=True) as f:
			tst_prefix = f.libxmp_metadata.get_prefix_for_namespace(TEST_NS)
			f.libxmp_metadata.set_property(schema_ns=TEST_NS,
			                               prop_name=tst_prefix+"Property",
			                               prop_value="Value")
		modified_sha1 = sha1(self.jpg_path)
		self.assertNotEqual(original_sha1, modified_sha1)

	def test_xmp_file_open(self):
		with XMPFile(fixtures.sandboxedData("foo.xmp")) as file:
			namespaces = file.metadata.namespaces
			self.assertIsInstance(namespaces, collections.Sequence)
			self.assertEqual(len(namespaces), 1)

			namespace = namespaces[0]
			self.assertIsInstance(namespace, XMPNamespace)
			self.assertEqual(namespace.uid, "http://test.com/xmp/test/1")
			self.assertIsInstance(namespace.structure, XMPValue)
			self.assertEqual(namespace.structure.value, "value")

	def test_xmp_file_creation(self):
		with XMPFile(self.xmp_extension_path, rw=True) as xmp_file:
			xmp_file.metadata[TEST_NS].structure = "value"
		self.assertTrue(os.path.exists(self.xmp_extension_path))
		with XMPFile(self.xmp_extension_path) as xmp_file:
			self.assertEqual(xmp_file.metadata[TEST_NS].structure.value, "value")

class XMPTestCase(unittest.TestCase):
	def setUp(self):
		self.EXPECTED_NS_UIDS = fixtures.JPG_PHOTO_NS_UIDS

		self.xmp_file = XMPFile(fixtures.sandboxedData(fixtures.JPG_PHOTO))
		self.xmp_file.__enter__()
		self.example_xmp = self.xmp_file.metadata

	def tearDown(self):
		self.xmp_file.__exit__(None, None, None)

class XMP(XMPTestCase):
	def test_empty_init(self):
		empty_xmp = XMPMetadata()
		self.assertEqual(len(empty_xmp.namespaces), 0)

	def test_len(self):
		self.assertEqual(len(self.example_xmp), 4)

	def test_namespaces_property_types(self):
		namespaces = self.example_xmp.namespaces
		self.assertIsInstance(namespaces, list)
		self.assertTrue(all([isinstance(n,XMPNamespace) for n in namespaces]))

	def test_getitem(self):
		for ns_uid in self.EXPECTED_NS_UIDS:
			self.assertIsInstance(self.example_xmp[ns_uid], XMPNamespace)

	def test_create_namespace(self):
		empty_xmp = XMPMetadata()
		self.assertEqual(len(empty_xmp.namespaces), 0)

class XMPNamespaceTests(XMPTestCase):
	def setUp(self):
		super(XMPNamespaceTests, self).setUp()
		self.exif_ns = self.example_xmp[libxmp.consts.XMP_NS_EXIF]

	def test_address(self):
		namespaces = self.example_xmp.namespaces
		read_uids  = [n.uid for n in namespaces]
		self.assertListEqual(read_uids, self.EXPECTED_NS_UIDS)

	def test_len(self):
		for ns_uid in self.EXPECTED_NS_UIDS:
			ns = self.example_xmp[ns_uid]
			self.assertEqual(len(ns), fixtures.JPG_PHOTO_NS_LEN[ns_uid])

	def test_getitem(self):
		self.assertIsInstance(self.exif_ns["LightSource"], XMPElement)
		self.assertIsInstance(self.exif_ns["Flash/Function"], XMPElement)
		self.assertIsInstance(self.exif_ns["exif:Flash/exif:Function"], XMPElement)
		with self.assertRaises(KeyError):
			self.exif_ns["Flashing"]
		with self.assertRaises(KeyError):
			self.exif_ns["Flash/Functioning"]

class TreeMixinsTests(XMPTestCase):
	def setUp(self):
		super(TreeMixinsTests, self).setUp()
		self.exif_ns = self.example_xmp[libxmp.consts.XMP_NS_EXIF]
		self.root_structure = self.exif_ns.Flash
		self.root_array = self.exif_ns.ISOSpeedRatings
		self.nested_structure = self.exif_ns.Flash.Function

	def test_namespace_uid(self):
		self.assertEqual(self.root_structure.namespace_uid, libxmp.consts.XMP_NS_EXIF)

	def test_is_top_level(self):
		self.assertTrue(self.root_structure.is_top_level)
		self.assertTrue(self.root_array.is_top_level)
		self.assertFalse(self.nested_structure.is_top_level)
		# TODO Array nested in array
		# TODO Struct nested in array

	def test_is_array_element(self):
		self.assertFalse(self.root_array.is_array_element)
		self.assertTrue(self.root_array[0].is_array_element)
		self.assertFalse(self.root_structure.is_array_element)
		self.assertFalse(self.nested_structure.is_array_element)

	def test_parent_address(self):
		self.assertIsNone(self.root_array.parent_address)
		self.assertIsNone(self.root_structure.parent_address)
		self.assertIsNotNone(self.nested_structure.parent_address)
		self.assertEqual(self.nested_structure.parent_address, "exif:Flash")
		self.assertEqual(self.root_array[0].parent_address, "exif:ISOSpeedRatings")

	def test_element_parent(self):
		self.assertIsNone(self.exif_ns.parent)
		self.assertIsInstance(self.root_structure.parent, XMPNamespace)
		self.assertIsInstance(self.root_array.parent, XMPNamespace)
		self.assertIsInstance(self.nested_structure.parent, XMPStructure)
		self.assertEqual(self.nested_structure.parent.name, "exif:Flash")
		self.assertIsInstance(self.nested_structure.parent.parent, XMPNamespace)

class XMPArrayTests(XMPTestCase):
	def setUp(self):
		super(XMPArrayTests, self).setUp()
		self.exif = self.example_xmp[libxmp.consts.XMP_NS_EXIF]
		self.iso_array = self.exif.ISOSpeedRatings
		self.components_array = self.exif.ComponentsConfiguration

	def test_len(self):
		self.assertEqual(len(self.iso_array), 1)
		self.assertEqual(len(self.components_array), 4)

	def test_getitem(self):
		self.assertEqual(self.iso_array[0].value, "400")

	def test_getitem_slices(self):
		self.assertEqual(self.iso_array[-1].value, "400")
		self.assertEqual(self.components_array[-1].value, "0")
		self.assertEqual([e.value for e in self.iso_array[:]], ["400"])
		self.assertEqual([e.value for e in self.components_array[:]], ["1", "2", "3", "0"])
		self.assertEqual([e.value for e in self.components_array[:-1]], ["1", "2", "3"])
		self.assertEqual([e.value for e in self.components_array[::2]], ["1", "3"])
		self.assertEqual([e.value for e in self.components_array[-3:-1]], ["2","3"])

class XMPStructureTests(XMPTestCase):
	def setUp(self):
		super(XMPStructureTests, self).setUp()
		self.exif_ns = self.example_xmp[libxmp.consts.XMP_NS_EXIF]
		self.tiff_metadata = self.example_xmp[libxmp.consts.XMP_NS_TIFF]

	def test_contains(self):
		self.assertTrue( "FNumber"  in self.exif_ns)
		self.assertFalse("FNumbers" in self.exif_ns)
		self.assertTrue( "ResolutionUnit"  in self.tiff_metadata)
		self.assertFalse("ResolutionUnits" in self.tiff_metadata)

	def test_has(self):
		self.assertTrue( self.exif_ns.has("FNumber"))
		self.assertFalse(self.exif_ns.has("FNumbers"))

		self.assertTrue( self.tiff_metadata.has("ResolutionUnit"))
		self.assertFalse(self.tiff_metadata.has("ResolutionUnits"))

	def test_getitem(self):
		self.assertEqual("32/10", self.exif_ns["FNumber"].value)
		with self.assertRaises(KeyError):
			self.exif_ns["inexistent_element"]

	def test_get(self):
		# Existing attribute
		self.assertIsInstance(self.exif_ns.get("FNumber"), XMPValue)
		self.assertEqual(self.exif_ns.get("FNumber").value, "32/10")
		# Non-existing attribute
		self.assertIsNone(self.exif_ns.get("inexistent_element"))

	def test_attribute_descriptor_get(self):
		self.assertEqual("32/10", self.exif_ns.FNumber.value)

	def test_getattr(self):
		# Existing attribute
		self.assertIsInstance(self.exif_ns.FNumber, XMPValue)
		self.assertEqual(self.exif_ns.FNumber.value, "32/10")
		# Non-existing attribute
		self.assertIsInstance(self.exif_ns.inexistent_element, XMPVirtualElement)
		# Nested attribute
		self.assertIsInstance(self.exif_ns.Flash, XMPStructure)
		self.assertIsInstance(self.exif_ns.Flash.RedEyeMode, XMPValue)
		self.assertEqual(self.exif_ns.Flash.RedEyeMode.value, "False")

	def test_setattr_existing(self):
		jpg_filepath = fixtures.sandboxedData(fixtures.JPG_PHOTO)

		with XMPFile(jpg_filepath, rw=True) as xmp_file:
			xmp_file.metadata[libxmp.consts.XMP_NS_EXIF].FNumber = "314/141"
			self.assertEqual(xmp_file.metadata[libxmp.consts.XMP_NS_EXIF].FNumber.value, "314/141")

		with XMPFile(jpg_filepath) as xmp_file:
			# libxmp doesn't allow persistence of standard namespaces such as EXIF
			self.assertEqual(xmp_file.metadata[libxmp.consts.XMP_NS_EXIF].FNumber.value, "32/10")

	def test_setattr_inexistent(self):
		sandboxed_photo = fixtures.sandboxedData(fixtures.JPG_PHOTO)
		with XMPFile(sandboxed_photo, rw=True) as xmp_file:
			xmp_file.metadata[TEST_NS].inexistent_element = 12
			self.assertIsInstance(xmp_file.metadata[TEST_NS].inexistent_element,
			                      XMPValue)
			self.assertEqual(xmp_file.metadata[TEST_NS].inexistent_element.value, "12")
		# Close and write file then reopen it
		with XMPFile(sandboxed_photo) as xmp_file:
			self.assertIsInstance(xmp_file.metadata[TEST_NS].inexistent_element,
			                      XMPValue)
			self.assertEqual(xmp_file.metadata[TEST_NS].inexistent_element.value, "12")

	def test_setattr_nested_inexistent(self):
		metadata = XMPMetadata()
		metadata[TEST_NS].A.B = 12

		self.assertIsInstance(metadata[TEST_NS].A,   XMPStructure)
		self.assertIsInstance(metadata[TEST_NS].A.B, XMPValue)
		self.assertEqual(metadata[TEST_NS].A.B.value, "12")

	def test_setattr_array_in_struct(self):
		metadata = XMPMetadata()
		metadata[TEST_NS].container.nested_array = [3.14, u"π"]

		tested_array = metadata[TEST_NS].container.nested_array
		self.assertIsInstance(metadata[TEST_NS].container, XMPStructure)
		self.assertEqual(len(metadata[TEST_NS].container), 1)
		self.assertIsInstance(tested_array, XMPArray)
		self.assertEqual(len(tested_array), 2)
		self.assertEqual(tested_array.value, ["3.14", u"π"])

	def test_setattr_nested_struct_from_dict(self):
		metadata = XMPMetadata()
		metadata[TEST_NS].test_struct = { "a": 1,
		                                  "b": 2,
		                                  "c": { "x": 3,
		                                         "y": 4,
		                                         "z": 5 } }

		test_struct = metadata[TEST_NS].test_struct

		self.assertIsInstance(test_struct, XMPStructure)
		self.assertIsInstance(test_struct.a, XMPValue)
		self.assertIsInstance(test_struct.b, XMPValue)
		self.assertIsInstance(test_struct.c, XMPStructure)

		self.assertEqual(len(test_struct), 3)
		self.assertEqual(len(test_struct.c), 3)

		self.assertEqual(test_struct.a.value, "1")
		self.assertEqual(test_struct.b.value, "2")
		self.assertEqual(test_struct.c.x.value, "3")
		self.assertEqual(test_struct.c.y.value, "4")
		self.assertDictEqual(test_struct.value, { "test:a": "1",
		                                          "test:b": "2",
		                                          "test:c": { "test:x": "3",
		                                                      "test:y": "4",
		                                                      "test:z": "5" } })

	def test_delitem(self):
		metadata = XMPMetadata()
		metadata[TEST_NS]["element"] = {"a": 1}
		self.assertIsInstance(metadata[TEST_NS].element, XMPStructure)
		del metadata[TEST_NS]["element"]
		self.assertIsNone(metadata[TEST_NS].get("element"))

class XMPArrayTests(XMPTestCase):
	def test_setattr_top_level_array(self):
		metadata = XMPMetadata()
		metadata[TEST_NS].top_level_array = [1,2,3,"a","b","c"]

		self.assertIsInstance(metadata[TEST_NS].top_level_array, XMPArray)
		self.assertIsInstance(metadata[TEST_NS].top_level_array.value, list)
		self.assertListEqual(metadata[TEST_NS].top_level_array.value,
		                     ["1","2","3","a","b","c"])

	def test_array_expand(self):
		metadata = XMPMetadata()
		metadata[TEST_NS].top_level_array = [1,2]

		self.assertEqual(len(metadata[TEST_NS].top_level_array), 2)
		self.assertListEqual(metadata[TEST_NS].top_level_array.value, ["1","2"])

		metadata[TEST_NS].top_level_array = [3,4,5,6]
		self.assertEqual(len(metadata[TEST_NS].top_level_array), 4)
		self.assertListEqual(metadata[TEST_NS].top_level_array.value, ["3","4","5","6"])

	def test_array_shrink(self):
		metadata = XMPMetadata()
		metadata[TEST_NS].top_level_array = [3,4,5,6]

		self.assertEqual(len(metadata[TEST_NS].top_level_array), 4)
		self.assertListEqual(metadata[TEST_NS].top_level_array.value, ["3","4","5","6"])

		metadata[TEST_NS].top_level_array = [1,2]
		self.assertEqual(len(metadata[TEST_NS].top_level_array), 2)
		self.assertListEqual(metadata[TEST_NS].top_level_array.value, ["1","2"])

	def test_array_insert(self):
		metadata = XMPMetadata()
		metadata[TEST_NS].test_array = [0,2,3]

		self.assertListEqual(metadata[TEST_NS].test_array.value, ["0","2","3"])
		metadata[TEST_NS].test_array.insert(1, 1)
		self.assertListEqual(metadata[TEST_NS].test_array.value, ["0","1","2","3"])

	def test_setattr_array_in_array(self):
		metadata = XMPMetadata()
		metadata[TEST_NS].top_level_array = [1,[2,3,4],5]

		created_array = metadata[TEST_NS].top_level_array
		self.assertIsInstance(created_array, XMPArray)
		self.assertEqual(len(created_array), 3)
		self.assertIsInstance(created_array.value, list)
		self.assertIsInstance(created_array[1], XMPArray)
		self.assertEqual(len(created_array[1]), 3)
		self.assertIsInstance(created_array.value, list)
		self.assertEqual(created_array.value, ["1", ["2","3","4"], "5"])
		self.assertEqual(created_array[1].value, ["2","3","4"])

	def test_setattr_struct_in_array(self):
		metadata = XMPMetadata()
		metadata[TEST_NS].root_array[2].nested_structure = 12

		root_array = metadata[TEST_NS].root_array

		self.assertIsInstance(root_array, XMPArray)
		self.assertEqual(len(root_array), 3)
		self.assertIsInstance(root_array[0], XMPValue)
		self.assertIsNone(root_array[0].value)
		self.assertIsInstance(root_array[1], XMPValue)
		self.assertIsNone(root_array[1].value)
		self.assertIsInstance(root_array[2], XMPStructure)
		self.assertEqual(len(root_array[2]), 1)
		self.assertEqual(root_array[2].value, {"test:nested_structure": "12"})
		self.assertIsInstance(root_array[2].nested_structure, XMPValue)
		self.assertEqual(root_array[2].nested_structure.value, "12")

	def test_array_delitem(self):
		metadata = XMPMetadata()
		metadata[TEST_NS].test_array = range(12)
		self.assertListEqual(metadata[TEST_NS].test_array.value,
		                     [str(x) for x in range(12)])
		del metadata[TEST_NS].test_array[6:]
		self.assertListEqual(metadata[TEST_NS].test_array.value,
		                     [str(x) for x in range(6)])
		del metadata[TEST_NS].test_array[::2]
		self.assertListEqual(metadata[TEST_NS].test_array.value,
		                     [str(x) for x in range(6)[1::2]])
		del metadata[TEST_NS].test_array[:]
		self.assertListEqual(metadata[TEST_NS].test_array.value, [])

class XMPSetTests(XMPTestCase):
	def test_setattr_set(self):
		metadata = XMPMetadata()
		test_metadata = metadata[TEST_NS]
		test_metadata.root_set = {3, 1, 4}

		self.assertIsInstance(test_metadata.root_set, XMPSet)
		self.assertEqual(len(test_metadata.root_set), 3)
		self.assertSetEqual(test_metadata.root_set.value, {"3", "1", "4"})

	def test_contains(self):
		metadata = XMPMetadata()
		test_metadata = metadata[TEST_NS]
		test_metadata.root_set = {3, 1, 4}

		self.assertTrue(3 in test_metadata.root_set)
		self.assertTrue(1 in test_metadata.root_set)
		self.assertTrue(4 in test_metadata.root_set)

		self.assertFalse(2 in test_metadata.root_set)
		for i in range(5,20):
			self.assertFalse(i in test_metadata.root_set)

class XMPNamespaceTests(XMPTestCase):
	def test_update_namespace(self):
		metadata = XMPMetadata()
		test_metadata = metadata[TEST_NS]
		test_metadata.update({"a": 12,
		                           "b": [1,2]})

		self.assertEqual(len(test_metadata), 2)
		self.assertIsInstance(test_metadata.a, XMPValue)
		self.assertEqual(test_metadata.a.value, "12")
		self.assertIsInstance(test_metadata.b, XMPArray)
		self.assertEqual(len(test_metadata.b), 2)
		self.assertListEqual(test_metadata.b.value, ["1","2"])

	def test_namespace_unregistered(self):
		TEST_NS_2 = u"http://test.com/xmp/test/2"
		PREFIX_2 = "test2"

		metadata = XMPMetadata()
		test_metadata = metadata[TEST_NS_2]
		with self.assertRaises(NameError):
			test_metadata["test_key"]=0

		registerNamespace(TEST_NS_2, "test2")
		assert(test_metadata.prefix == PREFIX_2)
		try:
			test_metadata["test_key"]=0
		except Exception, e:
			assert(False)
			pass

class XMPVirtualElementTests(XMPTestCase):
	def setUp(self):
		super(XMPVirtualElementTests, self).setUp()
		self.exif_ns = self.example_xmp[libxmp.consts.XMP_NS_EXIF]

	def test_getattr(self):
		self.assertIsInstance(self.exif_ns.inexistent_element.nested_inexistent_element,
		                      XMPVirtualElement)
		self.assertIsInstance(self.exif_ns.inexistent_element[2], XMPVirtualElement)
		self.assertEqual(self.exif_ns.inexistent_element[2].address,
		                 "%s[2]" % self.exif_ns.inexistent_element.address)

	def test_parent(self):
		self.assertIsInstance(self.exif_ns.virtual_element.parent, XMPNamespace)
		self.assertIsInstance(self.exif_ns.virtual_element.nested_virtual_element.parent,
		                      XMPVirtualElement)

class ComplexTests(XMPTestCase):
	def test_setattr_complex(self):
		metadata = XMPMetadata()
		test_metadata = metadata[TEST_NS]

		test_metadata.root_value = 12

class Metadata(unittest.TestCase):
	def setUp(self):
		self.xmp_file = XMPFile(fixtures.sandboxedData(fixtures.JPG_PHOTO))
		self.xmp_file.open()
		self.xmp_metadata = self.xmp_file.metadata[TEST_NS]

	def tearDown(self):
		self.xmp_file.close()

	def test_virtual_element(self):
		self.xmp_metadata.inexistent_attribute

	def test_nested_virtual_element(self):
		self.xmp_metadata.inexistent_attribute.nested_inexistent_attribute

	def test_virtual_element_descriptor_get(self):
		self.assertIsInstance(self.xmp_metadata.inexistent_attribute, XMPVirtualElement)
		self.assertIsInstance(self.xmp_metadata.__dict__, dict)

	def test_virtual_element_descriptor_set_readonly(self):
		self.xmp_metadata.inexistent_attribute = 12
		import warnings
		with warnings.catch_warnings(record=True) as w:
			warnings.simplefilter("always")
			self.xmp_file.close()
			self.assertEqual(len(w), 1)
			self.assertEqual(w[-1].category, RuntimeWarning)

		self.xmp_file.open()

	def test_virtual_element_descriptor_set(self):
		with XMPFile(fixtures.sandboxedData(fixtures.JPG_PHOTO), rw = True) as xmpitem:
			xmpitem.metadata[TEST_NS].inexistent_attribute = 12
			self.assertIsInstance(xmpitem.metadata[TEST_NS].inexistent_attribute, XMPValue)
			self.assertEqual(xmpitem.metadata[TEST_NS].inexistent_attribute.value, "12")

	def test_virtual_element_descriptor_delete(self):
		with self.assertRaises(TypeError):
			del self.xmp_metadata.inexistent_attribute

class SidecarTests(unittest.TestCase):
	def setUp(self):
		self.sidecar_only_path = fixtures.sandboxedData("foobar.txt")
		self.sidecar_path = self.sidecar_only_path + ".xmp"
		if os.path.exists(self.sidecar_path):
			os.remove(self.sidecar_path)

	def test_sidecar_creation(self):
		with XMPFile(self.sidecar_only_path, rw=True) as sidecar:
			sidecar.metadata[TEST_NS].structure = "value"
		self.assertTrue(os.path.exists(self.sidecar_only_path))
		with XMPFile(self.sidecar_only_path, rw=True) as sidecar:
			self.assertEqual(sidecar.metadata[TEST_NS].structure.value, "value")
