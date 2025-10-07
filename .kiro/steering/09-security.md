---
inclusion: always
---

# Security

1. **Server-Side Authority:** Keep sensitive logic, validation, and data manipulation strictly on the server-side. Use secure API endpoints.
2. **Input Sanitization/Validation:** Always sanitize and validate user input on the server-side.
3. **Dependency Awareness:** Be mindful of the security implications of adding or updating dependencies.
4. **Credentials Management:** Never hardcode secrets or credentials in the codebase. Use environment variables or a secure secrets management solution.
