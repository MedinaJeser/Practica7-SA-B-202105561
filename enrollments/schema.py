import strawberry
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from db.database import enrollment_collection


@strawberry.type
class Enrollment:
    id: str
    user_id: str
    course_id: str
    date: str
    status: str
    progress: float
    final_grade: Optional[float]
    createdAt: str
    updatedAt: str


def serialize_enrollment(enrollment):
    """ Convierte `_id` a `id` en los resultados de MongoDB """
    return Enrollment(
        id=str(enrollment["_id"]),
        user_id=enrollment["user_id"],
        course_id=enrollment["course_id"],
        date=enrollment["date"],
        status=enrollment["status"],
        progress=enrollment["progress"],
        final_grade=enrollment.get("final_grade"),
        createdAt=enrollment["createdAt"],
        updatedAt=enrollment["updatedAt"]
    )


@strawberry.type
class Query:
    @strawberry.field
    def get_enrollments(self) -> List[Enrollment]:
        enrollments = list(enrollment_collection.find())
        return [serialize_enrollment(enroll) for enroll in enrollments]

    @strawberry.field
    def get_enrollment_by_id(self, id: str) -> Optional[Enrollment]:
        enrollment = enrollment_collection.find_one({"_id": ObjectId(id)})
        if not enrollment:
            return None
        return serialize_enrollment(enrollment)


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_enrollment(self, user_id: str, course_id: str, status: str, progress: float, final_grade: Optional[float] = None) -> Enrollment:
        now = datetime.utcnow().isoformat()
        new_enrollment = {
            "user_id": user_id,
            "course_id": course_id,
            "date": now,
            "status": status,
            "progress": progress,
            "final_grade": final_grade,
            "createdAt": now,
            "updatedAt": now
        }
        result = enrollment_collection.insert_one(new_enrollment)
        # 🔹 Agregar manualmente `_id`
        new_enrollment["_id"] = result.inserted_id
        return serialize_enrollment(new_enrollment)

    @strawberry.mutation
    def update_enrollment(self, id: str, status: Optional[str] = None, progress: Optional[float] = None, final_grade: Optional[float] = None) -> Enrollment:
        now = datetime.utcnow().isoformat()
        update_fields = {"updatedAt": now}

        if status is not None:
            update_fields["status"] = status
        if progress is not None:
            update_fields["progress"] = progress
        if final_grade is not None:
            update_fields["final_grade"] = final_grade

        enrollment_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_fields})
        updated_enrollment = enrollment_collection.find_one(
            {"_id": ObjectId(id)})
        return serialize_enrollment(updated_enrollment)

    @strawberry.mutation
    def delete_enrollment(self, id: str) -> Optional[Enrollment]:
        enrollment = enrollment_collection.find_one({"_id": ObjectId(id)})
        if not enrollment:
            return None

        enrollment_collection.delete_one({"_id": ObjectId(id)})
        return serialize_enrollment(enrollment)


schema = strawberry.Schema(query=Query, mutation=Mutation)
