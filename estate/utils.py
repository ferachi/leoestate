from django.utils.text import slugify



def upload_display_image_dir(instance, filename):
    title = instance.title
    slug = slugify(title)
    base, extension = filename.split('.')
    new_filename = "{0}.{1}".format(title, extension)
    return "places/images/%s/main/%s" % (slug, new_filename)


def upload_thumbnail_dir(instance, filename):
    title = instance.title
    slug = slugify(title)
    base, extension = filename.split('.')
    new_filename = "{0}.{1}".format(title, extension)
    return "places/images/%s/thumbnail/%s" % (slug, new_filename)


def upload_place_images_dir(instance, filename):
    title = instance.title
    place = instance.place.title
    slug = slugify(place)
    base, extension = filename.split('.')
    new_filename = "{0}.{1}".format(title, extension)
    return "places/images/%s/images/%s" % (slug, new_filename)