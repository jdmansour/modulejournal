from django.contrib import admin
from . import models
from merged_inlines.admin import MergedInlineAdmin
# Register your models here.


# class JournalEntryInline(admin.TabularInline):
#     model = models.JournalEntry
    

class NoteEntryInline(admin.TabularInline):
    model = models.NoteEntry
    extra = 0
    # fields = ('image',)

class RunEntryInline(admin.TabularInline):
    model = models.RunEntry
    readonly_fields = ('runnumber', 'eventcount', 'recorded')
    exclude = ('posted',)
    extra = 0

class ImageEntryInline(admin.TabularInline):
    model = models.ImageEntry
    extra = 0

# def blub(*a):
#     return "x"

# class RunEntryInlineReverse(admin.TabularInline):
#     model = models.ToolRun.inputRuns.through
#     # readonly_fields = ('runnumber', 'eventcount', 'recorded')
#     # exclude = ('posted',)
#     extra = 0


# class ModuleAdmin(MergedInlineAdmin):
class MyModuleAdmin(admin.ModelAdmin):
    # model = models.Module
    inlines=(NoteEntryInline, RunEntryInline, ImageEntryInline)


admin.site.register(models.Module, MyModuleAdmin)
# admin.site.register(models.JournalEntry, list_display=['__str__', 'posted'])
admin.site.register(models.NoteEntry, list_display=['text', 'module', 'posted', 'posted_by'])
admin.site.register(models.ImageEntry, list_display=['image_tag', 'module', 'posted', 'posted_by'])
admin.site.register(models.RunEntry,
    list_display=['runnumber', 'eventcount', 'module', 'posted', 'posted_by', 'data'],
    readonly_fields=['runnumber', 'eventcount'])

class OutputImageInline(admin.StackedInline):
    model = models.OutputImage
    extra = 0
    fields = ('image_tag',)
    readonly_fields = ('image_tag',)

admin.site.register(models.ToolRun,
    admin.ModelAdmin,
    fields=['inputRuns'],
    readonly_fields=['inputRuns'],
    inlines=[OutputImageInline]
    )