import webbrowser

from flox import Flox, utils, clipboard, ICON_BROWSER, ICON_COPY, ICON_APP_ERROR
import bttv

class TwitchEmotes(Flox):

    def query(self, query):
        if len(query) >= bttv.MIN_QUERY_LEN:
            emotes = bttv.search_emotes(query)
            for emote in emotes:
                self.items(emote)
        elif len(query) == 0:
            emotes = bttv.top_emotes()
            for emote in emotes:
                self.items(emote['emote'])
        else:
            self.add_item(
                title="Invalid search!",
                subtitle="{} or more characters required.".format(bttv.MIN_QUERY_LEN),
                icon=ICON_APP_ERROR
            )

    def context_menu(self, data):
        self.add_item(
            title="Open in browser",
            subtitle="Open icon in web browser.",
            icon=ICON_BROWSER,
            method=self.open_in_browser,
            parameters=[bttv.get_img_url(data[0], '3x')],
        )
        self.add_item(
            title="Copy to clipboard",
            subtitle="Copy emote to clipboard.",
            icon=ICON_COPY,
            method=self.copy_to_clipboard,
            parameters=[bttv.get_img_url(data[0], '3x'), data[0]['code']],
        )

    def items(self, item):
        emote_owner = str(item['user']['name'])
        file_ext = item['imageType']
        self.add_item(
            title=item['code'],
            subtitle=f"Streamer: {emote_owner}",
            icon=utils.get_icon(bttv.get_img_url(item), self.name, file_name=f"{item['id']}.{file_ext}"),
            method=self.copy_to_clipboard,
            parameters=[bttv.get_img_url(item, '3x'), item['code']],
            context=[item]
        )

    def open_in_browser(self, url):
        webbrowser.open(url)

    def copy_to_clipboard(self, url, code):
        clipboard.put(url)
        self.show_msg("Copied to clipboard", f"Emote: {code}", url)

if __name__ == "__main__":
    TwitchEmotes()
