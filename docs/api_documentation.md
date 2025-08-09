# AI Interview Platform API Documentation

This document provides a comprehensive overview of the AI Interview Platform API endpoints.

## Base URL
`/api/v1`

## Authentication

### Register a new user
`POST /auth/register`

Registers a new user in the system.

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "newuser",
  "full_name": "New User",
  "password": "securepassword"
}
```

**Response (200 OK):**
```json
{
  "id": "b1a2...",
  "email": "user@example.com",
  "username": "newuser",
  "full_name": "New User",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2023-01-01T12:00:00.000Z"
}
```

**Error Responses:**
*   `400 Bad Request`: If email or username already exists.

### Login user and return access token
`POST /auth/login`

Authenticates a user with email and password, returning an access token.

**Request Body (Form Data):**
```
username: user@example.com
password: securepassword
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1Ni...",
  "token_type": "bearer"
}
```

**Error Responses:**
*   `401 Unauthorized`: Incorrect email or password.

### Logout user
`POST /auth/logout`

Logs out the current user by invalidating their access token. The token is added to a blocklist.

**Headers:**
`Authorization: Bearer <access_token>`

**Response (200 OK):**
```json
{
  "message": "Successfully logged out"
}
```

**Error Responses:**
*   `401 Unauthorized`: Invalid token.

> Note: Current user profile is available via `/users/me`.

## Users

### Get current user profile
`GET /users/me`

Retrieves the profile information of the currently authenticated user. (Alias for `/auth/me`)

**Headers:**
`Authorization: Bearer <access_token>`

**Response (200 OK):**
```json
{
  "id": "b1a2...",
  "email": "user@example.com",
  "username": "newuser",
  "full_name": "New User",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2023-01-01T12:00:00.000Z"
}
```

**Error Responses:**
*   `401 Unauthorized`: Not authenticated.
*   `400 Bad Request`: Inactive user.

### Update current user profile
`PUT /users/me`

Updates the profile information of the currently authenticated user.

**Headers:**
`Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "full_name": "Updated Name",
  "is_active": true
}
```
*Note: `is_active` can only be updated by a superuser.*

**Response (200 OK):**
```json
{
  "id": "b1a2...",
  "email": "user@example.com",
  "username": "newuser",
  "full_name": "Updated Name",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2023-01-01T12:00:00.000Z"
}
```

**Error Responses:**
*   `401 Unauthorized`: Not authenticated.
*   `400 Bad Request`: Inactive user.

## API Keys

### Create new API key
`POST /api-keys/`

Creates a new API key for the current user. There is a limit on the number of active API keys per user.

**Headers:**
`Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "name": "My Integration Key"
}
```

**Response (200 OK):**
```json
{
  "id": "key_123...",
  "name": "My Integration Key",
  "key": "pk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "secret": "sk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "is_active": true,
  "usage_count": 0,
  "created_at": "2023-01-01T12:00:00.000Z",
  "last_used_at": null
}
```

**Error Responses:**
*   `401 Unauthorized`: Not authenticated.
*   `400 Bad Request`: Maximum number of API keys reached.

### List user's API keys
`GET /api-keys/`

Lists all API keys belonging to the current user.

**Headers:**
`Authorization: Bearer <access_token>`

**Response (200 OK):**
```json
[
  {
    "id": "key_123...",
    "name": "My Integration Key",
    "key": "pk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "is_active": true,
    "usage_count": 10,
    "created_at": "2023-01-01T12:00:00.000Z",
    "last_used_at": "2023-01-02T10:00:00.000Z"
  }
]
```

**Error Responses:**
*   `401 Unauthorized`: Not authenticated.

### Deactivate API key
`DELETE /api-keys/{key_id}`

Deactivates a specific API key by its ID.

**Headers:**
`Authorization: Bearer <access_token>`

**Path Parameters:**
`key_id`: The ID of the API key to deactivate (string UUID).

**Response (200 OK):**
```json
{
  "message": "API key deactivated successfully"
}
```

**Error Responses:**
*   `401 Unauthorized`: Not authenticated.
*   `404 Not Found`: API key not found or does not belong to the user.

## Interviews

### Create new interview session
`POST /interviews/`

Creates a new interview session and a corresponding LiveKit room.

**Headers:**
`Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "title": "Software Engineer Interview",
  "candidate_name": "Jane Doe",
  "candidate_email": "jane.doe@example.com",
  "position": "Software Engineer",
  "interview_config": {
    "duration": 60,
    "difficulty": "medium"
  },
  "scheduled_at": "2023-08-15T10:00:00Z"
}
```

**Response (200 OK):**
```json
{
  "id": "a3b4...",
  "title": "Software Engineer Interview",
  "candidate_name": "Jane Doe",
  "candidate_email": "jane.doe@example.com",
  "position": "Software Engineer",
  "status": "scheduled",
  "room_name": "interview-abcdef123456",
  "technical_score": 0,
  "behavioral_score": 0,
  "created_at": "2023-08-10T14:30:00.000Z",
  "creator_id": "b1a2..."
}
```

**Error Responses:**
*   `401 Unauthorized`: Not authenticated.

### List user's interviews
`GET /interviews/`

Lists all interview sessions created by the current user.

**Headers:**
`Authorization: Bearer <access_token>`

**Query Parameters:**
*   `skip`: (Optional) Number of records to skip (for pagination). Default: 0.
*   `limit`: (Optional) Maximum number of records to return. Default: 100.

**Response (200 OK):**
```json
[
  {
    "id": "a3b4...",
    "title": "Software Engineer Interview",
    "candidate_name": "Jane Doe",
    "candidate_email": "jane.doe@example.com",
    "position": "Software Engineer",
    "status": "scheduled",
    "room_name": "interview-abcdef123456",
    "technical_score": 0,
    "behavioral_score": 0,
    "created_at": "2023-08-10T14:30:00.000Z",
    "creator_id": "b1a2..."
  }
]
```

**Error Responses:**
*   `401 Unauthorized`: Not authenticated.

### Get interview details
`GET /interviews/{interview_id}`

Retrieves the details of a specific interview session.

**Headers:**
`Authorization: Bearer <access_token>`

**Path Parameters:**
`interview_id`: The ID of the interview to retrieve (string UUID).

**Response (200 OK):**
```json
{
  "id": "a3b4...",
  "title": "Software Engineer Interview",
  "candidate_name": "Jane Doe",
  "candidate_email": "jane.doe@example.com",
  "position": "Software Engineer",
  "status": "scheduled",
  "room_name": "interview-abcdef123456",
  "technical_score": 0,
  "behavioral_score": 0,
  "created_at": "2023-08-10T14:30:00.000Z",
  "creator_id": "b1a2..."
}
```

**Error Responses:**
*   `401 Unauthorized`: Not authenticated.
*   `403 Forbidden`: Not enough permissions (if not creator or superuser).
*   `404 Not Found`: Interview not found.

### Update interview
`PUT /interviews/{interview_id}`

Updates the details of an existing interview session.

**Headers:**
`Authorization: Bearer <access_token>`

**Path Parameters:**
`interview_id`: The ID of the interview to update (string UUID).

**Request Body:**
```json
{
  "title": "Updated Interview Title",
  "status": "completed",
  "technical_score": 85,
  "behavioral_score": 90,
  "overall_feedback": "Excellent candidate."
}
```

**Response (200 OK):**
```json
{
  "id": "a3b4...",
  "title": "Updated Interview Title",
  "candidate_name": "Jane Doe",
  "candidate_email": "jane.doe@example.com",
  "position": "Software Engineer",
  "status": "completed",
  "room_name": "interview-abcdef123456",
  "technical_score": 85,
  "behavioral_score": 90,
  "created_at": "2023-08-10T14:30:00.000Z",
  "creator_id": "b1a2..."
}
```

**Error Responses:**
*   `401 Unauthorized`: Not authenticated.
*   `403 Forbidden`: Not enough permissions (if not creator or superuser).
*   `404 Not Found`: Interview not found.

### Generate LiveKit token for interview participant
`POST /interviews/{interview_id}/token`

Generates a LiveKit token for a participant to join the specified interview's room.

**Headers:**
`Authorization: Bearer <access_token>`

**Path Parameters:**
`interview_id`: The ID of the interview for which to generate a token (string UUID).

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1Ni...",
  "room_name": "interview-abcdef123456",
  "participant_name": "Jane Doe"
}
```

