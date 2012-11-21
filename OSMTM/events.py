class EventHook(object):

    def __init__(self):
        print "#######"
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        print self .__handlers
        return self

    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    def fire(self, *args, **keywargs):
        for handler in self.__handlers:
            handler(*args, **keywargs)

    def clearObjectHandlers(self, inObject):
        for theHandler in self.__handlers:
            if theHandler.im_self == inObject:
                self -= theHandler

class Broadcaster():
    def __init__(self):
        self.onChange = EventHook()

myBroadcaster = Broadcaster()
