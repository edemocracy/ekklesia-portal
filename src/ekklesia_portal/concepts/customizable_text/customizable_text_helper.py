from ekklesia_portal.datamodel import CustomizableText


def customizable_text(request, name, lang=None):
    if lang is None:
        lang = request.i18n.get_locale().language

    customizable_text = request.q(CustomizableText).filter_by(lang=lang, name=name).scalar()

    if customizable_text is None:
        fallback_language = request.app.settings.app.fallback_language
        customizable_text = request.q(CustomizableText).filter_by(lang=fallback_language, name=name).scalar()

    if customizable_text is None:
        return request.i18n.gettext(name)
    else:
        return customizable_text.text
