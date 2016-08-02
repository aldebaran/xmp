# -*- coding: utf-8 -*-

"""
    ``XMP`` module
    ==============

    This module wraps Adobe's libxmp package, providing an easier API.

    Reading metadata
    ----------------

    Importing `XMPFile` is enough to fulfill almost all of use cases.

    :Example:

    >>> from xmp.xmp import XMPFile
    >>> myFile = XMPFile("path/to/file")
    >>> myFile.open()
    >>> len(myFile.libxmp_metadata.namespaces) # Number of available namespaces
    4
    >>> for ns in myFile.metadata.namespaces:
    ...     print ns.uid
    ...
    http://ns.adobe.com/exif/1.0/
    http://ns.adobe.com/tiff/1.0/
    http://ns.adobe.com/xap/1.0/
    http://ns.adobe.com/photoshop/1.0/
    >>> myFile.metadata["http://ns.adobe.com/exif/1.0/"].value
    OrderedDict([(u'exif:ColorSpace', u'1'), (u'exif:CompressedBitsPerPixel', u'4/1'),\
        (u'exif:PixelXDimension', u'3968'), (u'exif:PixelYDimension', u'2232'),\
        (u'exif:ExposureTime', u'10/60'), (u'exif:FNumber', u'32/10'),\
        (u'exif:ExposureProgram', u'3'), (u'exif:ExposureBiasValue', u'-133/100'),\
        (u'exif:MaxApertureValue', u'237/128'), (u'exif:MeteringMode', u'5'),\
        (u'exif:LightSource', u'0'), (u'exif:FocalLength', u'98/10'),\
        (u'exif:SensingMethod', u'2'), (u'exif:CustomRendered', u'0'),\
        (u'exif:ExposureMode', u'0'), (u'exif:WhiteBalance', u'0'),\
        (u'exif:DigitalZoomRatio', u'0/10'), (u'exif:FocalLengthIn35mmFilm', u'50'),\
        (u'exif:SceneCaptureType', u'0'), (u'exif:GainControl', u'2'),\
        (u'exif:Contrast', u'0'), (u'exif:Saturation', u'0'), (u'exif:Sharpness', u'0'),\
        (u'exif:DateTimeOriginal', u'2016-03-25T21:40:20'), (u'exif:ISOSpeedRatings', [u'400']),\
        (u'exif:ExifVersion', u'0230'), (u'exif:FlashpixVersion', u'0100'),\
        (u'exif:ComponentsConfiguration', [u'1', u'2', u'3', u'0']),\
        (u'exif:Flash', OrderedDict([(u'exif:Fired', u'False'), (u'exif:Return', u'0'),\
        (u'exif:Mode', u'2'), (u'exif:Function', u'False'), (u'exif:RedEyeMode', u'False')])),\
        (u'exif:FileSource', u'3'), (u'exif:SceneType', u'1')])


    Calling `.value` on a XMPNamespace will return an OrderedDict containing all the elements in the namespace.
    If you know the key of the value you are looking for, you can directly call it.

    :Example:

    >>> myFile.metadata["http://ns.adobe.com/exif/1.0/"]["exif:ColorSpace"].value
    u'1'

    ..note:: If your namespace is registered (see `Creating a namespace`), you can directly query the parameter
    without the prefix (see `Creating a namespace` for details about what a prefix is). When opening a file, its
    namespaces are automatically registered upon reading.

    :Example:

    >>> myFile.metadata["http://ns.adobe.com/exif/1.0/"]["ColorSpace"].value
    u'1'

    If you don't know the items and want to print the available keys, you can iterate on the OrderedDict.

    :Example:

    >>> for i in myFile.metadata["http://ns.adobe.com/exif/1.0/"]:
    ...     print i.address
    ...
    exif:ColorSpace
    exif:CompressedBitsPerPixel
    exif:PixelXDimension
    exif:PixelYDimension
    exif:ExposureTime
    exif:FNumber
    exif:ExposureProgram
    exif:ExposureBiasValue
    exif:MaxApertureValue
    exif:MeteringMode
    exif:LightSource
    exif:FocalLength
    exif:SensingMethod
    exif:CustomRendered
    exif:ExposureMode
    exif:WhiteBalance
    exif:DigitalZoomRatio
    exif:FocalLengthIn35mmFilm
    exif:SceneCaptureType
    exif:GainControl
    exif:Contrast
    exif:Saturation
    exif:Sharpness
    exif:DateTimeOriginal
    exif:ISOSpeedRatings
    exif:ExifVersion
    exif:FlashpixVersion
    exif:ComponentsConfiguration
    exif:Flash
    exif:FileSource
    exif:SceneType

    Don't forget to close the file when finished. You can also use the `with` statement.

    :Example:

    >>> myFile.open()
    >>> for ns in myFile.metadata.namespaces:
    ...     print ns.uid
    http://ns.adobe.com/exif/1.0/
    http://ns.adobe.com/tiff/1.0/
    http://ns.adobe.com/xap/1.0/
    http://ns.adobe.com/photoshop/1.0/
    >>> myFile.close()
    >>> myFile.is_open
    False

    >>> with myFile as _:
    ...     for ns in myFile.metadata.namespaces:
    ...             print ns.uid
    ...
    http://ns.adobe.com/exif/1.0/
    http://ns.adobe.com/tiff/1.0/
    http://ns.adobe.com/xap/1.0/
    http://ns.adobe.com/photoshop/1.0/

    >>> myFile.is_open
    False


    Updating metadata
    -----------------

    Importing `XMPFile` is enough to fulfill almost all of use cases. To update, you must open
    the file in rw mode.

    ..note::

    All your changes are written only when the file is closed.

    :Example:

    >>> from xmp.xmp import XMPFile
    >>> myFile = XMPFile("path/to/file", rw=True)
    >>> myFile.open()
    >>> myFile.metadata["http://ns.adobe.com/exif/1.0/"]["ColorSpace"]=2
    >>> myFile.metadata["http://ns.adobe.com/exif/1.0/"]["exif:ColorSpace"].value
    u'2'

    You can also add a new field in an existing namespace, or delete one. When creating a new key, you
    should avoid using ":" in it (see `Creating a namespace` section).

    :Example:

    >>> myFile.metadata["http://ns.adobe.com/exif/1.0/"]["myNewField"]=2
    >>> myFile.metadata["http://ns.adobe.com/exif/1.0/"]["myNewField"].value
    u'2'
    >>> del myFile.metadata["http://ns.adobe.com/exif/1.0/"]["myNewField"]
    >>> myFile.metadata["http://ns.adobe.com/exif/1.0/"]["myNewField"].value
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "xmp/xmp.py", line 1019, in __getitem__
        raise KeyError(qualified_field_name)
    KeyError: 'exif:myNewField'

    This works for any existing namespace. To write metadata in a new namespace, you must first create
    that namespace.


    Creating a new namespace
    ------------------------

    In libxmp, a namespace is bound to a prefix. There can be only one prefix per namespace, and only
    one namespace per prefix. This prefix is added to your field names to make them "qualified". This is
    also a way for you to remember in which namespace a value is, just from its qualifier name.

    For instance, and as you saw before, the prefix for "http://ns.adobe.com/exif/1.0/" namespace is "exif".

    :Example:

    >>> myFile.metadata["http://ns.adobe.com/exif/1.0/"]["myNewField"]=2
    >>> myFile.metadata["http://ns.adobe.com/exif/1.0/"]["myNewField"].address
    'exif:myNewField'

    The qualified version of "myNewField" is "exif:myNewField". And your data is accessible using both
    the qualified and the unqualified name.

    ..warning::

    A qualifier is "qualified" if it follows the form "prefix:key". Because of this, you should never use ":"
    in your keys, otherwise libxmp will consider the first part as a different prefix than the default
    namespace's one, which is not allowed.

    When using a new namespace, you therefore need first to register its default prefix. Not doing so will lead to
    errors when trying to set values in the namespace.

    :Example:

    >>> ns=myFile.metadata["http://test.com/xmp/1"]
    >>> ns.prefix is None
    True
    >>> ns["test:myField"]=0
    Unregistered schema namespace URI
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "xmp/xmp.py", line 1027, in __setitem__
        self.set(key, value)
      File "xmp/xmp.py", line 930, in set
        new_element._create(value)
      File "xmp/xmp.py", line 1574, in _create
        self.update(value)
      File "xmp/xmp.py", line 1596, in update
        prop_value = value)
      File "build/bdist.linux-x86_64/egg/libxmp/core.py", line 248, in set_property
      File "build/bdist.linux-x86_64/egg/libxmp/exempi.py", line 1422, in set_property
      File "build/bdist.linux-x86_64/egg/libxmp/exempi.py", line 1702, in check_error
    libxmp.XMPError: Exempi function failure ("bad schema").

    To register a namespace, you need to use the `registerNamespace` function. You can then set values
    using both qualified and unqualified names. However, you must use the proper prefix if you use a
    qualified name.

    :Example:

    >>> from xmp.xmp import registerNamespace
    >>> registerNamespace("http://test.com/xmp/1", "test")
    u'test'
    >>> ns.prefix
    u'test'
    >>> ns["test:myField"]=0
    >>> ns["myField2"]=0
    >>> ns["test:myField"].value
    u'0'
    >>> ns["myField2"].value
    u'0'
    >>> ns["otherPrefix:myField"]=0
    Schema namespace URI and prefix mismatch
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "xmp/xmp.py", line 1027, in __setitem__
        self.set(key, value)
      File "xmp/xmp.py", line 930, in set
        new_element._create(value)
      File "xmp/xmp.py", line 1574, in _create
        self.update(value)
      File "xmp/xmp.py", line 1596, in update
        prop_value = value)
      File "build/bdist.linux-x86_64/egg/libxmp/core.py", line 248, in set_property
      File "build/bdist.linux-x86_64/egg/libxmp/exempi.py", line 1422, in set_property
      File "build/bdist.linux-x86_64/egg/libxmp/exempi.py", line 1702, in check_error
    libxmp.XMPError: Exempi function failure ("bad schema").


    ..warning::

    Registered namespaces are stored in a global map that is only cleared when the session is over. It is
    automatically updated when a file with unknown namespaces is loaded, and once a namespace is entered, its
    prefix CANNOT be changed without closing the python script and starting over. Be very careful when selecting
    a prefix for a namespace, as it should always be the same across different files (otherwise you may have
    trouble when successively opening different files), and as changing a prefix afterwards without changing the
    namespace is not such an easy operation.

    :Example:

    >>> from xmp.xmp import registerNamespace
    >>> registerNamespace("http://test.com/xmp/1", "foo")
    u'foo'
    >>> registerNamespace("http://test.com/xmp/1", "bar") # this will not change the prefix
    u'foo'

"""
import os, glob

# ––––––––––––––––––
# Export all modules

__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/*.py")]

try: del f # Cleanup the iteration variable so that it's not exported
except: pass

# ––––––––––––––––––––––––––––
# Convenience version variable

VERSION = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "VERSION")).read().split()[0]

# ––––––––––––––––––––
# Hook for qiq plugins

QIQ_PLUGIN_PACKAGES = ["qiq"]

#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––#
