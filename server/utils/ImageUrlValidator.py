from rest_framework import serializers


def build_image_url(request, image):
    return request.build_absolute_uri(image.image.url)


def validate_image_url(url, Model, request, default=True):
    if not url:
        return url

    directory = Model._meta.get_field('image').upload_to
    image_name = url.split('/')[-1]

    if default:
        if url == build_image_url(request, Model.objects.get(image='default.jpg')):
            return url

    try:
        image = Model.objects.get(image=f'{directory}/{image_name}')
        if url != build_image_url(request, image):
            raise serializers.ValidationError("Invalid uri.")
        return image
    except Model.DoesNotExist:
        raise serializers.ValidationError("Invalid url")
