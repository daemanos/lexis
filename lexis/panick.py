#!/usr/bin/python3

import panflute as pf
from functools import cmp_to_key, partial
from itertools import zip_longest

def validate_doc(doc):
    """
    Check to see if the given document is a valid dictionary, that is, that it
    contains a single definition list.
    """
    return len(doc.content) == 1 and \
           isinstance(doc.content[0], pf.DefinitionList)


def gen_collation(order):
    """
    Generate a collation (mapping from characters to their position in a
    sorting order) from a sorting order.
    """

    coll = {}
    for pos, letter in enumerate(order):
        if isinstance(letter, pf.MetaList):
            for inline in letter:
                coll[inline.content[0].text] = pos
        else:
            coll[letter.content[0].text] = pos

    return coll


def term(item):
    """
    Get the term (as a string) of dictionary entry.
    """

    return pf.stringify(pf.Para(*item.term), newlines = False)


def strip_term(term, collation):
    """Strip out undefined letters from a term."""
    return ''.join(c for c in term if c in collation)


def cmp_entries(e, f, collation):
    """
    Compare two dictionary entries with the given collation.
    """
    te, tf = strip_term(term(e), collation), strip_term(term(f), collation)
    for le, lf in zip_longest(te, tf):
        if le is None: return -1 # first word ran out of letters
        if lf is None: return 1 # second word ran out of letters

        pe, pf = collation[le], collation[lf]
        if pe != pf:
            return pe - pf

    return 0


def latex_dict(doc):
    lst = list(doc.content[0].content)
    coll = gen_collation(doc.metadata['sort_order'])

    lst = sorted(lst, key = cmp_to_key(partial(cmp_entries, collation = coll)))

    doc.content[0] = pf.DefinitionList(*lst)
    return doc


formats = {
        'latex': latex_dict
        }

def main():
    doc = pf.load()
    if validate_doc(doc) and doc.format in formats:
        pf.dump(formats[doc.format](doc))
    else:
        pf.dump(doc)

if __name__ == '__main__':
    main()
