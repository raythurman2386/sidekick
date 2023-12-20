import markdown
import tkinterweb


class MarkdownTextArea(tkinterweb.HtmlFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.markdown_text = ""

    def insert(self, text):
        """Insert text, to be rendered as markdown"""
        self.markdown_text += text
        html = markdown.markdown(self.markdown_text)
        self.load_html(html)

    def get(self):
        """Get the current markdown text"""
        return self.markdown_text

    def clear(self):
        """Clear the text area"""
        self.markdown_text = ""
        self.load_html("")
