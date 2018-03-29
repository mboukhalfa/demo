from rest_framework import serializers

from upload.models import Video

class UploadUUIDSerializer(serializers.ModelSerializer):

	class Meta():
		model = Video
		fields = [
			"pk",
			"name",
			"timestamp",
			"uploade",
			"uuid",

		]
		read_only_fields = ("pk","name","timestamp","uuid")
