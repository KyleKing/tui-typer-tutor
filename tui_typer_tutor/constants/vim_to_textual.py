"""Vim to Textual Key Maps."""

from string import ascii_lowercase

from bidict import bidict

# Replace '<leader>' with ' ' on load
_special_keys = {
    "'": 'apostrophe',
    '!': 'exclamation_mark',
    '"': 'quotation_mark',
    '#': 'number_sign',
    '$': 'dollar_sign',
    '%': 'percent_sign',
    '&': 'ampersand',
    '(': 'left_parenthesis',
    ')': 'right_parenthesis',
    '*': 'asterisk',
    '+': 'plus',
    ',': 'comma',
    '-': 'minus',
    '.': 'full_stop',
    '/': 'slash',
    ':': 'colon',
    ';': 'semicolon',
    '<Bar>': 'vertical_line',
    '<Bslash>': 'backslash',
    '<Del>': 'delete',
    '<down>': 'down',
    '<Enter>': 'enter',
    '<Esc>': 'escape',
    '<gt>': 'greater_than_sign',
    '<left>': 'left',
    '<lt>': 'less_than_sign',
    '<Return>': 'return',
    '<right>': 'right',
    '<Space>': 'space',
    '<Tab>': 'tab',
    '<up>': 'up',
    '=': 'equals_sign',
    '?': 'question_mark',
    '@': 'at',
    '[': 'left_square_bracket',
    ']': 'right_square_bracket',
    '^': 'circumflex_accent',
    '_': 'underscore',
    '{': 'left_curly_bracket',
    '}': 'right_curly_bracket',
    '~': 'tilde',
}

VIM_TO_TEXTUAL = bidict({
    **_special_keys,
    **{f'<C-{letter}>': f'ctrl+{letter}' for letter in ascii_lowercase},
    **{f'<C-{vim_key}>': f'ctrl+{textual_key}' for vim_key, textual_key in _special_keys.items()},
    **{f'<F{idx}>': f'f{idx}' for idx in range(1, 13)},
})
"""Bi-directional mapping of VIM key maps to textual."""
