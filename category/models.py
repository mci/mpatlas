from django.db import models
from django.utils.translation import ugettext_lazy as _
from uuslug import uuslug, slugify

from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase, TaggedItemBase

from ckeditor.fields import RichTextField

class Category(TagBase):
    # name and slug provided by TagBase

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __unicode__(self):
        return self.name

    def slugify(self, tag, i=None):
        slug = uuslug(tag, instance=self)
        if i is not None:
            slug += "_%d" % i
        return slug

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('category-info', args=[self.slug])


class TaggedItem(GenericTaggedItemBase):
    # Here is where you provide your custom Tag class.
    tag = models.ForeignKey(Category,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items")
    
    class Meta:
        verbose_name = _("Tagged Item")
        verbose_name_plural = _("Tagged Items")


class Details(models.Model):
    category = models.OneToOneField('Category', on_delete=models.CASCADE)
    summary = RichTextField('Short Summary', null=True, blank=True)
    description = RichTextField('Description', null=True, blank=True)

    def __unicode__(self):
        return self.category.name + ' details'

    class Meta:
        verbose_name = _("Category Details")
        verbose_name_plural = _("Category Details")
