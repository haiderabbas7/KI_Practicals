
def get_node(name, node_list):
    """
    Sucht in der node_list nach dem Node mit name und gibt diesen zurück wenn gefunden
    Wenn nicht gefunden, gibt None zurück (basically der Nullptr aus Python)
    IN DER VORLAGE WURDE HIER -1 ZURÜCKGEGEBEN
    """
    return next((i for i in node_list if i.name == name), None)
