from authx import AuthXConfig, AuthX

authx_config = AuthXConfig()
authx_config.JWT_ALGORITHM = "HS256"
authx_config.JWT_SECRET_KEY = "SECRET_KEY"
authx_config.JWT_ACCESS_COOKIE_NAME = "Authorization"
authx_config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=authx_config)
