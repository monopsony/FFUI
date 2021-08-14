from collections import defaultdict
import logging

logger = logging.getLogger(__name__)
subs = defaultdict(list)


class EventClass:
    def __init__(self):
        super().__init__()
        self.eventQueue = []

    # this is meant ot be seen during the event loop, not immediately
    # so that it runs in a separate thread

    def eventSubscribe(self, event, func):
        subs[event].append((self, func))

    def eventPush(self, event, *args, quiet=False):
        if not quiet:
            logger.debug(f"Event pushed: {event} by {type(self)}")
        for obj, func in subs[event]:
            obj.eventQueue.append((func, args))

    eventBusy = None
    eventFree = None
    busy = False

    def eventHandle(self):
        if len(self.eventQueue) < 1:
            return

        self.busy = True
        if self.eventBusy is not None:
            self.eventPush(self.eventBusy)

        for func, args in self.eventQueue:
            func(*args)

        self.busy = False
        if self.eventFree is not None:
            self.eventPush(self.eventFree)

        self.eventQueue.clear()


class EventWidgetClass:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def eventSubscribe(self, *args):
        self.launcher.eventSubscribe(*args)

    def eventPush(self, *args, **kwargs):
        self.launcher.eventPush(*args, **kwargs)
