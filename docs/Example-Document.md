---
title: "User Authentication API Spec"
para: Project
tags: [python, fastapi, jwt, security]
---

# User Authentication API Spec

This document outlines the planned architecture for the new user authentication microservice.

## Core Requirements
* Must transition from the legacy session-based middleware to stateless JWTs.
* Token signing will use `RS256` with asymmetric keys.
* Needs to handle rate limiting at the gateway level before hitting the DB.

## Token Payload Structure
The JWT payload should remain lightweight to keep header sizes down.

```json
{
  "sub": "1234567890",
  "name": "Jane Doe",
  "role": "admin",
  "iat": 1716300000,
  "exp": 1716303600
}
```

## Open Questions for AI Review
1. What is the best way to handle token revocation without introducing a heavy stateful database lookup on every single request?
2. Should we implement refresh tokens immediately, or wait for the V2 release?