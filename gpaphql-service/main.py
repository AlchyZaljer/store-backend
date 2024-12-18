from ariadne import make_executable_schema
from ariadne.asgi import GraphQL
import uvicorn

from gateway import type_defs, query, order_item


schema = make_executable_schema(type_defs, query, order_item)
app = GraphQL(schema)

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8004)
