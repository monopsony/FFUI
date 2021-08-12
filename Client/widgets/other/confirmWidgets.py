from widgets.confirmWidget.confirmWidget import confirmWidget
import math


class itemCraftConfirmWidget(confirmWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.eventSubscribe("ITEMLIST_ITEM_SELECTED", self.setSelectedItem)
        self.eventSubscribe("CLIENT_FREE", self.applyVisibility)
        self.setText("Something something about crafting idk man")

        self.applyVisibility()

    selectedItem = None

    def setSelectedItem(self, item, *args):

        self.selectedItem = item
        self.applyVisibility()

    def checkVisibility(self):
        if self.selectedItem is None:
            return False

        client = self.launcher.client
        if not client.hasItemInfo(self.selectedItem):
            return True

        itemInfo = client.mbGetItemInfo(self.selectedItem)
        return math.isnan(itemInfo["craftPrice"])

    def onClick(self, *args):
        if self.selectedItem is None:
            return

        item = self.selectedItem
        self.eventPush("CLIENT_MBCRAFT_REQUEST", item)


class itemListingsConfirmWidget(confirmWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.eventSubscribe("ITEMLIST_ITEM_SELECTED", self.setSelectedItem)
        self.eventSubscribe("CLIENT_FREE", self.applyVisibility)
        self.setText("Something something about listings idk man")

        self.applyVisibility()

    selectedItem = None

    def setSelectedItem(self, item, *args):
        self.selectedItem = item
        self.applyVisibility()

    def checkVisibility(self):
        if self.selectedItem is None:
            return False
        client = self.launcher.client
        return not client.hasItemInfo(self.selectedItem)

    def onClick(self, *args):
        if self.selectedItem is None:
            return

        item = self.selectedItem
        self.eventPush("CLIENT_MBINFO_REQUEST", item)


class itemFlipConfirmWidget(confirmWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.eventSubscribe("ITEMLIST_ITEM_SELECTED", self.setSelectedItem)
        self.eventSubscribe("CLIENT_FREE", self.applyVisibility)
        self.setText("Something something about flipping idk man")

        self.applyVisibility()

    selectedItem = None

    def setSelectedItem(self, item, *args):

        self.selectedItem = item
        self.applyVisibility()

    def checkVisibility(self):
        if self.selectedItem is None:
            return False

        client = self.launcher.client
        return not client.hasItemInfo(self.selectedItem, allWorlds=True)

    def onClick(self, *args):
        if self.selectedItem is None:
            return

        item = self.selectedItem
        self.eventPush("CLIENT_MBFLIP_REQUEST", item)


class listListingsConfirmWidget(confirmWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.eventSubscribe("LISTSLIST_LIST_SELECTED", self.setSelectedList)
        self.eventSubscribe("CLIENT_FREE", self.applyVisibility)
        self.setText("Something something about listings idk man")

        self.applyVisibility()

    selectedList = None

    def setSelectedList(self, lst, *args):
        self.selectedList = lst
        self.applyVisibility()

    def checkVisibility(self):
        if self.selectedList is None:
            return False
        lst = self.selectedList
        itemInfo = lst["ItemInfoCache"]
        return itemInfo is None

    def onClick(self, *args):
        if self.selectedList is None:
            return

        lst = self.selectedList["ItemListCache"]
        self.eventPush("CLIENT_MBINFO_REQUEST", lst)


class listCraftConfirmWidget(confirmWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.eventSubscribe("LISTSLIST_LIST_SELECTED", self.setSelectedList)
        self.eventSubscribe("CLIENT_FREE", self.applyVisibility)
        self.setText("Something something about listings idk man")

        self.applyVisibility()

    selectedList = None

    def setSelectedList(self, lst, *args):
        self.selectedList = lst
        self.applyVisibility()

    def checkVisibility(self):
        if self.selectedList is None:
            return False
        lst = self.selectedList
        itemInfo = lst["ItemInfoCache"]
        if itemInfo is None:
            return True

        return itemInfo["craftPrice"].isna().values.any()

    def onClick(self, *args):
        if self.selectedList is None:
            return

        lst = self.selectedList["ItemListCache"]
        # print("ON CLICK STUFF")
        self.eventPush("CLIENT_MBCRAFT_REQUEST", lst)
