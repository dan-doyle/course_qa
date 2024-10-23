class CleanFile:
    def __init__(self, unclean_content):
        self.data = unclean_content
        self.cleaned_data = self.data

    def deduplicate(self):
        lines = self.cleaned_data.splitlines()
        unique_lines = list(dict.fromkeys(lines)) 
        self.cleaned_data = "\n".join(unique_lines)

    def remove_non_ascii(self):
        self.cleaned_data = ''.join(char for char in self.data if ord(char) < 128)

    def clean(self):
        self.deduplicate()
        self.remove_non_ascii()
        return self.cleaned_data