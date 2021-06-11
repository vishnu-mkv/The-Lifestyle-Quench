# The Lifestyle Quench

a blog application with django backend and angular frontend.

completely restful.

Server:
- Custom user model
- Create posts with html content. Image url should reference to a image in server. Checked by server on create and update and populated dynamically on request to support migrations.
- Writer applictaions and Post submissions

To cleanup un-referenced images in server
run `python manage.py clean-images`
see settings.py for configuration

//Server pretty much completed
