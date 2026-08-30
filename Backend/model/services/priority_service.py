def calculate_priority(fill_percentage):

    if fill_percentage >= 90:

        return {
            "status": "CRITICAL",
            "priority": 1,
            "collection_required": True
        }

    elif fill_percentage >= 75:

        return {
            "status": "HIGH",
            "priority": 2,
            "collection_required": True
        }

    elif fill_percentage >= 50:

        return {
            "status": "MEDIUM",
            "priority": 3,
            "collection_required": False
        }

    else:

        return {
            "status": "LOW",
            "priority": 4,
            "collection_required": False
        }