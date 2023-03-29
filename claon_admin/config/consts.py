from pytz import timezone

from claon_admin.config.config import config

TIME_ZONE_KST = timezone("Asia/Seoul")

KOR_BEGIN_CODE = 0xAC00
KOR_END_CODE = 0xD7AF

SESSION_SECRET_KEY = config.get("SESSION", "SECRET_KEY")

AWS_ACCESS_KEY_ID = config.get("AWS", "AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config.get("AWS", "AWS_SECRET_ACCESS_KEY")
REGION_NAME = config.get("AWS", "REGION_NAME")

BUCKET = config.get("S3", "BUCKET")

# JWT
ALGORITHM = "HS256"
JWT_SECRET_KEY = '2e9ab9a49d4def94b9b8859becdc35269c732ba73fa37f71f7c2804242cf9d51'
JWT_REFRESH_SECRET_KEY = '87a6cd538d569a2af646bb70ccbfc2362481848abbca1f9b48080fd275c22d13'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
