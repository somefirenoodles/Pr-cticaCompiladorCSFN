"""Pruebas del analizador léxico de Mini C (Proyecto 1).

Verifican todas las reglas de la especificación: alfabeto, palabras reservadas,
patrones de tokens, políticas de separación, prioridades, diagnósticos LEX001,
recuperación y formato de salida.
"""

from minic.diagnostics.diagnostic_code import LEX001
from minic.lexer.lexer import Lexer
from minic.lexer.token_type import TokenType
from minic.output.diagnostic_printer import format_diagnostic
from minic.output.token_printer import format_token


def test_empty_source() -> None:
    tokens, diagnostics = Lexer("").scan()
    assert len(tokens) == 1
    assert tokens[0].type == TokenType.EOF
    assert tokens[0].lexeme == ""
    assert tokens[0].literal is None
    assert tokens[0].line == 1
    assert tokens[0].column == 1
    assert diagnostics == []


def test_section_7_case_1_clean_source() -> None:
    source = "int2 = 12abc;\nwhilex == -5"
    tokens, diagnostics = Lexer(source).scan()

    assert diagnostics == []

    expected = [
        (TokenType.IDENTIFIER, "int2", None, 1, 1),
        (TokenType.ASSIGN, "=", None, 1, 6),
        (TokenType.INTEGER_LITERAL, "12", 12, 1, 8),
        (TokenType.IDENTIFIER, "abc", None, 1, 10),
        (TokenType.SEMICOLON, ";", None, 1, 13),
        (TokenType.IDENTIFIER, "whilex", None, 2, 1),
        (TokenType.EQUAL_EQUAL, "==", None, 2, 8),
        (TokenType.MINUS, "-", None, 2, 11),
        (TokenType.INTEGER_LITERAL, "5", 5, 2, 12),
        (TokenType.EOF, "", None, 2, 13),
    ]

    assert len(tokens) == len(expected)
    for actual, (exp_type, exp_lexeme, exp_literal, exp_line, exp_col) in zip(tokens, expected):
        assert actual.type == exp_type
        assert actual.lexeme == exp_lexeme
        assert actual.literal == exp_literal
        assert actual.line == exp_line
        assert actual.column == exp_col

    lines = [format_token(t) for t in tokens]
    expected_output = [
        "IDENTIFIER 'int2' 1 1",
        "ASSIGN '=' 1 6",
        "INTEGER_LITERAL '12' 1 8",
        "IDENTIFIER 'abc' 1 10",
        "SEMICOLON ';' 1 13",
        "IDENTIFIER 'whilex' 2 1",
        "EQUAL_EQUAL '==' 2 8",
        "MINUS '-' 2 11",
        "INTEGER_LITERAL '5' 2 12",
        "EOF '' 2 13",
    ]
    assert lines == expected_output


def test_section_7_case_2_with_errors() -> None:
    source = "int x = @;\nx ! = 0; // fin"
    tokens, diagnostics = Lexer(source).scan()

    expected_tokens = [
        (TokenType.KW_INT, "int", None, 1, 1),
        (TokenType.IDENTIFIER, "x", None, 1, 5),
        (TokenType.ASSIGN, "=", None, 1, 7),
        (TokenType.SEMICOLON, ";", None, 1, 10),
        (TokenType.IDENTIFIER, "x", None, 2, 1),
        (TokenType.ASSIGN, "=", None, 2, 5),
        (TokenType.INTEGER_LITERAL, "0", 0, 2, 7),
        (TokenType.SEMICOLON, ";", None, 2, 8),
        (TokenType.IDENTIFIER, "fin", None, 2, 13),
        (TokenType.EOF, "", None, 2, 16),
    ]

    assert len(tokens) == len(expected_tokens)
    for actual, (exp_type, exp_lexeme, exp_literal, exp_line, exp_col) in zip(tokens, expected_tokens):
        assert actual.type == exp_type
        assert actual.lexeme == exp_lexeme
        assert actual.literal == exp_literal
        assert actual.line == exp_line
        assert actual.column == exp_col

    expected_diagnostics = [
        (LEX001, "error", "Carácter no reconocido: '@'", 1, 9),
        (LEX001, "error", "Carácter no reconocido: '!'", 2, 3),
        (LEX001, "error", "Carácter no reconocido: '/'", 2, 10),
        (LEX001, "error", "Carácter no reconocido: '/'", 2, 11),
    ]

    assert len(diagnostics) == len(expected_diagnostics)
    for actual, (exp_code, exp_sev, exp_msg, exp_line, exp_col) in zip(diagnostics, expected_diagnostics):
        assert actual.code == exp_code
        assert actual.severity == exp_sev
        assert actual.message == exp_msg
        assert actual.line == exp_line
        assert actual.column == exp_col

    diag_lines = [format_diagnostic(d) for d in diagnostics]
    expected_diag_lines = [
        "LEX001 error 1:9 Carácter no reconocido: '@'",
        "LEX001 error 2:3 Carácter no reconocido: '!'",
        "LEX001 error 2:10 Carácter no reconocido: '/'",
        "LEX001 error 2:11 Carácter no reconocido: '/'",
    ]
    assert diag_lines == expected_diag_lines


