from database.dbApi import DB_API

db_api = DB_API()
db_api.connect()
current_lang = db_api.get_current_language()

if current_lang == 'ru':
    from lexicon.lexicon_RU import LEXICON_ERRORS
elif current_lang == 'en':
    from lexicon.lexicon_ENG import LEXICON_ERRORS
elif current_lang == 'uz':
    from lexicon.lexicon_UZB import LEXICON_ERRORS





print(LEXICON_ERRORS['empty'])
