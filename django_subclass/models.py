import logging
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_init, post_save
from django.dispatch.dispatcher import receiver
from django.db import models
from django.contrib.contenttypes.models import ContentType,ContentTypeManager
from django.contrib.contenttypes import generic

from django_subclass import site

from logging import getLogger
logger = getLogger("my_logger")
hdlr = logging.StreamHandler()
hdlr.setLevel(logging.ERROR)
logger.addHandler(hdlr)
logger.error("Initialized")

class RealClassManager(models.Manager):

    def get_for_obj(self,obj):
        return self.get_query_set().get(model=obj.__class__.__name__)

    def get_for_class(self,cls):
        return self.get_query_set().get(model=cls.__name__)


class RealClass(ContentType):
    objects = RealClassManager()

# Create your models here.
class SubclassMapper(models.Model):
    """ Map a base class with a real proxy class

        real_type: type of the original proxy
    """
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    real_type = models.ForeignKey(RealClass, related_name="real_type")


@receiver(post_init,dispatch_uid="update_proxy")
def update_proxy(sender, **kwargs):
    """ Change the class object to the original proxy class
    """
    # Check if the class has been registered
    if sender in site.Register._registry:
        logger.debug("Sender %s found in registry" % sender)
        obj = kwargs['instance']
        # if the sender belong to the base class registry
        # the object class should be updated
        if sender in site.Register._bases_registry:
            logger.debug("Base class found in registry")
            # Construct the list of
            ct_list = []
            for base_type in site.Register._bases_registry[sender]:
                ct_list.append(ContentType.objects.get_for_model(base_type))

            # Retrieve the real type from the SubclassMapper
            try:
                rt = SubclassMapper.objects.get(object_id=obj.id,
                                                       content_type__in=ct_list).real_type
                new_class = site.Register._class_content_map[rt]
                logger.debug("Object class changed to %s " % new_class)
                obj.__class__ = new_class
            # If the object is not found, do not change the class
            except ObjectDoesNotExist:
                logging.debug("Object not found in MapperClass")


@receiver(post_save,dispatch_uid="save_instance")
def save_instance(sender, **kwargs):
    """ Save in SubclassMapper the object real type
        to be retrieve later
    """
    # If the class has been register
    if sender in site.Register._registry:
        # Only when the object is save for the first time
        if kwargs['created']:
            obj = kwargs['instance']
            logger.debug("Add object %s to mapper. Object type: %s" % (obj,obj.__class__))
#            import pdb;pdb.set_trace()
            ct = RealClass.objects.get_for_obj(obj)

            # create the real class mapping
            SubclassMapper.objects.create(content_object=obj,
                                          real_type=ct)
