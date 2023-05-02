from googletrans import Translator


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


# def translate_django_model(model, language):
#     """Translates a Django model into another language using googletrans.

#     Args:
#         model (Django Model): The model to be translated.
#         language (str): The language to translate the model into.

#     Returns:
#         The translated model.
#     """
#     fields = get_all_string_attributes_in_Django_model(model)
#     # print(fields, language,model.__getattribute__(fields[0]))
#     translator = Translator()
#     translated_model = model
#     print(translated_model)
#     for field in fields:
#         translated_field = translator.translate(
#             getattr(translated_model, field), dest=language)
#         # setattr(translated_model, field, translated_field)
#         print(field, translated_field)
#     # translated_model = translator.translate("model", dest=language)
#     return translated_model

def translate_django_model(model, language):
    """
    Translates each attribute in a specific Django model into another language using googletrans.

    Parameters:
    model (Django Model): The Django model to be translated.
    language (str): The language to translate the model into.

    Returns:
    model (Django Model): The translated Django model.
    """
    translator = Translator()
    # print(model)
    fields = get_all_string_attributes_in_Django_model(model)
    # print("/********************************/")
    # print(fields, language)

    for field in fields:
        # print("########")
        if field != 'id':
            # print(type(getattr(model, field)))

            translated_field = translator.translate(
                str(getattr(model, field, None)).strip(), dest=language).text

            setattr(model, field, translated_field)
            # print(field, getattr(model, field))
    # print("/********************************/")
    return model


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
