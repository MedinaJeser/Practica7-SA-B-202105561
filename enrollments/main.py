from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from schema import schema
from db.database import enrollment_collection

app = FastAPI()

graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/enrollments")

@app.get("/")
def root():
    return {"message": "Welcome HELLO to the Enrollment API with FastAPI, GraphQL, and MongoDB"}
