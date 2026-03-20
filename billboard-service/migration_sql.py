import re
from pathlib import Path
from typing import Iterable

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
            buffer.append(char)
            if char == "\n":
                in_line_comment = False
            index += 1
            continue

        if in_block_comment:
            buffer.append(char)
            if char == "*" and next_char == "/":
                buffer.append(next_char)
                in_block_comment = False
                index += 2
            else:
                index += 1
            continue

        if dollar_tag is not None:
            if sql_text.startswith(dollar_tag, index):
                buffer.append(dollar_tag)
                index += len(dollar_tag)
                dollar_tag = None
            else:
                buffer.append(char)
                index += 1
            continue

        if in_single_quote:
            buffer.append(char)
            if char == "'":
                if next_char == "'":
                    buffer.append(next_char)
                    index += 2
                    continue
                in_single_quote = False
            index += 1
            continue

        if in_double_quote:
            buffer.append(char)
            if char == '"':
                in_double_quote = False
            index += 1
            continue

        if char == "-" and next_char == "-":
            buffer.append(char)
            buffer.append(next_char)
            in_line_comment = True
            index += 2
            continue

        if char == "/" and next_char == "*":
            buffer.append(char)
            buffer.append(next_char)
            in_block_comment = True
            index += 2
            continue

        if char == "'":
            buffer.append(char)
            in_single_quote = True
            index += 1
            continue

        if char == '"':
            buffer.append(char)
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
                buffer.append(tag)
                dollar_tag = tag
                index = end_index + 1
                continue

        if char == ";":
            statement = "".join(buffer).strip()
            if statement:
                statements.append(statement)
            buffer = []
            index += 1
            continue

        buffer.append(char)
        index += 1

    trailing = "".join(buffer).strip()
    if trailing:
        statements.append(trailing)

    return statements


def execute_sql(sql_text: str) -> None:
    bind = op.get_bind()
    for statement in _split_sql_statements(sql_text):
        bind.exec_driver_sql(statement)


def _validate_identifier(identifier: str) -> str:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", identifier):
        raise ValueError(f"Invalid SQL identifier: {identifier}")
    return identifier


def run_sql_file(file_name: str) -> None:
    sql_path = Path(__file__).resolve().parent / "db" / file_name
    execute_sql(sql_path.read_text(encoding="utf-8"))


def table_has_rows(table_name: str) -> bool:
    bind = op.get_bind()
    safe_table_name = _validate_identifier(table_name)
    result = bind.exec_driver_sql(
        f"SELECT EXISTS (SELECT 1 FROM {safe_table_name} LIMIT 1)"
    )
    return bool(result.scalar())


def run_migration_sql(base_name: str, direction: str) -> None:
    run_sql_file(f"{base_name}.{direction}.sql")


def run_migration_sql_if_table_empty(
    base_name: str, direction: str, table_name: str
) -> None:
    if direction == "up" and table_has_rows(table_name):
        return
    run_migration_sql(base_name, direction)
