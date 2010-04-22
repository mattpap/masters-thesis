

from pybtex.style.formatting import FormatterBase, toplevel
from pybtex.style.template import field, join, optional, sentence, tag, words
from pybtex.database.input.bibtex import Parser

class Formatter(FormatterBase):

    def format_title(self, title):

    def format_article(self, entry):
        #author = entry.fields['author']
        if 'volume' in entry.fields:
            volume_and_pages = join [field('volume'), optional [':', 'pages']]
        else:
            volume_and_pages = words ['pages', optional ['pages']]
        #import pdb
        #pdb.set_trace()
        template = toplevel [
            self.format_name(entry.persons['author'][0]),
            sentence [field('title')],
            sentence [
                tag('emph') [field('journal')], volume_and_pages, field('year')],
        ]
        return template.format_data(entry)

    def format_manual(self, entry):
        return toplevel.format_data(entry)

    def format_book(self, entry):
        return toplevel.format_data(entry)

    def format_booklet(self, entry):
        return toplevel.format_data(entry)

    def format_proceedings(self, entry):
        return toplevel.format_data(entry)

    def format_inproceedings(self, entry):
        return toplevel.format_data(entry)

    def format_incollection(self, entry):
        return toplevel.format_data(entry)

    def format_mastersthesis(self, entry):
        return toplevel.format_data(entry)

    def format_phdthesis(self, entry):
        return toplevel.format_data(entry)

    def format_techreport(self, entry):
        return toplevel.format_data(entry)

    def format_unpublished(self, entry):
        return toplevel.format_data(entry)

    def format_misc(self, entry):
        return toplevel.format_data(entry)

parser = Parser()

bib = parser.parse_file("../bibtex.bib")

formatted = Formatter().format_entries(bib.entries.items())
import pdb
pdb.set_trace()

print list(formatted)

from pybtex.backends import BackendBase

class Writer(BackendBase):
    symbols = {
        'ndash': '--',
        'newblock': '\n\\newblock ',
        'nbsp': '~'
    }

    def format_tag(self, tag_name, text):
        return r'\%s{%s}' % (tag_name, text)

    def write_prologue(self, maxlen):
        self.output('\\begin{thebibliography}{%s}' % ('8' * maxlen))

    def write_epilogue(self):
        self.output('\n\n\\end{thebibliography}\n')

    def write_entry(self, key, label, text):
        self.output('\n\n\\bibitem[%s]{%s}\n' % (label, key))
        self.output(text)

