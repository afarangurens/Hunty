
def vacanteEntity(item) -> dict:
    return {
        "VacancyId": str(item["_id"]),
        "PositionName": item["PositionName"],
        "CompanyName": item["CompanyName"],
        "Salary": item["Salary"],
        "VacancyLink": item["VacancyLink"],
        "RequiredSkills": item["RequiredSkills"],
        "active": item["active"]
    }

def vacantesEntity(entity) -> list:

    return [vacanteEntity(item) for item in entity]