**Error Responses:**
*   `401 Unauthorized`: Not authenticated.
*   `403 Forbidden`: Not enough permissions (if not creator or superuser).
*   `404 Not Found`: Interview not found.

### Create interview via API key (for integrations)
`POST /interviews/api/create`

Creates a new interview session using an API key for authentication. This endpoint is intended for integrations.

**Headers:**
`Authorization: Bearer <api_key>`

**Request Body:**
```json
{
  "title": "Integration Interview",
  "candidate_name": "John Smith",
  "candidate_email": "john.smith@example.com",
  "position": "Data Scientist",
  "interview_config": {
    "duration": 45
  }
}
```

**Response (200 OK):**
```json
{
  "id": 2,
  "title": "Integration Interview",
  "candidate_name": "John Smith",
  "candidate_email": "john.smith@example.com",
  "position": "Data Scientist",
  "status": "pending",
  "room_name": "interview-fedcba987654",
  "technical_score": 0,
  "behavioral_score": 0,
  "created_at": "2023-08-10T15:00:00.000Z",
  "creator_id": 1
}
```

**Error Responses:**
*   `401 Unauthorized`: Invalid or inactive API key.

### Generate interview token via API key
`POST /interviews/api/{interview_id}/token`

Generates a LiveKit token for a participant to join the specified interview's room, using an API key for authentication.

**Headers:**
`Authorization: Bearer <api_key>`

**Path Parameters:**
`interview_id`: The ID of the interview for which to generate a token.

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1Ni...",
  "room_name": "interview-abcdef123456",
  "participant_name": "Jane Doe"
}
```

**Error Responses:**
*   `401 Unauthorized`: Invalid or inactive API key.
*   `404 Not Found`: Interview not found or does not belong to the API key owner.