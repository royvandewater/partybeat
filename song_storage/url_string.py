class UrlString:
    def __init__(self, string):
        self.string = string
        self.url_safe = string.replace(" ", "_")

    def __str__(self):
        return self.string
