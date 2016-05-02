# -*- coding: utf-8 -*-

# Qt
from PySide.QtCore import Signal

# qidata
from ...models import makeDataItem
from ...view import makeWidget
from ..datacontroller import DataController
from qidata.annotationitems import *

class ImageController(DataController):

    # ───────
    # Signals

    selectionChanged = Signal((Person,), (Face,))

    # ───────────
    # Constructor

    def __init__(self, source_path):
        super(ImageController, self).__init__()
        DataController.modelHandler = makeDataItem(source_path)
        DataController.model = self.modelHandler.metadata
        DataController.widget = makeWidget(self.modelHandler)

        self.last_selected_item = None

        for annotationIndex in range(0,len(self.model)):
            r = self.widget.addRect(self.model[annotationIndex][1], annotationIndex)
            r.isSelected.connect(self.onItemSelected)

    # ─────
    # Slots

    def onItemSelected(self, item_selected):
        self.last_selected_item = item_selected
        self.selectionChanged.emit(self.model[item_selected][0])

    def onTypeChangeRequest(self, message_type):
        self.model[self.last_selected_item][0] = makeAnnotationItems(message_type)
        self.selectionChanged.emit(self.model[self.last_selected_item][0])
