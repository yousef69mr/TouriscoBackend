from googletrans import Translator

from django.db import models

class TranslatableModelManager(models.Manager):
    def create(self, **kwargs):
        translatable_fields = [field.name for field in self.model._meta.fields if isinstance(field, models.CharField)]
        translator = Translator()
        for field_name in translatable_fields:
            if field_name in kwargs and kwargs[field_name]:
                kwargs[field_name] = translator.translate(kwargs[field_name]).text
        return super().create(**kwargs)

    def save(self, *args, **kwargs):
        translatable_fields = [field.name for field in self.model._meta.fields if isinstance(field, models.CharField)]
        translator = Translator()
        for obj in self.all():
            for field_name in translatable_fields:
                if getattr(obj, field_name):
                    setattr(obj, field_name, translator.translate(getattr(obj, field_name)).text)
            obj.save()


def get_all_string_attributes_in_Django_model(model):
    """
    This function takes a Django model as an argument and returns a list of all string attributes.

    Args:
        model (Django Model): The model to get the string attributes from.

    Returns:
        list: A list of all string attributes in the model.
    """
    string_attributes = []
    for field in model._meta.get_fields():
        if field.get_internal_type() == 'CharField' or field.get_internal_type() == 'TextField':
            string_attributes.append(field.name)
    # print(string_attributes)
    return string_attributes


def translate_django_model(model_instance, target_language):
    translator = Translator()

    for field in model_instance._meta.fields:
        if isinstance(field, models.CharField) or isinstance(field, models.TextField):
            # print(field)
            value = getattr(model_instance, field.name)
            if value:
                translated_value = translator.translate(value, dest=target_language).text
                setattr(model_instance, field.name, translated_value if translated_value else '')
    return model_instance

def return_django_models_except(models_to_exclude):
    """
    Return all Django models except specific models.

    Parameters:
    models_to_exclude (list): List of models to exclude from the returned list.

    Returns:
    list: List of Django models except the models specified in the parameter.
    """
    from django.apps import apps
    all_models = apps.get_models()
    return [model for model in all_models if model not in models_to_exclude]


def return_django_models():
    """
    Returns all Django models.

    Returns:
        list: A list of all Django models.
    """
    from django.apps import apps
    return apps.get_models()


def invertedIndex(models):
    """
    Return an inverted index which stores term and its frequency in each Django model.

    Parameters:
    models (list): A list of Django models

    Returns:
    dict: An inverted index of terms and their frequencies in each model.
    """
    inverted_index = {}
    for model in models:
        for field in model._meta.fields:
            if field.get_internal_type() == 'CharField':
                terms = field.value_from_object(model).split()
                for term in terms:
                    if term in inverted_index:
                        inverted_index[term] += 1
                    else:
                        inverted_index[term] = 1
    return inverted_index


import re

def extract_coordinates(embedded_link):
    matches = re.findall(r"!2d([-+]?\d+\.\d+)!3d([-+]?\d+\.\d+)", embedded_link)
    if matches:
        return float(matches[0][1]), float(matches[0][0])
    else:
        return None
    


def isInteger(num):
    try:
        int(num)
        # If num can be converted to integer without raising ValueError, then it's a valid number
        print("Valid Integer")
        return True
    except ValueError as e:
        return False