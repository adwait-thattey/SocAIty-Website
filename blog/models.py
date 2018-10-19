from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
import datetime
import os


# Create your models here.
def tag_name_validator(tag_name):
    if '_' in tag_name:
        raise ValidationError("The Tag Name can not contain underscores (_)")


class Tag(models.Model):
    name = models.CharField(verbose_name="Tag Name", max_length=15, validators=[tag_name_validator])

    def __str__(self):
        return self.name

    @property
    def blogcount(self):
        return self.blog_set.count()


def validate_blog_file_extension(incoming_file):
    extension = os.path.splitext(incoming_file.name)[1]
    allowed_extensions = ['.md', '.html']
    if extension.lower() not in allowed_extensions:
        raise ValidationError("This file type is not allowed")


def get_blog_upload_path(instance, filename):
    return os.path.join("blogs", str(instance.id), filename)


def get_blog_image_upload_path(instance, filename):
    return os.path.join("blogs", str(instance.id), "images", filename)


def blog_title_validator(title):
    if '-' in title:
        raise ValidationError("The Title can not contain '-' as it will interfere with the slug url!")


class Blog(models.Model):
    title = models.CharField(max_length=50, validators=[blog_title_validator])
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    create_date = models.DateTimeField(verbose_name='Date Published', auto_now_add=True, editable=False)
    upvotes = models.PositiveIntegerField(verbose_name="Upvotes", editable=False, default=0)
    downvotes = models.PositiveIntegerField(verbose_name="Downvotes", editable=False, default=0)
    short_description = models.TextField(blank=True, null=True)
    # TODO Put relevant maxlength limit here
    body = RichTextUploadingField(blank=True, null=True)
    picture = models.ImageField(blank=True, null=True, upload_to=get_blog_image_upload_path)
    slug = models.SlugField(max_length=200, null=True, blank=True,
                            help_text="This slug will form the url of your blog. The Url will be blogs/blog/<your username>/<slug>")
    tags = models.ManyToManyField(to=Tag, blank=True)
    views = models.PositiveIntegerField(verbose_name="Views", default=0, editable=False)

    # TODO Improve the procedure of counting views (See the blog detail view)

    class Meta:
        ordering = ['-create_date']
        unique_together = ['slug', 'author', 'title']

    def __str__(self):
        return str(self.title) + ' : by ' + str(self.author)

    def was_published_recently(self):
        return self.create_date >= timezone.now() - datetime.timedelta(minutes=1)
        # TODO Change this to relevant time duration

    def recount_upvotes(self):
        self.upvotes = self.vote_set.filter(upvote_downvote=1).count()
        self.save()

    def recount_downvotes(self):
        self.downvotes = self.vote_set.filter(upvote_downvote=-1).count()
        self.save()

    def recount_votes(self):
        self.recount_upvotes()
        self.recount_downvotes()

    # TODO Set Cron Job to call recount periodically

    def upvote(self, user):
        vote = Vote(voter=user, blog=self, upvote_downvote=0)
        vote.save()
        vote.upvote()

    def downvote(self, user):
        vote = Vote(voter=user, blog=self, upvote_downvote=0)
        vote.save()
        vote.downvote()

    def save(self, *args, **kwargs):
        if str(self.slug) == "None":
            self.slug = self.title.lower().replace(' ', '-')

        try:
            super().save()
        except IntegrityError:
            raise ValidationError(
                "You have another blog with either same title or same slug. Please change title of this blog")


# @receiver(pre_save,sender=Blog)
# def pre_save_slug(sender,**kwargs):
#     slug = slugify(kwargs['instance'].title)
#     kwargs['instance'].slug=slug

class Vote(models.Model):
    voter = models.ForeignKey(to=User, on_delete=models.CASCADE)
    blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE)
    vote_time = models.DateTimeField(auto_now=True, editable=False)
    upvote_downvote = models.SmallIntegerField(default=0, validators=[MinValueValidator(-1), MaxValueValidator(1)],
                                               help_text="-1 for downvote, 0 for none, 1 for upvote"
                                               )

    class Meta:
        unique_together = ('voter', 'blog')

    def upvote(self):
        if self.upvote_downvote != 1:
            pre = self.upvote_downvote
            self.upvote_downvote = 1
            self.save()

            self.blog.upvotes += 1
            if pre == -1:
                self.blog.downvotes -= 1
            self.blog.save()

    def downvote(self):
        if self.upvote_downvote != -1:
            pre = self.upvote_downvote
            self.upvote_downvote = -1
            self.save()

            self.blog.upvotes -= 1
            if pre == 1:
                self.blog.upvotes -= 1
            self.blog.save()

    def novote(self):
        if self.upvote_downvote == 1:
            self.upvote_downvote = 0
            self.save()
            self.blog.upvotes -= 1

        elif self.upvote_downvote == -1:
            self.upvote_downvote = 0
            self.save()
            self.blog.downvotes -= 1

        self.blog.save()

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            vote = Vote.objects.get(voter=self.voter, blog=self.blog)
            if self.upvote_downvote == -1:
                vote.downvote()
            elif self.upvote_downvote == 0:
                self.novote()
            elif self.upvote_downvote == 1:
                self.upvote()
            else:
                self.novote()
                raise ValueError("One of the votes has a value other than -1, 0 1")

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
