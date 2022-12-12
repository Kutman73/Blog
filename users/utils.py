
def get_user_from_request(request):
    return request.user if not request.user.is_anonymous else None
