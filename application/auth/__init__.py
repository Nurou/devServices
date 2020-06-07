from application import current_user, login_manager
from functools import wraps
  
def login_required(_func=None, *, role="ANY"):
  def wrapper(func):
      @wraps(func)
      def decorated_view(*args, **kwargs):
          if not (current_user and current_user.is_authenticated):
              return login_manager.unauthorized()

          unauthorized = False

          if role != "ANY":
              unauthorized = True
              
              user_role = current_user.role.name
              
              if user_role == role:
                  unauthorized = False
          if unauthorized:
              return login_manager.unauthorized()

          return func(*args, **kwargs)

      return decorated_view
      wrapper.__name__ = func.__name__

  return wrapper if _func is None else wrapper(_func)
  