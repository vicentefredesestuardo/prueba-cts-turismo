def normalize_contestant_fields(attrs):
    """
    Normaliza los campos de entrada de un concursante.
    
    Aplica strip() a campos de texto y normaliza email a minúsculas.
    
    Args:
        attrs (dict): Diccionario con los campos del concursante
        
    Returns:
        dict: Diccionario con campos normalizados
    """
    # Normaliza campos de nombre
    for field in ("first_name", "last_name", "second_last_name"):
        if field in attrs and attrs[field]:
            attrs[field] = attrs[field].strip()
            
    # Normaliza email y teléfono
    if "email" in attrs:
        attrs["email"] = attrs["email"].strip().lower()
    if "phone" in attrs:
        attrs["phone"] = attrs["phone"].strip()
        
    return attrs
