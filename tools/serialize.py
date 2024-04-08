from datetime import datetime


def serialize_mongo_document(document: dict) -> dict:
    # Check if the document is None
    if not document:
        return {}

    # Convert ObjectId to string (if you decide to include it later) and exclude '_id'
    serialized = {key: value for key, value in document.items() if key != '_id'}

    # Convert datetime fields to string
    for key, value in serialized.items():
        if isinstance(value, datetime):
            # Format can be adjusted as needed
            serialized[key] = value.strftime('%Y-%m-%d %H:%M:%S')

    return serialized
