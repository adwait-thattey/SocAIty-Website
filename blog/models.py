from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os



# Create your models here.
class Vote(models.Model):
    upvoter = models.ForeignKey(to=User, on_delete=models.CASCADE)
    upvote_time = models.DateTimeField()


def validate_blog_file_extension(incoming_file):
    extension = os.path.splitext(incoming_file.name)[1]
    allowed_extensions = ['.md', '.html']
    if extension.lower() not in allowed_extensions:
        raise ValidationError("This file type is not allowed")


def get_blog_upload_path(instance, filename):
    return os.path.join("blogs", str(instance.id), filename)


class Blog(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    create_date = models.DateTimeField()
    upvotes = models.ManyToManyField(to=Vote, related_name="upvoted_blog")
    downvotes = models.ManyToManyField(to=Vote, related_name="downvoted_blog")
    main_file = models.FileField(verbose_name="Blog Content File", upload_to=get_blog_upload_path,
                                 validators=[validate_blog_file_extension])


# class BlogMeta(models.Model):
#     blog = models.OneToOneField(to=Blog, on_delete=models.CASCADE)
#
#
# def get_blog_video_upload_path(instance, filename):
#     return os.path.join("blogs", str(instance.blog.id), "videos", filename)
#
#
# def validate_blog_video_file_extension(incoming_file):
#     extension = os.path.splitext(incoming_file.name)[1]
#     allowed_extensions = ['.mp4', '.ogg', '.webm']
#     if extension.lower() not in allowed_extensions:
#         raise ValidationError("This file type is not allowed/supported")
#
#
# class BlogVideo(models.Model):
#     blog = models.ForeignKey(to=BlogMeta, on_delete=models.CASCADE)
#     video = models.FileField(upload_to=get_blog_video_upload_path, validators=[validate_blog_video_file_extension])
#
# def get_blog_audio_upload_path(instance, filename):
#     return os.path.join("blogs", str(instance.blog.id), "audios", filename)
#
#
# def validate_blog_audio_file_extension(incoming_file):
#     extension = os.path.splitext(incoming_file.name)[1]
#     allowed_extensions = ['.mp3', '.wav']
#     if extension.lower() not in allowed_extensions:
#         raise ValidationError("This file type is not allowed/supported")
#
#
# class BlogAudio(models.Model):
#     blog = models.ForeignKey(to=BlogMeta, on_delete=models.CASCADE)
#     audio = models.FileField(upload_to=get_blog_audio_upload_path, validators=[validate_blog_audio_file_extension])
#
#
# def get_blog_image_upload_path(instance, filename):
#     return os.path.join("blogs", str(instance.blog.id), "images", filename)
#
#
# class BlogImage(models.Model):
#     blog = models.ForeignKey(to=BlogMeta, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to=get_blog_image_upload_path)
#
# def get_blog_other_file_upload_path(instance, filename):
#     return os.path.join("blogs", str(instance.blog.id), "other_files", filename)
#
# class BlogFile(models.Model):
#     blog = models.ForeignKey(to=BlogMeta, on_delete=models.CASCADE)
#     file = models.FileField(upload_to=get_blog_other_file_upload_path)
