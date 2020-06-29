from ekklesia_portal.datamodel import CustomizableText


class CustomizableTexts:

    def customizable_texts(self, q):
        query = q(CustomizableText)
        return query.all()
