from django.conf import settings
import magic

'''
<QueryDict: {'file.path': ['/tmp/0000000015'], 'file.name': ['video.mp4'], 'uuid': ['6e550925-6767-4120-b245-5d92e30542e2'], 'file.size': ['0'], 'file.content_type': ['video/mp4'], 'file.md5': ['d41d8cd98f00b204e9800998ecf8427e']}>
'''
class VideoValidator():
	ext = settings.UPLOAD_VIDEO_EXT
	mime_type = settings.UPLOAD_VIDEO_MIMETYPE
	path=''
	name=''
	size=''
	content_type=''
	def __init__(self,data):
		self.path = data['file.path']
		self.name = data['file.name']
		self.size = data['file.size']
		self.content_type = data['file.content_type']
		print(data)

	def is_valid(self):
		mime = magic.Magic(mime=True)
		self.video_mime = mime.from_file(self.path)
		print(self.video_mime)
		if self.video_mime in self.mime_type:
			return True
		return False