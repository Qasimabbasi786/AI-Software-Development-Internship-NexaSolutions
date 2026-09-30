# Week 4 - Part A: JWT Authentication in ASP.NET Core (Real Implementation)

## 📌 Executive Summary
In Week 3, the application utilized an authentication skeleton with mock tokens and unhashed passwords. Week 4 - Part A transitions this to a production-grade, hardened authentication and authorization subsystem built on **ASP.NET Core 8**, **Entity Framework Core 8**, and **PostgreSQL**.

---

## 🏗️ Architectural Overview & Security Mechanics

```
┌─────────────────┐       1. POST /api/auth/login        ┌────────────────────────────┐
│                 │  { "username", "password": "..." }   │   ASP.NET Core Web API     │
│                 ├─────────────────────────────────────►│  (AuthController.cs)       │
│                 │                                      └─────────────┬──────────────┘
│                 │                                                    │ 2. Query User
│                 │                                                    ▼
│  Client / SPA   │                                      ┌────────────────────────────┐
│ (Angular / Post)│                                      │    PostgreSQL Database     │
│                 │                                      │  (Users: PasswordHash)     │
│                 │                                      └─────────────┬──────────────┘
│                 │                                                    │ 3. Verify Hash
│                 │                                                    ▼ (PBKDF2 HMAC-SHA256)
│                 │       4. Return Signed JWT           ┌────────────────────────────┐
│                 │◄─────────────────────────────────────┤  Token Issuer (HMAC-SHA256)│
│                 │   { "token": "ey..." }               │  Claims: id, name, role    │
│                 │                                      └────────────────────────────┘
│                 │
│                 │       5. POST /api/books [Bearer Token]
│                 ├─────────────────────────────────────► [ JwtBearerHandler Middleware ]
│                 │                                              │
│                 │                                        Valid? ├── Yes ──► Controller Action
│                 │                                               └── No  ──► 401 Unauthorized
└─────────────────┘
```

---

## 🔑 Core Concepts Mastered

### 1. Cryptographic Password Hashing vs Plaintext
- **One-Way Mathematical Transformation:** Passwords must never be stored in plain text or reversibly encrypted.
- **Salted PBKDF2 with HMAC-SHA256:** Implemented via `Microsoft.AspNetCore.Identity.PasswordHasher<User>`.
  - Automatically generates a unique cryptographically random 128-bit salt per user.
  - Iterates 100,000 times to protect against brute-force and rainbow table attacks.
  - Stored output includes format marker, salt, and hash subkey in a single Base64 string.
- **Verification Flow:** `_passwordHasher.VerifyHashedPassword(user, user.PasswordHash, incomingPassword)` extracts the salt from the stored hash, computes the PBKDF2 hash on the candidate password, and performs a timing-safe byte comparison.

### 2. JSON Web Token (JWT) Anatomy
A JWT consists of three Base64Url-encoded segments separated by dots (`.`):
1. **Header:** Algorithm used (`HS256`) and token type (`JWT`).
2. **Payload (Claims):**
   - `sub`: Subject identifier (`UserId`)
   - `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name`: Username
   - `http://schemas.microsoft.com/ws/2008/06/identity/claims/role`: Role (`Admin` or `User`)
   - `jti`: Unique token GUID for replay prevention
   - `nbf` & `exp`: Not-Before and Expiration Unix timestamps (configured for 120 minutes)
3. **Signature:** Cryptographic verification signature computed with symmetric secret key `HMACSHA256(header + "." + payload, secretKey)`.

### 3. Middleware Pipeline & Precedence
In `Program.cs`, authentication middleware **must execute before** authorization middleware:
```csharp
app.UseAuthentication(); // 1. Validates token signature, unpacks ClaimsPrincipal
app.UseAuthorization();  // 2. Checks [Authorize] policies and [Authorize(Roles = "...")]
```

---

## 🛠️ Step-by-Step Implementation Reference

### 1. Package Installation
Added to `libraryAPI.csproj`:
```bash
& "D:\Software\dotnet\dotnet.exe" add package Microsoft.AspNetCore.Authentication.JwtBearer --version 8.0.8
```

