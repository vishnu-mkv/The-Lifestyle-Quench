# Curiosity

A blog application with Django REST.

You can visit the hosted server homepage at [Curiosity - Home](https://curio-sity.herokuapp.com)

Features:

-   Custom user model. Log in using email.
-   Activate account, recover account using email.
-   AWS S3 for serving media files.
-   Create posts with html content. Javascript is removed if found in writer uploaded post.
-   Image url should reference to a image in server. Checked by server on create and update and populated dynamically on request to support serving from AWS.
-   Writer applictaions and Post submissions.
-   Writers can use the integrated Quill WYSIWYG editor to write posts.
-   Editor supports alignment, change font color, change font size change, hyperlinks and image uploads. More editing options can be added.
-   Mobile friendly WYSIWYG editor. Writers can work on their mobile too.
-   Save a post as a draft. Submit post and will be published if approved.

To clean up un-referenced images in server
run `python manage.py clean-images`. Deletes un-referenced model objects of image models which will be followed up by deletion of images by django-cleanup.

Use `python manage.py generate-default` to generate default image model objects.

see settings.py for configuration
