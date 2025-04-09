import strawberry
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from db.database import evaluation_collection

@strawberry.type
class Evaluation:
    id: str
    title: str
    description: str
    course_id: str
    type: str
    difficulty: str
    status: str
    url: str
    createdAt: str
    updatedAt: str

def serialize_evaluation(evaluation):
    """ Convierte `_id` a `id` en los resultados de MongoDB """
    return Evaluation(
        id=str(evaluation["_id"]),
        title=evaluation["title"],
        description=evaluation["description"],
        course_id=evaluation["course_id"],
        type=evaluation["type"],
        difficulty=evaluation["difficulty"],
        status=evaluation["status"],
        url=evaluation["url"],
        createdAt=evaluation["createdAt"],
        updatedAt=evaluation["updatedAt"]
    )

@strawberry.type
class Query:
    @strawberry.field
    def get_evaluations(self) -> List[Evaluation]:
        evaluations = list(evaluation_collection.find())
        return [serialize_evaluation(e) for e in evaluations]

    @strawberry.field
    def get_evaluation_by_id(self, id: str) -> Optional[Evaluation]:
        evaluation = evaluation_collection.find_one({"_id": ObjectId(id)})
        if not evaluation:
            return None
        return serialize_evaluation(evaluation)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_evaluation(self, title: str, description: str, course_id: str, type: str, difficulty: str, status: str, url: str) -> Evaluation:
        now = datetime.utcnow().isoformat()
        new_evaluation = {
            "title": title,
            "description": description,
            "course_id": course_id,
            "type": type,
            "difficulty": difficulty,
            "status": status,
            "url": url,
            "createdAt": now,
            "updatedAt": now
        }
        result = evaluation_collection.insert_one(new_evaluation)
        new_evaluation["_id"] = result.inserted_id  # 🔹 Agregar manualmente `_id`
        return serialize_evaluation(new_evaluation)

    @strawberry.mutation
    def update_evaluation(self, id: str, title: Optional[str] = None, description: Optional[str] = None, type: Optional[str] = None, difficulty: Optional[str] = None, status: Optional[str] = None, url: Optional[str] = None) -> Optional[Evaluation]:
        now = datetime.utcnow().isoformat()
        update_fields = {"updatedAt": now}

        if title is not None:
            update_fields["title"] = title
        if description is not None:
            update_fields["description"] = description
        if type is not None:
            update_fields["type"] = type
        if difficulty is not None:
            update_fields["difficulty"] = difficulty
        if status is not None:
            update_fields["status"] = status
        if url is not None:
            update_fields["url"] = url

        evaluation_collection.update_one({"_id": ObjectId(id)}, {"$set": update_fields})
        updated_evaluation = evaluation_collection.find_one({"_id": ObjectId(id)})
        return serialize_evaluation(updated_evaluation)

    @strawberry.mutation
    def delete_evaluation(self, id: str) -> Optional[Evaluation]:
        evaluation = evaluation_collection.find_one({"_id": ObjectId(id)})  # 🔹 Buscar antes de eliminar
        if not evaluation:
            return None  # 🔹 Si no existe, devolver `None`

        evaluation_collection.delete_one({"_id": ObjectId(id)})  # 🔹 Eliminar evaluación
        return serialize_evaluation(evaluation)  # 🔹 Retornar la evaluación eliminada

schema = strawberry.Schema(query=Query, mutation=Mutation)
