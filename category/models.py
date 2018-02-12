from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from uuslug import uuslug, slugify

from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase, TaggedItemBase

from ckeditor.fields import RichTextField

@python_2_unicode_compatible  # only if you need to support Python 2
class Category(TagBase):
    # name and slug provided by TagBase

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
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
                            related_name="%(app_label)s_%(class)s_items")
    
    class Meta:
        verbose_name = _("Tagged Item")
        verbose_name_plural = _("Tagged Items")

@python_2_unicode_compatible  # only if you need to support Python 2
class Details(models.Model):
    category = models.OneToOneField('Category')
    summary = RichTextField('Short Summary', null=True, blank=True)
    description = RichTextField('Description', null=True, blank=True)

    def __str__(self):
        return self.category.name + ' details'

    class Meta:
        verbose_name = _("Category Details")
        verbose_name_plural = _("Category Details")
