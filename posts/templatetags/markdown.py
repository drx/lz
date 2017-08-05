import re

import mistune
from django import template
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name

register = template.Library()


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang=None):
        if not lang:
            return '\n<pre><code>{}</code></pre>\n'.format(mistune.escape(code))

        if lang == 'objdump-nasm':
            # Insert tabs into the code so that the objdump-nasm lexer can work correctly.

            hex_re = r'[0-9A-Za-z]'
            code = re.sub(fr'^( *)({hex_re}+:)(\s*?)((?:{hex_re}{hex_re} )+) {{,8}}( *)([a-zA-Z].*?)$',
                          r'\1\2\t\4\5\t\6',
                          code, flags=re.M)

        lexer = get_lexer_by_name(lang, stripnl=False)
        formatter = HtmlFormatter()
        code = highlight(code, lexer, formatter)
        code = code.replace('\t', '  ')
        return code

    def block_html(self, html):
        return html + '\n'


class BetterBlockGrammar(mistune.BlockGrammar):
    block_tag = mistune._block_tag
    valid_attr = mistune._valid_attr
    block_html = re.compile(
        r'^ *(?:{}|{}|{}) *'.format(
            r'<!--[\s\S]*?-->',

            # One-liner outer block tags.
            fr'<({block_tag})((?:{valid_attr})*?)>([ \t\r\f\v\S]*?)<\/\1>',

            # All other block tags.
            fr'<()\/?{block_tag}(?:{valid_attr})*?\s*\/?>', )
    )
    fences = re.compile(
        r'^ *(`{3,}|~{3,}) *(\S+)? *\n'  # ```lang
        r'([\s\S]+?)'
        r'\1 *(?:\n+|$)'  # ```
    )


@register.filter
def markdown(value):
    renderer = HighlightRenderer()

    block = mistune.BlockLexer(BetterBlockGrammar())

    return mistune.Markdown(escape=False, renderer=renderer, block=block)(value)
