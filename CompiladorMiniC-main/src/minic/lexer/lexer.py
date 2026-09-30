"""Analizador léxico de Mini C.

Se implementa en el **proyecto 1**. Aquí solo quedan el estado y las firmas;
cada método describe lo que debe hacer según el capítulo IV, §4.4.
"""

from minic.diagnostics.diagnostic_bag import DiagnosticBag
from minic.lexer.lexer_result import LexerResult
from minic.lexer.token import Token


class Lexer:
    """Convierte el texto fuente en una lista de tokens.

    Uso: ``tokens, diagnostics = Lexer(source).scan()``.
    """

    def __init__(self, source: str) -> None:
        """Prepara el recorrido de ``source`` desde la línea 1, columna 1."""
        self._source = source
        self._start = 0
        self._current = 0
        self._line = 1
        self._column = 1
        self._start_line = 1
        self._start_column = 1
        self._tokens: list[Token] = []
        self._diagnostics = DiagnosticBag()

    def scan(self) -> LexerResult:
        """Recorre toda la fuente y devuelve los tokens y los diagnósticos.

        Mientras no se llegue al final: marca el inicio del lexema (índice,
        línea y columna) y llama a ``_scan_token``. Al terminar agrega
        exactamente un ``EOF`` con lexema vacío en la posición final.

        Devuelve:
            ``LexerResult(tokens, diagnostics)``.

        Referencia: capítulo IV, §4.4 (API y token ``EOF``).
        """
        raise NotImplementedError("TODO: proyecto 1 — implementar Lexer.scan")

    def _is_at_end(self) -> bool:
        """Indica si ya se consumió todo el texto fuente."""
        raise NotImplementedError("TODO: proyecto 1 — implementar Lexer._is_at_end")

    def _peek(self) -> str:
        """Devuelve el carácter actual sin consumirlo, o ``""`` al final."""
        raise NotImplementedError("TODO: proyecto 1 — implementar Lexer._peek")

    def _peek_next(self) -> str:
        """Devuelve el carácter siguiente al actual sin consumirlo, o ``""``."""
        raise NotImplementedError("TODO: proyecto 1 — implementar Lexer._peek_next")

    def _advance(self) -> str:
        """Consume y devuelve el carácter actual, actualizando la posición.

        Cada carácter suma una columna; ``\\n`` suma una línea y reinicia la
        columna en 1 (capítulo IV, §4.4, posiciones).
        """
        raise NotImplementedError("TODO: proyecto 1 — implementar Lexer._advance")

    def _scan_token(self) -> None:
        """Reconoce un token a partir del carácter actual.

        Orden de decisión:
        1. Espacio en blanco (``WHITESPACE``): se consume sin producir token.
        2. Inicio de identificador: ``_scan_identifier``.
        3. Dígito: ``_scan_number``.
        4. Operador o símbolo: ``_scan_operator``.
        5. Cualquier otro carácter: ``_report_unrecognized``.
        """
        raise NotImplementedError("TODO: proyecto 1 — implementar Lexer._scan_token")

    def _scan_identifier(self) -> None:
        """Consume ``[A-Za-z_][A-Za-z0-9_]*`` y emite el token.

        Primero se consume el nombre completo y después se consulta
        ``KEYWORDS``: si está, el tipo es la reservada; si no, ``IDENTIFIER``.
        """
        raise NotImplementedError("TODO: proyecto 1 — implementar Lexer._scan_identifier")

    def _scan_number(self) -> None:
        """Consume ``[0-9]+`` y emite ``INTEGER_LITERAL`` con su valor en base 10.

        El valor va en ``literal`` como ``int`` sin cota (capítulo IV, §4.4).
        """
        raise NotImplementedError("TODO: proyecto 1 — implementar Lexer._scan_number")

    def _scan_operator(self) -> bool:
        """Intenta reconocer un operador o símbolo en la posición actual.

        Consulta ``DOUBLE`` antes que ``SINGLE`` (máxima coincidencia). Si
        reconoce algo, lo consume, emite el token y devuelve ``True``; si no,
        devuelve ``False`` sin consumir nada.
        """
        raise NotImplementedError("TODO: proyecto 1 — implementar Lexer._scan_operator")

    def _add_token(self, token_type: str, literal: int | None = None) -> None:
        """Agrega un ``Token`` con el lexema entre el inicio marcado y la posición actual.

        La línea y la columna son las del **inicio** del lexema.
        """
        raise NotImplementedError("TODO: proyecto 1 — implementar Lexer._add_token")

    def _report_unrecognized(self) -> None:
        """Registra ``LEX001`` para el carácter actual, lo consume y continúa.

        Mensaje: ``Carácter no reconocido: '<c>'`` en la línea y la columna del
        carácter (``diagnostic_code.unrecognized_character``).
        """
        raise NotImplementedError("TODO: proyecto 1 — implementar Lexer._report_unrecognized")
