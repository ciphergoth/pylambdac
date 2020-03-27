import mistletoe
from mistletoe.block_token import BlockCode
from mistletoe.span_token import RawText

def extract_blockcode(b, node):
    if b and node.__class__ == RawText:
        yield node.content
    elif node.__class__ == BlockCode:
        b = True
    if hasattr(node, 'children'):
        for subnode in node.children:
            yield from extract_blockcode(b, subnode)

def blockcodes_as_string(fp):
    return "".join(extract_blockcode(False, mistletoe.Document(fp)))
