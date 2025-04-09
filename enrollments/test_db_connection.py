from db.database import enrollment_collection

def test_connection():
    try:
        count = enrollment_collection.count_documents({})
        print(f"Conexión exitosa. Documentos en enrollments: {count}")
    except Exception as e:
        print(f"Error de conexión: {e}")

test_connection()
