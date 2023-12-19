import uuid

import boto3

from pyramid.response import Response
from pyramid.view import view_config

from storage.users_db import UsersDB
from entities import User
from utils import INTERNAL_ERROR, USER_IMAGE, AVAILABLE_PARAMETERS, USER_PROFILE_IMAGE_URL, UsersError

S3_BUCKET = 'image.sharing.platform'


@view_config(
    route_name='homepage',
    request_method='GET'
)
def get_homepage(request):
    return Response('Image sharing app Homepage')


@view_config(
    route_name='new_user_registration',
    request_method='POST'
)
def register(request):
    print('register started', flush=True)
    params = request.params

    check, checked_params, missing_params = check_params(params, False)
    if not check:
        err = UsersError.MISSING_PARAMS + ' {}'.format(missing_params)
        return Response(json_body={"error": err, "user_id": None}, status=400)

    user = User(checked_params)

    image = checked_params.get(USER_IMAGE)
    if image:
        image_file = image.file

        image_name = '{username}_{id}'.format(username=user.username, id=uuid.uuid4())
        image_url = upload_image(image_file, image_name)

        user.set_image_url(image_url)

    err, user_id = UsersDB().add_user(user)

    status_code = 500 if INTERNAL_ERROR in err else 200
    resp_usr_id = str(user_id) if user_id else None

    return Response(json_body={"error": err, "user_id": resp_usr_id}, status=status_code)


@view_config(
    # route_name='get_user',
    request_method='GET',
)
def get_user(request):
    try:
        print(request.json_body)
    except:
        print('no json body')
    user_id = request.params.get('id')
    if not user_id:
        return Response(status=400)

    err, user = UsersDB().get_user(user_id)
    if err:
        return Response(json_body={"error": err, "user_id": None}, status=400)

    return Response(json_body=user.to_json(), status=200)


@view_config(
    route_name='update_user',
    request_method='PUT'
)
def update_user(request):
    user_id = request.params.get('id')
    if not user_id:
        return Response(status=400)

    params = request.params
    check, checked_params, _ = check_params(params, True)

    if not check:
        err = UsersError.EMPTY_LIST_OF_PARAMS
        return Response(json_body={"error": err, "user_id": None}, status=400)
    err, user_id = UsersDB().update_user(user_id, checked_params)

    return create_response(err, user_id)

@view_config(
    route_name='delete_user',
    request_method='DELETE'
)
def delete_user(request):
    user_id = request.params.get('id')
    if not user_id:
        return Response(status=400)

    err, user_id = UsersDB().delete_user(user_id)

    return create_response(err, user_id)


def check_params(params, check_for_update=False):
    checked_params = {k: v for k, v in params.items() if str(k) in AVAILABLE_PARAMETERS}

    if check_for_update:
        return bool(checked_params), checked_params, set()

    required_params = set(AVAILABLE_PARAMETERS).difference({USER_PROFILE_IMAGE_URL})

    missing_params = required_params.difference(set(checked_params.keys()))

    return not bool(missing_params), checked_params, missing_params


def upload_image(image_file, file_name):
    s3_client = boto3.client('s3')
    s3_client.upload_fileobj(image_file, S3_BUCKET, file_name)
    file_url = '%s/%s/%s' % (s3_client.meta.endpoint_url, S3_BUCKET, file_name)

    return file_url


def create_response(err, user_id):
    status_code = 500 if INTERNAL_ERROR in err else 200
    resp_usr_id = str(user_id) if user_id else None

    return Response(json_body={"error": err, "user_id": resp_usr_id},
                    status=status_code)
