class Engine:
    pass

from abc import ABC, abstractmethod


class ObservableEngine(Engine):
    def __init__(self):
        self.subscribers=set()

    def subscribe(self,subscriber):
        self.subscribers.add(subscriber)

    def unsubscribe(self,subscriber):
        self.subscribers.remove(subscriber)

    def notify(self,msg):
        for subscriber in self.subscribers:
            subscriber.update(msg)


class AbstractObserver(ABC):

    @abstractmethod
    def update(self, data):
        pass


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements=set()

    def update(self,data):
        self.achievements.add(data['title'])

class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements=list()
    def update(self,data):
        f=False
        for i in self.achievements:
            f=f or (i==data['title'])
        if not f:
            self.achievements.append(data['title'])




a = ObservableEngine()
b = ShortNotificationPrinter()
c=FullNotificationPrinter()
a.subscribe(b)
a.subscribe(c)
a.notify({"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"})
a.notify({"title": "Покоритель", "text": "Дается при выполнении всех заданий в игре"})
print(b.achievements,c.achievements)