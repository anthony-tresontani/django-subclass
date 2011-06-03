import logging

logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)
hdlr = logging.StreamHandler()
hdlr.setLevel(logging.DEBUG)
logger.addHandler(hdlr)
logger.error("Initialized")

class Register():
    """ Manage the registration of proxies classes
    """
    _registry = []  # Proxies classes to be managed
    _bases_registry = {} # dict key: base class; value: subclass
    _class_content_map = {}

    @classmethod
    def register(cls, model):
        """
            Register a model and its base class
        """
        from models import  RealClass
        # Register the model if not  already done
        print "MODEL: %s" % model
        if model not in cls._registry:
            logger.debug("Add in registry %s" % model)
            cls._registry.append(model)
            rt = RealClass(app_label=model.__name__,
                                        model=model.__name__,
                                        name=model.__name__)
            rt.save()
            cls._class_content_map[rt] = model
            logger.debug("Real class: %s " % RealClass.objects.all())
            # Register the base class
        # Only work for one base class
        if len(model.__bases__) == 1:
            # Add the base the class to the registry
            # base model should be managed too
            if model.__bases__[0] not in cls._registry:
                logger.debug("Add base class in base class registry: %s" % model.__bases__[0])
                cls._registry.append(model.__bases__[0])
                # Check if the base class is already registered
            # if yes, add it the model class to the list
            if model.__bases__[0] in cls._bases_registry:
                cls._bases_registry[model.__bases__[0]].append(model)
            else:
                cls._bases_registry[model.__bases__[0]] = [model]

    @classmethod
    def clean(cls):
        cls._registry = []
        cls._bases_registry = {}


# Bound the register method to the class method
register = Register.register