def test_keywords_vs_identifiers() -> None:
    source = "int while intx while1 _int _while INT While"
    tokens, diagnostics = Lexer(source).scan()
    assert diagnostics == []

    types = [t.type for t in tokens[:-1]]
    assert types == [
        TokenType.KW_INT,
        TokenType.KW_WHILE,
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
        TokenType.IDENTIFIER,
    ]


def test_all_symbols_and_operators() -> None:
    source = "= == != + - ( ) { } ;"
    tokens, diagnostics = Lexer(source).scan()
    assert diagnostics == []

    types = [t.type for t in tokens[:-1]]
    assert types == [
        TokenType.ASSIGN,
        TokenType.EQUAL_EQUAL,
        TokenType.NOT_EQUAL,
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.LPAREN,
        TokenType.RPAREN,
        TokenType.LBRACE,
        TokenType.RBRACE,
        TokenType.SEMICOLON,
    ]


def test_maximum_munch() -> None:
    source = "=== !== !=="
    tokens, diagnostics = Lexer(source).scan()
    assert diagnostics == []

    # === -> == and =
    # !== -> != and =
    # !== -> != and =
    types = [t.type for t in tokens[:-1]]
    assert types == [
        TokenType.EQUAL_EQUAL,
        TokenType.ASSIGN,
        TokenType.NOT_EQUAL,
        TokenType.ASSIGN,
        TokenType.NOT_EQUAL,
        TokenType.ASSIGN,
    ]


def test_number_literal_conversion() -> None:
    source = "007 0 42 100000000000000000000"
    tokens, diagnostics = Lexer(source).scan()
    assert diagnostics == []

    literals = [t.literal for t in tokens[:-1]]
    assert literals == [7, 0, 42, 100000000000000000000]


def test_tabs_and_newlines_positioning() -> None:
    # \t counts as 1 column, \r without \n counts as 1 column
    source = "\t\tint\r x;\n\tint"
    tokens, diagnostics = Lexer(source).scan()
    assert diagnostics == []

    # col 1: \t, col 2: \t, col 3: int -> (1, 3)
    # col 6: \r, col 7: ' ', col 8: x -> (1, 8)
    # col 9: ; -> (1, 9)
    # col 10: \n -> next line is line 2
    # line 2, col 1: \t, col 2: int -> (2, 2)
    assert tokens[0].type == TokenType.KW_INT
    assert (tokens[0].line, tokens[0].column) == (1, 3)

    assert tokens[1].type == TokenType.IDENTIFIER
    assert (tokens[1].line, tokens[1].column) == (1, 8)

    assert tokens[2].type == TokenType.SEMICOLON
    assert (tokens[2].line, tokens[2].column) == (1, 9)

    assert tokens[3].type == TokenType.KW_INT
    assert (tokens[3].line, tokens[3].column) == (2, 2)

    assert tokens[4].type == TokenType.EOF
    assert (tokens[4].line, tokens[4].column) == (2, 5)


def test_negative_number_separation() -> None:
    source = "-5"
    tokens, diagnostics = Lexer(source).scan()
    assert diagnostics == []
    assert tokens[0].type == TokenType.MINUS
    assert tokens[1].type == TokenType.INTEGER_LITERAL
    assert tokens[1].literal == 5


def test_number_followed_by_letters() -> None:
    source = "12abc"
    tokens, diagnostics = Lexer(source).scan()
    assert diagnostics == []
    assert tokens[0].type == TokenType.INTEGER_LITERAL
    assert tokens[0].lexeme == "12"
    assert tokens[0].literal == 12
    assert tokens[1].type == TokenType.IDENTIFIER
    assert tokens[1].lexeme == "abc"
