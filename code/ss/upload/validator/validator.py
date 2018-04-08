import magic


class VideoValidator:

    def __init__(self, data):
        self.path = data['file.path']
        self.name = data['file.name']
        self.size = data['file.size']
        self.content_type = data['file.content_type']
        self.video_mime = ''

    def is_valid(self):
        mime = magic.Magic(mime=True)
        self.video_mime = mime.from_file(self.path)
        if self.video_mime.startswith('video'):
            return True
        return False
