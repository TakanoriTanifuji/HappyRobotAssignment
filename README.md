# HappyRobotAPI

## API Endpoints

### Get Carrier Information
GET /carrier/{mc_number}

### Get Load Details
GET /loads/{reference_number}

## Authentication
All endpoints require API key authentication. Include "X-API-Key: secret_key" in the request header.