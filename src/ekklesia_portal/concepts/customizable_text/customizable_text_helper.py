from ekklesia_portal.datamodel import CustomizableText


def customizable_text(request, name):
    lang = request.i18n.get_locale().language
    # TODO: add fallback to default language and/or maybe a default text from the translations.
    customizable_text = request.q(CustomizableText).filter_by(lang=lang, name=name).scalar()
    if customizable_text is None:
        return name
    else:
        return customizable_text.text
