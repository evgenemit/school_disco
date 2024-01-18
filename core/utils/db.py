import asyncpg


class Database:

    def __init__(self, pool_connect: asyncpg.pool.Pool) -> None:
        self.pool_connect = pool_connect

    async def execute(self, text: str) -> None:
        async with self.pool_connect.acquire() as connection:
            await connection.execute(text)
    
    async def fetch(self, text: str) -> list:
        async with self.pool_connect.acquire() as connection:
            return await connection.fetch(text)
    
    async def fetchrow(self, text: str) -> list:
        async with self.pool_connect.acquire() as connection:
            return await connection.fetchrow(text)

    async def close(self) -> None:
        await self.pool_connect.close()

    async def create_user(self, user_id: int, full_name: str) -> None:
        """Создание пользователя"""
        await self.execute(
            f"""
            INSERT INTO users (user_id, name) VALUES
            ('{user_id}', '{full_name}')
            ON CONFLICT (user_id) DO UPDATE SET name = '{full_name}';
            """
        )

    async def create_track(
        self,
        track_name: str,
        artist_name: str,
        user_id: int
    ) -> None:
        """Создание трека"""
        await self.execute(
            f"""
            INSERT INTO tracks (track_name, artist_name, user_id) VALUES
            ('{track_name}', '{artist_name}', '{user_id}');
            """
        )
    
    async def get_playlist(self) -> list:
        """Получение треков из плейлиста"""
        return await self.fetch("SELECT * FROM tracks WHERE approved = true;")

    async def get_next_track(self) -> list:
        """Получение одного необработанного трека"""
        return await self.fetchrow("SELECT * FROM tracks WHERE approved = false")