### 2. Secret Configuration in `appsettings.Development.json`
```json
{
  "Jwt": {
    "Key": "NexaSolutions_OriginSoft_SecureKey_2026_JWT_SecretKey_9876543210!",
    "Issuer": "LibraryAPI",
    "Audience": "LibraryAppUsers",
    "ExpiryMinutes": 120
  }
}
```

### 3. Authentication & Swagger Registration in `Program.cs`
Configured symmetric signing key validation, zero clock-skew, and Swagger Bearer authorization definitions:
```csharp
var jwtKey = builder.Configuration["Jwt:Key"] ?? "...";
var keyBytes = Encoding.UTF8.GetBytes(jwtKey);

builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.RequireHttpsMetadata = false;
    options.SaveToken = true;
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuerSigningKey = true,
        IssuerSigningKey = new SymmetricSecurityKey(keyBytes),
        ValidateIssuer = false,
        ValidateAudience = false,
        ClockSkew = TimeSpan.Zero
    };
});

builder.Services.AddAuthorization();
```

### 4. Controller Endpoints & Protection Matrix

| Route | HTTP | Auth Required | Allowed Roles | Description |
| :--- | :--- | :--- | :--- | :--- |
| `/api/auth/register` | `POST` | No (`AllowAnonymous`) | Public | Hashes password with PBKDF2 and creates `User` record |
| `/api/auth/login` | `POST` | No (`AllowAnonymous`) | Public | Verifies hash, returns signed JWT token & claims |
| `/api/books` | `GET` | No (`AllowAnonymous`) | Public | Fetch entire book catalog |
| `/api/books/{id}` | `GET` | No (`AllowAnonymous`) | Public | Fetch book by ID |
| `/api/books` | `POST` | **Yes** (`[Authorize]`) | `User`, `Admin` | Add new book to PostgreSQL catalog |
| `/api/books/{id}` | `PUT` | **Yes** (`[Authorize]`) | `User`, `Admin` | Update existing book entry |
| `/api/books/{id}` | `DELETE`| **Yes** (`[Authorize(Roles = "Admin")]`) | **`Admin` Only** | Deletes book. Regular `User` returns `403 Forbidden` |

---

## 🧪 Testing & Verification Guide

### 1. Start the API
```powershell
cd "Week_04/Week_04_Final_Project/backend"
& "D:\Software\dotnet\dotnet.exe" run
```
Navigate to Swagger UI: `http://localhost:5000/`

### 2. Register Users (Member vs Admin)
- **Register Normal User:**
  - `POST /api/auth/register`
  ```json
  { "username": "sam", "password": "UserPass123!", "role": "User" }
  ```
- **Register Admin User:**
  - `POST /api/auth/register`
  ```json
  { "username": "admin_qasim", "password": "AdminPass123!", "role": "Admin" }
  ```
- **Database Inspection:**
  Open `psql` or pgAdmin on `librarydb_week3`:
  ```sql
  SELECT "UserId", "Username", "Role", "PasswordHash" FROM "Users";
  ```
  *Notice that `PasswordHash` is a long cryptographic string (starting with `AQAAAAIA...`), never the plaintext password.*

### 3. Log In and Retrieve Token
- Call `POST /api/auth/login` with `{"username": "admin_qasim", "password": "AdminPass123!"}`.
- Copy the returned `token` string.

### 4. Decode Token at [jwt.io](https://jwt.io)
- Paste the token into the **Encoded** area.
- Verify payload claims:
  ```json
  {
    "sub": "2",
    "http://schemas.microsoft.com/ws/2008/06/identity/claims/role": "Admin",
    "exp": 1727732400
  }
  ```

### 5. Test Role-Based Protection in Swagger
1. Click the green **Authorize** button at the top of Swagger.
2. Enter: `Bearer <your_token>` and click **Authorize**.
3. Test `POST /api/books` -> Returns `201 Created`.
4. Test `DELETE /api/books/{id}`:
   - When authenticated as `User` -> Returns `403 Forbidden`.
   - When authenticated as `Admin` -> Returns `204 NoContent`.
   - When unauthenticated (logged out / no header) -> Returns `401 Unauthorized`.

---

## 🌿 Git Checkpoint
```bash
git checkout -b feature/jwt-auth-backend
git add .
git commit -m "feat: add JWT authentication with register, login, and role-based authorization"
```
