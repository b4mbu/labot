from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    BigInteger,
)


def create_metadata():
    metadata = MetaData()

    user = Table(
        "users",
        metadata,
        Column("id", Integer(), primary_key=True, autoincrement=True),
        Column("user", Text(), nullable=False),
        Column("full_name", Text(), nullable=False),
        Column("telegram_id", BigInteger(), nullable=False),
    )

    labs = Table(
        "labs",
        metadata,
        Column("id", Integer(), primary_key=True, autoincrement=True),
        Column("name", Text(), nullable=False),
        Column("description", Text(), nullable=False),
        Column("creator_id", Integer(), ForeignKey("users.id")),
    )

    variants = Table(
        "variants",
        metadata,
        Column("id", Integer(), primary_key=True, autoincrement=True),
        Column("name", Text(), nullable=False),
        Column("task", Text(), nullable=False),
        Column("count", Integer(), nullable=False),
        Column("lab_id", Integer(), ForeignKey("users.id")),
    )

    users_variants = Table(
        "users_variants",
        metadata,
        Column("id", Integer(), primary_key=True, autoincrement=True),
        Column("user_id", Integer(), ForeignKey("users.id")),
        Column("variant_id", Integer(), ForeignKey("variants.id")),
    )

    tokens = Table(
        "tokens",
        metadata,
        Column("id", Integer(), primary_key=True, autoincrement=True),
        Column("token", Text()),
        Column("role", Text()),
        Column("count_of_activation", Integer()),
    )
    return metadata
