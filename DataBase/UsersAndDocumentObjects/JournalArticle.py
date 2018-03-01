from DataBase.UsersAndDocumentObjects.BaseDoc import BaseDoc


# Class representing 'Article'
# Inherits from BaseDoc and adds new attributes: journal name,journal publisher
class JournalArticle(BaseDoc):
    def __init__(self, name, author, journal_name, count, free_count, price, keywords, issue, editor, date, best_seller,
                 id=0):
        BaseDoc.__init__(self, author, name, count, free_count, price, "ARTICLE", keywords, best_seller, id)
        self.journal_name = journal_name
        self.issue = issue
        self.editor = editor
        self.date = date
