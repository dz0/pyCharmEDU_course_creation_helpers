import sys
from test_helper import run_common_tests, failed, passed, get_answer_placeholders

# https://docs.python.org/3/library/tokenize.html
from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from io import BytesIO
from collections import Counter
import random

def get_tokens(code, filter_spaces=True, group_by_parentheses_one_level=True):
    g = tokenize(BytesIO(code.encode('utf-8')).readline)  # tokenize the string
    tokens = [tokval for toknum, tokval, _, _, _ in g][1:]

    if group_by_parentheses_one_level:
        def group_by_parentheses_one_level():
            start = None
            tokens_some_grouped = []
            for nr, t in enumerate(tokens):
                # print(nr, repr(t))
                if not t:
                    continue

                if t in "[({":
                    if len(tokens) > nr+1 and tokens[nr+1]  in "])}":  # if not just empty parentheses
                        tokens[nr] += tokens[nr+1]
                        t = tokens[nr]
                        del tokens[nr+1]
                    else:
                        start = nr

                if start is None:
                    tokens_some_grouped .append ( t )

                if t in "])}" and start != None:
                    tokens_some_grouped.append( ''.join(tokens[start:nr+1]).replace(',', ', '))  # todo: maybe 1) use untokenize
                    start = None
            return tokens_some_grouped
        tokens = group_by_parentheses_one_level()

    if filter_spaces:
        tokens = [t for t in tokens if t.strip()]
    return tokens


def hints_by_token_comparison(input, expected , limit_hints=2, **tokens_kwargs):
    """

    :param input:
    :param expected:
    :param limit_hints: max number of hints per category (missing/unnecessary)
    :return:
    """
    a_tokens = get_tokens(input, **tokens_kwargs)
    b_tokens = get_tokens(expected, **tokens_kwargs)
    if a_tokens == b_tokens:
        msgs = [  "seems OK, maybe spacing is mangled.." ]


    a = Counter( a_tokens )
    b = Counter( b_tokens )
    if a == b:
        msgs =[ "Ordering or spacing is incorrect" ]

    unnecessary= a - b
    missing  = b - a

    if limit_hints:
        missing = list( missing.keys() )
        unnecessary = list( unnecessary.keys() )

        random.shuffle( missing )
        random.shuffle( unnecessary )

        missing = missing[:limit_hints]
        unnecessary = unnecessary[:limit_hints]

    msgs = messages_by_fragments(input, required=missing, unnecessary=unnecessary )
    return msgs

def code_highlight(txt):
    return "<span style='color:blue; font-family: monospace;'>%s</span>" % txt

def messages_by_fragments(placeholder, result=None, unnecessary=[], required=[]):
    
    msgs = []

    if result and  result in placeholder    and  len(placeholder) > len(result):
        msg = "Too much code in placeholder.."
        if placeholder.startswith(result):
            msg += " at the end..."
        if placeholder.endswith(result):
            msg += " at the beginning.."
        msgs.append( msg )

    if not isinstance(unnecessary, (list, tuple)):
        unnecessary = [unnecessary]
    if not isinstance(required, (list, tuple)):
        required = [required]

    for item in unnecessary:
        if item in placeholder:
            msgs .append( code_highlight(item) + " is not needed" )
    msgs.append("")
    for item in required:
        if not item in placeholder:
            msgs .append(  code_highlight(item) + " is needed "  )

    return msgs


def check_placeholder(placeholder, result,  required=[], unnecessary=[], human_nr=None, **hints_kwargs ):

    if placeholder == result:
        passed()

    else:
        # msgs = messages_by_fragments(placeholder, result, unnecessary=unnecessary, required=required)
        msgs = hints_by_token_comparison(placeholder, result, **hints_kwargs)
        if human_nr:
            msgs.insert(0, "Placeholder nr. %s:" %(human_nr))
        failed( '<br />'.join(msgs) )



# TEST
if __name__ == '__main__':
    # check_placeholder(placeholder='has_money == True', result='has_money', unnecessary=['=='], required='has_money')
    print( hints_by_token_comparison(input='has_money == True', expected='has_money',  limit_hints=5) )
    print( hints_by_token_comparison(input='len(data)>0', expected='data',  limit_hints=5) )
