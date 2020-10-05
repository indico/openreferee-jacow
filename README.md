# OpenReferee

## OpenReferee Reference Server

This is a reference implementation of the OpenReferee Specification.

### Development setup
```
pip install -e '.[dev]'
npm ci
```

### Running Test Server
```
flask run -p 12345
```

### Consulting API Docs
```
npm run api-docs
```

Docs available at http://localhost:5000

### Running Swagger UI (Docker required)

First, let's run the test server with CORS enabled
```
FLASK_ENABLE_CORS=1 flask run -p 12345
```

Then, run the Swagger UI:
```
npm run swagger-ui
```

Swagger UI available at http://localhost:5001
