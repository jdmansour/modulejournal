from datetime import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

import eventfile


class Module(models.Model):
    """ Represents one module """
    name = models.CharField(max_length=200)
    produced = models.DateField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('module_details', args=[str(self.pk)])


class JournalEntry(models.Model):
    """ Different things can go into a module's journal:  Notes,
        Images, and Runs (recorded data).  This is the common
        base class.  Every entry currently has a posted date
        in common.

        TODO: add user (there is a build-in user model in Django,
        and there is a UserField field to use this)
        """
    module = models.ForeignKey(Module)
    posted = models.DateTimeField(default=timezone.now)
    posted_by = models.ForeignKey(User)

    class Meta:
        ordering = ['-posted']
        verbose_name_plural = "journal entries"


class NoteEntry(JournalEntry):
    text = models.TextField()

    class Meta:
        verbose_name_plural = "note entries"

# https://docs.djangoproject.com/en/1.11/ref/models/fields/#django.db.models.FileField.upload_to
def module_upload_path(journalentry: JournalEntry, filename: str):
    """ Determines where to save uploaded files. """
    return 'module_{0}/{1}'.format(journalentry.module.id, filename)

class ImageEntry(JournalEntry):
    image = models.ImageField(upload_to=module_upload_path)
    
    class Meta:
        verbose_name_plural = "image entries"

    def image_tag(self):
        return u'<img src="%s" style="max-width: 300px; max-height: 300px;" />' % self.image.url
    image_tag.short_description = "Image"
    image_tag.allow_tags = True


class RunEntry(JournalEntry):
    runnumber = models.IntegerField()
    eventcount = models.BigIntegerField()
    recorded = models.DateTimeField()
    data = models.FileField(upload_to=module_upload_path)

    class Meta:
        verbose_name_plural = "run entries"

    def clean(self):
        """ Used to validate the uploaded file, and to read data from
            the header (recorded date and event count).abs
            
            TODO: It is probably stupid to have the event count in the
            header, since we do not know how many events we are going
            to have when we start recording!

            We should probably write an "event size" to the header, and
            then divide the file size by the event size.
            """

        try:
            header, data = eventfile.read_event_file(self.data)
        except ValueError:
            raise ValidationError("File is not a valid run file")
        self.runnumber = header['runnumber']
        self.eventcount = header['eventcount']
    
        recorded_str = header['recorded']
        recorded = datetime.strptime(recorded_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        self.recorded = recorded

    def __str__(self):
        return "Run {0} ({1} events)".format(self.runnumber, self.eventcount)


class AnalysisTool(models.Model):
    """ This is something we can run over one or multiple runs. """
    name = models.CharField(max_length=200)

class ToolRun(models.Model):
    """ This is the result of using an AnalysisTool on runs.
        It has the `tool`, the `inputRuns`, and multiple
        `OutputImage`s (below) can point to it.
    """
    inputRuns = models.ManyToManyField(RunEntry)
    tool = models.ForeignKey(AnalysisTool)

    def __str__(self):
        return "Run of %s" % self.tool.name


def toolrun_upload_path(obj, filename):
    """ Tells where to save the result of a tool run """
    return 'toolrun_{0}/{1}'.format(obj.toolrun.id, filename)


class OutputImage(models.Model):
    """ The result of an AnalysisTool, as a graphic.

        TODO: We could add another type to save other kinds
        of data, e.g. text, or a calculated number.
    """
    toolrun = models.ForeignKey(ToolRun)
    image = models.ImageField(upload_to=toolrun_upload_path)

    def image_tag(self):
        return u'<img src="%s" style="max-width: 300px; max-height: 300px;" />' % self.image.url
    image_tag.short_description = "Image"
    image_tag.allow_tags = True
