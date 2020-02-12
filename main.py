from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
import requests

#Proxies = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}


class Extension(Extension):

    def __init__(self):
        super(Extension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        query = event.get_argument() or str()
        if len(query.strip()) == 0:
            return RenderResultListAction([
                ExtensionResultItem(icon='images/icon.png',
                                    name='No input',
                                    on_enter=HideWindowAction())
            ])
        else:
            result = requests.get(
                "https://api.github.com/search/repositories?q=%s&sort=stars&page=1&order=desc&per_page=10" % query ).json()
            items = []
            for i in result["items"]:
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name=i["full_name"],
                                                 description=str(
                                                     i["description"]),
                                                 on_enter=OpenUrlAction(i["html_url"])))

            return RenderResultListAction(items)


if __name__ == '__main__':
    Extension().run()
