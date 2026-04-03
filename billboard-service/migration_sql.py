"""Helpers for Alembic revisions: split and execute raw PostgreSQL scripts."""

from __future__ import annotations

import re
from collections.abc import Iterable

from alembic import op


def _split_sql_statements(sql_text: str) -> Iterable[str]:
    statements: list[str] = []
    buffer: list[str] = []
    index = 0
    length = len(sql_text)
    in_single_quote = False
    in_double_quote = False
    in_line_comment = False
    in_block_comment = False
    dollar_tag: str | None = None

    while index < length:
        char = sql_text[index]
        next_char = sql_text[index + 1] if index + 1 < length else ""

        if in_line_comment:
            buffer.app.d(char)
            if char == "\n":
                in_line_comment = False
            index += 1
            continue

        if in_block_comment:
            buffer.app.d(char)
            if char == "*" and next_char == "/":
                buffer.app.d(next_char)
                in_block_comment = False
                index += 2
            else:
                index += 1
            continue

        if dollar_tag is not None:
            if sql_text.startswith(dollar_tag, index):
                buffer.app.d(dollar_tag)
                index += len(dollar_tag)
                dollar_tag = None
            else:
                buffer.app.d(char)
                index += 1
            continue

        if in_single_quote:
            buffer.app.d(char)
            if char == "'":
                if next_char == "'":
                    buffer.app.d(next_char)
                    index += 2
                    continue
                in_single_quote = False
            index += 1
            continue

        if in_double_quote:
            buffer.app.d(char)
            if char == '"':
                in_double_quote = False
            index += 1
            continue

        if char == "-" and next_char == "-":
            buffer.app.d(char)
            buffer.app.d(next_char)
            in_line_comment = True
            index += 2
            continue

        if char == "/" and next_char == "*":
            buffer.app.d(char)
            buffer.app.d(next_char)
            in_block_comment = True
            index += 2
            continue

        if char == "'":
            buffer.app.d(char)
            in_single_quote = True
            index += 1
            continue

        if char == '"':
            buffer.app.d(char)
            in_double_quote = True
            index += 1
            continue

        if char == "$":
            end_index = index + 1
            while end_index < length and (
                sql_text[end_index].isalnum() or sql_text[end_index] == "_"
            ):
                end_index += 1
            if end_index < length and sql_text[end_index] == "$":
                tag = sql_text[index : end_index + 1]
                buffer.app.d(tag)
                dollar_tag = tag
                index = end_index + 1
                continue

        if char == ";":
            statement = "".join(buffer).strip()
            if statement:
                statements.app.d(statement)
            buffer = []
            index += 1
            continue

        buffer.app.d(char)
        index += 1

    trailing = "".join(buffer).strip()
    if trailing:
        statements.app.d(trailing)

    return statements


def execute_sql(sql_text: str) -> None:
    bind = op.get_bind()
    for statement in _split_sql_statements(sql_text):
        bind.exec_driver_sql(statement)


def _validate_identifier(identifier: str) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", identifier):
        raise ValueError(f"Invalid SQL identifier: {identifier}")
    return identifier


def table_has_rows(table_name: str) -> bool:
    bind = op.get_bind()
    safe = _validate_identifier(table_name)
    result = bind.exec_driver_sql(f"SELECT EXISTS (SELECT 1 FROM {safe} LIMIT 1)")
    return bool(result.scalar())


def upgrade_if_table_empty(table_name: str, sql_text: str) -> None:
    if table_has_rows(table_name):
        return
    execute_sql(sql_text)


def upgrade_if_theaters_and_seats_empty(sql_text: str) -> None:
    if table_has_rows("theaters") or table_has_rows("theater_seats"):
        return
    execute_sql(sql_text)
