# AllDay DJ FastAPI

The FastAPI with Firestore implementation of the AllDay DJ backend.

## Firebase

You may need to refresh the environment variables if it doesn't load:

    $env:FIREBASE_CREDENTIALS="/path/to/file.json"
    $env:ALLDAYDJ_BUCKET="addj-test-bucket"
    $env:ALLDADYJ_TOPIC_VALIDATE="validate-audio"

## Testing

Testing the backend API can be done with a call to:

    pytest

## Search

To allow the generation of search terms to ignore stop words, NLTK must have collection of stopwords for the language. Downloads can be triggered from the CLI:

    python -m nltk.downloader stopwords

## Secret key for authentication

An elliptic curve key is used for signing JWT tokens. To generate said key:

    openssl ecparam -genkey -name secp521r1 -noout -out secret.key