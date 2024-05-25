from sqlmodel import SQLModel, event, text


async def create_db_and_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all, checkfirst=True)


@event.listens_for(SQLModel.metadata, "after_create")
async def receive_after_create(engine):
    async with engine.begin() as conn:

        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto"))
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
        await conn.execute(
            text(
                """
                CREATE OR REPLACE FUNCTION generate_searchable(nome VARCHAR, apelido VARCHAR, stack JSON)
                RETURNS TEXT AS $$
                BEGIN
                    RETURN nome || ' ' || apelido || stack;
                END;
                $$ LANGUAGE plpgsql IMMUTABLE;
                """
            )
        )
