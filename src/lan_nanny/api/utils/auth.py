"""
    Cver Api
    Utility Auth

"""
import datetime
from functools import wraps
import logging
import random

from flask import make_response, request, jsonify
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from werkzeug import security

from polite_lib.utils import date_utils

from lan_nanny.api.models.api_key import ApiKey
from lan_nanny.api.models.user import User
from lan_nanny.api.utils import rbac
from lan_nanny.api.utils import glow

SECRET_KEY = glow.general["SECRET_KEY"]


def auth_request(f):
    """Authentication decorator, which gates HTTP routes. This method used to validate user access
    via a JWT.
    @todo: Harden this method, checking for jwt values.
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        data = {
            "message": "",
            "status": "Error"
        }
        if "Token" not in request.headers:
            data["message"] = "Missing token"
            return make_response(jsonify(data), 401)
        token = request.headers["Token"]
        jwt_value = validate_jwt(token)
        if jwt_value:
            # User has valid JWT
            glow.user["user_id"] = jwt_value["user_id"]
            glow.user["org_id"] = jwt_value["org_id"]
            glow.user["role_perms"] = jwt_value["role_perms"]
            user = User()
            if not user.get_by_id(glow.user["user_id"]):
                logging.error("Could not find User ID: %s" % glow.user["user_id"])
                data["message"] = "Could not find User: %s" % glow.user["user_id"]
                return make_response(jsonify(data), 400)
            user.load_meta()
            glow.user["obj"] = user
            logging.info("Authenticated JWT for User ID: %s" % glow.user["user_id"])
            record_last_access_user(glow.user["user_id"])
            # Check if user has access to this resource
            if "role_perms" not in jwt_value:
                data["message"] = "Invalid token"
                return make_response(jsonify(data), 401)
            logging.warning("Removing RBAC check from auth temporarily")
            # @WARN temporarily removing rbac checks
            # if not rbac.check_role_uri_access(jwt_value["role_perms"], request):
            #     msg = "User ID: %s attempted to access a resource they do not have authorization for"
            #     logging.warning(msg % glow.user["user_id"])
            #     data["message"] = "Access Forbidden"
            #     return make_response(jsonify(data), 403)
            return f(*args, **kwargs)
        else:
            logging.warning("Can't verify token")
            return make_response(jsonify({"message": "Invalid token"}), 401)
    return decorator


def validate_jwt(token: str) -> dict:
    """Check that the JWT is valid by checking the token.
    @todo: Update secret-key to be updatable to invalidate tokens.
    """
    try:
        # Decode and verify the JWT using the secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except ExpiredSignatureError:
        # Handle expired token
        data = {
            "message": "Token has expired.",
            "status": "Error"
        }
        make_response(jsonify(data), 412)
        return False
    except InvalidSignatureError:
        # Handle invalid signature
        logging.error("Invalid token signature.")
        return False
    except jwt.exceptions.DecodeError:
        logging.error("Unable to decode token")
        return False


def mint_jwt():
    """Mint a JWT token for a User with the given expiration time.
    @todo: Harden this with more failure scenarios around shitty input data.
    """
    if not glow.user:
        data = {
            "status": "Error",
            "message": "Couldnt find user"
        }
        return make_response(jsonify(data), 503)
    role_perms = rbac.get_perms_by_role_id(glow.user["role_id"])
    expiration_minutes = int(glow.general["JWT_EXPIRE_MINUTES"])
    payload = {
        "user_id": glow.user["user_id"],
        "role_perms": role_perms,
        "org_id": glow.user["org_id"],
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    }

    # Create the JWT using the payload and secret key
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    # logging.info("Minted JWT token for user_id: %s" % user_id)

    return jwt_token


def record_last_access(user: User, api_key: ApiKey) -> bool:
    """Records the User and ApiKey's last access."""
    if not glow.user:
        data = {
            "status": "Error",
            "message": "Couldnt find user"
        }
        return make_response(jsonify(data), 503)
    logging.debug("Recording User/ApiKey last access")

    user.last_access = date_utils.now()
    user.save()

    api_key.last_access = date_utils.now()
    api_key.save()
    logging.debug("Updating apikey last access.")

    return True


def record_last_access_user(user_id: int) -> bool:
    """Update the users last access record."""
    sql = """
        UPDATE users
        SET last_access = %s
        WHERE id = %s;
    """
    glow.db["cursor"].execute(sql, (date_utils.now(), user_id))
    glow.db["conn"].commit()
    return True


def verify_api_key(client_id: str, raw_api_key: str) -> bool:
    """"Authenticate a login request, taking the client_id and api_key looking for a match."""
    api_key = ApiKey()

    if not client_id or not raw_api_key:
        return False

    # Check for a matching Client ID
    if not api_key.get_by_client_id(client_id):
        logging.info("Could not find an ApiKey with client_id: %s" % client_id)
        return False

    # Check that the Api Key matches
    if not security.check_password_hash(api_key.key, raw_api_key):
        logging.warning("Api key doesn't match client_id: %s" % client_id)
        return False

    # Check Api Key expiration
    if api_key.expiration_date:
        if date_utils.now() > api_key.expiration_date:
            logging.warning("Key has expired")
            return False

    logging.info("Verified Api Key: %s" % api_key)
    data = {
        "api_key": api_key,
        "user_id": api_key.user_id
    }
    return data


def generate_client_id() -> str:
    """Generates a client id to be used in api authentication."""
    length = 10
    characters = "abcdefghijklmnopqrstuvwxyz1234567890"
    client_id = ""
    for index in range(length):
        client_id = client_id + random.choice(characters)
    return client_id


def generate_api_key() -> str:
    """Creates an api-key."""
    password_length = 19
    characters = "abcdefghijklmnopqrstuvwxyz1234567890"
    api_key = ""
    for index in range(password_length):
        api_key = api_key + random.choice(characters)
    api_key = "%s-%s-%s-%s" % (
        api_key[:4],
        api_key[5:9],
        api_key[10:14],
        api_key[15:])
    return api_key


def generate_hash(password: str) -> str:
    """Generate a password hash from a string"""
    return security.generate_password_hash(password, method="pbkdf2:sha256")


# End File: cver/src/api/utils/auth.py
