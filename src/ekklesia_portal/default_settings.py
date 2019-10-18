import secrets

welcome_text = """\
    # Ekklesia Portal
"""

settings = {
    "app": {
        "title": "Ekklesia Portal Dev",
        "fail_on_form_validation_error": False,
        "instance_name": "ekklesia_portal",
        "insecure_development_mode": False,
        "internal_login_enabled": True,
        "custom_footer_url": None,
        "source_code_url": "https://github.com/Piratenpartei/ekklesia-portal",
        "tos_url": None,
        "faq_url": None,
        "imprint_url": None,
        "welcome_text": {
            "de": welcome_text,
            "en": welcome_text,
            "fr": welcome_text
        }
    },
    "share": {
        "use_url_shortener": False,
        "hashtag": '',
        "promote_account": ''
    },
    "share_email_topic": {
        "en": "Ekklesia Portal - Share Proposition",
        "de": "Ekklesia Portal - Teile Antrag",
        "fr": "Ekklesia Portal - Share Proposition"
    },
    "share_email_body": {
        "en": "I just wanted to share a proposition from the Ekklesia Portal!\n",
        "de": "Ich wollte nur einen Antrag vom Ekklesia Portal teilen!\n",
        "fr": "I just wanted to share a proposition from the Ekklesia Portal!\n"
    },
    "share_tweet_msg": {
        "en": "I just wanted to share a proposition from the Ekklesia Portal!",
        "de": "Ich wollte nur einen Antrag vom Ekklesia Portal teilen!",
        "fr": "I just wanted to share a proposition from the Ekklesia Portal!"
    },
    "database": {
        "uri": "postgresql+psycopg2://ekklesia_portal:ekklesia_portal@127.0.0.1/ekklesia_portal"
    },
    "browser_session": {
        "secret_key": secrets.token_urlsafe(32),
        "cookie_secure": False
    }
}
