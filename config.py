class Config(object):
	"""
	Common configurations
	"""
	DEBUG = False
	CSRF_ENABLED = True


class DevelopmentConfig(Config):
	"""
	Development configurations
	"""

	DEBUG = True
	SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
	"""
	Production configurations
	"""

	DEBUG = False


class TestingConfig(Config):
	DEBUG = True
	TESTING = True


app_config = {
	'development': DevelopmentConfig,
	'production': ProductionConfig,
	"testing": TestingConfig
}
