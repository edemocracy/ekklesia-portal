import secrets

welcome_text = """\
    # Ekklesia Portal
"""

settings = {
    "app": {
        "title": "Ekklesia Portal Dev",
        "fail_on_form_validation_error": False,
        "force_ssl": False,
        "instance_name": "ekklesia_portal",
        "insecure_development_mode": False,
        "internal_login_enabled": True,
        "custom_footer_url": None,
        "source_code_url": "https://github.com/Piratenpartei/ekklesia-portal",
        "tos_url": None,
        "data_protection_url": None,
        "faq_url": None,
        "imprint_url": None,
        "report_url": None,
        "login_visible": False
    },
    "share": {
        "use_url_shortener": False,
        "hashtag": '',
        "promote_account": '',
        "email_topic": {
            "en": "Ekklesia Portal - Share Proposition",
            "de": "Ekklesia Portal - Teile Antrag"
        },
        "email_body": {
            "en": "I just wanted to share a proposition from the Ekklesia Portal!\n",
            "de": "Ich wollte nur einen Antrag vom Ekklesia Portal teilen!\n"
        },
        "tweet_msg": {
            "en": "I just wanted to share a proposition from the Ekklesia Portal!",
            "de": "Ich wollte nur einen Antrag vom Ekklesia Portal teilen!"
        },
    },
    "database": {
        "uri": "postgresql+psycopg2://ekklesia_portal:ekklesia_portal@127.0.0.1/ekklesia_portal"
    },
    "static_files": {
        "base_url": "/static",
    },
    "browser_session": {
        "secret_key": secrets.token_urlsafe(32),
        "cookie_secure": False
    }
}
