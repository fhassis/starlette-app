
CERT_FOLDER="certificates"

KEY_FILE="$CERT_FOLDER/key.pem"
CERT_FILE="$CERT_FOLDER/cert.pem"
DAYS=365

COUNTRY="CT"
STATE="ST"
CITY="YOUR CITY"
EMAIL="tbd@gmail.com"
ORGANIZATION="YOUR ORGANIZATION"
ORGANIZATION_UNIT="NA"
COMMON_NAME="APP_NAME"

# create directory
mkdir $CERT_FOLDER

# openssl req -nodes -x509 -newkey rsa:4096 -keyout $KEY_FILE -out $CERT_FILE -days $DAYS -subj "/C=$COUNTRY/ST=$STATE/L=$CITY/O=$ORGANIZATION/OU=$ORGANIZATION_UNIT/CN=$COMMON_NAME/emailAddress=$EMAIL"
openssl req -nodes -x509 -newkey rsa:4096 -keyout $KEY_FILE -out $CERT_FILE -days $DAYS