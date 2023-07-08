from middleware.language import setup_middleware

i18n = setup_middleware()
_ = i18n.gettext
