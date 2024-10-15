from rest_framework import status  # noqa
from rest_framework.response import Response


# Exemple de réponse lorsque tout se passe bien
def success_response(message, data, response_code):
    return Response(
        {
            "succes": "00",  # Indique que l'opération a réussi
            "response_code": response_code,  # Code de réponse HTTP (ex: 200)
            "response_message": message,  # Message de succès
            "data": data,  # Les données à renvoyer (ex: informations utilisateur, token)
        },
        status=response_code,
    )


# Exemple de réponse lorsque quelque chose échoue
def error_response(message, errors, response_code):
    return Response(
        {
            "succes": "01",  # Indique que l'opération a échoué
            "response_code": response_code,  # Code de réponse HTTP (ex: 400, 401, 500)
            "response_message": message,  # Message d'erreur
            "errors": errors,  # Pas de données dans le cas d'une erreur
        },
        status=response_code,
    )
