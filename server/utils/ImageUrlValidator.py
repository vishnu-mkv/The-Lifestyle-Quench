from rest_framework import serializers

def build_image_url(request, image):
    return request.build_absolute_uri(image.image.url)


def validate_image_url(url, Model, request, default=True):
    if not url:
        return serializers.ValidationError("Invalid url")

    directory = Model._meta.get_field('image').upload_to
    url = url[:url.find('?')]
    image_name = url.split('/')[-1]

    if default:
        if url == build_image_url(request, Model.objects.get(image='default.jpg')):
            return Model.objects.get(image='default.jpg')

    try:
        image = Model.objects.get(image=f'{directory}/{image_name}')
        if url != build_image_url(request, image).split('?')[0]:
            raise serializers.ValidationError("Invalid uri.")
        return image
    except Model.DoesNotExist:
        raise serializers.ValidationError("Invalid url")
