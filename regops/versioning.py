import asyncpg
import os

# Disable versioning if environment variable is set (useful for testing)
disable_versioning = os.environ.get("REGOPS_DISABLE_VERSIONING", "").lower() == "true"
# database connection details
database_username = os.environ.get("REGOPS_DB_USERNAME")
database_password = os.environ.get("REGOPS_DB_PASSWORD")
database_host = os.environ.get("REGOPS_DB_HOST")
database_port = os.environ.get("REGOPS_DB_PORT")
database_name = os.environ.get("REGOPS_DB_NAME")
database_schema = os.environ.get("REGOPS_DB_SCHEMA")

class DatabaseConnectionManager:
    connection = None
    async def __aenter__(self):
        if not disable_versioning:
            self.connection = await asyncpg.connect(
                user=database_username,
                password=database_password,
                host=database_host,
                port=database_port,
                database=database_name,
                server_settings={"search_path": database_schema}
            )
            return self.connection
        return None
    
    async def __aexit__(self, exc_type, exc, tb):
        if self.connection is not None:
            await self.connection.close()


async def getDocumentVersion() -> list:
    async with DatabaseConnectionManager() as connection:
        if connection:
            result = await connection.fetchval(
                "SELECT version FROM proj_joe_01.document_version")
        else:
            result = None
    if result is None:
        result = "1.0"
    version_array = result.split(".")
    if len(version_array) == 1:
        version_array.append(0)
    return version_array

async def setDocumentVersion(
    new_version: tuple=None
) -> str:
    if new_version is None:
        raise ValueError("Must provide new_version")
    
    _new_version_string = f"{new_version[0]}.{new_version[1]}"

    async with DatabaseConnectionManager() as connection:
        if connection:
            await connection.execute(
                "UPDATE document_version SET version = $1", _new_version_string)
            await connection.close()
    return new_version or [1,0]

async def getIncrementedVersion(
        increase_minor: bool=False, increase_major: bool=False) -> list:
    current_version = await getDocumentVersion()
    if increase_major:
        return [int(current_version[0]) + 1, 0]
    elif increase_minor:
        return [int(current_version[0]), int(current_version[1]) + 1]
    else:
        raise Exception("Must increase either major or minor version")
