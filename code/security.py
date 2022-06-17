from hmac import compare_digest
from models.user_model import UserModel

def authenticate(username, password):  # used for authentucation purposes
    user = UserModel.find_by_username(username)
    print(f"{user.username} authenticate wala")
    if user and compare_digest(user.password, password):
        print(f"{user.id} authenticate wala")
        return user

def identity(payload): ##Identity function takes in the payload (payload is the contents of the jwt token)
    print(f"{payload} identity wala")
    user_id = payload['identity']  #extract the user id from that payload
    print(f"{user_id} identity wala")
    print(f"{UserModel.find_by_id(user_id)} identity wala")
    return UserModel.find_by_id(user_id)  #retrieve the user which matches this userid