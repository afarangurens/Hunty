
def usuarioEntity(item) -> dict:
    return {
        "UserId": str(item["_id"]),
        "FirstName": item["FirstName"],
        "LastName": item["LastName"],
        "Email": item["Email"],
        "YearsPreviousExperience": item["YearsPreviousExperience"],
        "Skills": item["Skills"]
    }

def usuariosEntity(entity) -> list:

    return [usuarioEntity(item) for item in entity]

