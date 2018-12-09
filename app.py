from chalice import Chalice, Response
from chalice import BadRequestError, ConflictError, NotFoundError

from chalicelib.services import create_new_user, verify_user_code, delete_user

app = Chalice(app_name="lambdatotp")


@app.route("/", methods=["POST"])
def create_user():

    user_id = app.current_request.json_body.get("user")
    if not user_id:
        raise BadRequestError("No user found in the request body")

    try:
        response = create_new_user(user_id)
    except ValueError:
        raise ConflictError("User already exists")

    return Response(body=response, status_code=201)


@app.route("/verify", methods=["GET"])
def verify():

    query_params = app.current_request.query_params
    user = query_params and query_params.get("user")
    code = query_params and query_params.get("code")

    if not code or not user:
        raise BadRequestError("No code or user found in the query string")

    try:
        response = verify_user_code(user, code)
        return Response(body=response, status_code=200)
    except ValueError:
        raise NotFoundError("User not found")


@app.route("/{user_id}", methods=["DELETE"])
def delete(user_id):
    try:
        delete_user(user_id)
    except ValueError:
        raise NotFoundError("User not found")
    else:
        return Response(body="", status_code=204)
