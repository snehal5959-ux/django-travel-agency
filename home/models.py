from django.db import models

class Gallery(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(max_length=500, blank=True, null=True, help_text='Enter image URL')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
