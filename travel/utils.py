
class AbsoluteImageUrlMixin:
    def get_imge(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None