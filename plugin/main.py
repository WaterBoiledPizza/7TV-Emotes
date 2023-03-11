import webbrowser
from flox import Flox, utils, clipboard
import seventv

class SevenTVEmotes(Flox):

    def query(self, query):
        if len(query) >= seventv.MIN_QUERY_LEN:
            emotes = seventv.search_emotes(query)
            for emote in emotes:
                self.result(emote)
        elif len(query) == 0:
            cache = utils.cache(f'{self.name}_top_emotes.json', max_age=300)
            emotes = cache(seventv.trending_emotes)()
            for emote in emotes:
                self.result(emote)
        else:
            self.add_item(
                title="Invalid search!",
                subtitle="{} or more characters required.".format(seventv.MIN_QUERY_LEN),
                icon="./Images/app_error.png"
            )

    def context_menu(self, data):
        self.add_item(
            title="Open in browser",
            subtitle="Open emote page in web browser.",
            icon="./Images/Browser.png",
            method=self.open_in_browser,
            parameters=[seventv.get_emote_url(data[0])],
        )
        self.add_item(
            title="Copy to clipboard",
            subtitle="Copy image link to clipboard.",
            icon="./Images/copy.png",
            method=self.copy_to_clipboard,
            parameters=[seventv.get_img_url(data[0], '3x'), data[0]['name']],
        )

    def result(self, item):
        emote_owner = str(item['owner']['display_name'])
        file_ext = "gif" if seventv.isAnimated(item["id"]) else "png"
        self.add_item(
            title=item['name'],
            subtitle=f"User: {emote_owner}",
            icon=utils.get_icon(seventv.get_img_url(item), self.name, file_name=f"{item['id']}.{file_ext}"),
            method=self.copy_to_clipboard,
            parameters=[seventv.get_img_url(item, '3x'), item['name']],
            context=[item]
        )

    def open_in_browser(self, url):
        webbrowser.open(url)

    def copy_to_clipboard(self, url, name):
        clipboard.put(url)
        self.show_msg("Copied to clipboard", f"Emote: {name}", url)

if __name__ == "__main__":
    SevenTVEmotes()
