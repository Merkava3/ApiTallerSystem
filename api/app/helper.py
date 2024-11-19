def remove_empty(data, many):
    """Elimina campos vacíos en la serialización."""
    if many:
        return [item for item in data if item]
    return data
