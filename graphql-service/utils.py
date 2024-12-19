def load_schema(schema_path: str) -> str:
    with open(schema_path, "r", encoding="utf-8") as schema_file:
        return schema_file.read()
