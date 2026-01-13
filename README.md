# FastAPI CRUD Application

A production-ready FastAPI application with JWT authentication, MySQL database, and Firebase integration support. Built with clean MVC architecture, full type safety, and async/await patterns.

## Features

- **Modern FastAPI** - Fast, modern web framework with automatic API documentation
- **JWT Authentication** - Secure token-based authentication with access and refresh tokens
- **SQLAlchemy 2.0** - Async ORM with full type safety using `Mapped` annotations
- **Alembic Migrations** - Database schema version control
- **Docker Ready** - Containerized with Docker Compose
- **Firebase Support** - Ready for Firebase authentication integration
- **Clean Architecture** - MVC pattern with Repository, Service, and Controller layers
- **Auto Documentation** - Interactive API docs with Swagger UI and ReDoc
- **Type Safe** - 100% type hints for IDE support and static analysis

## Quick Start

### Using Docker (Recommended)

1. **Clone and setup**
```bash
git clone <repository-url>
cd CapstoneProjectFastAPI2
cp .env.example .env
```

2. **Start services**
```bash
docker-compose up -d
```

3. **Run migrations**
```bash
docker-compose exec app alembic upgrade head
```

4. **Access the application**
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- phpMyAdmin: http://localhost:8080

### Manual Installation

#### Step 1: Prerequisites
Ensure you have the following installed:
- Python 3.8+ (Python 3.13 recommended)
- pip (Python package installer)
- MySQL 8.0+ or MariaDB 10.5+

#### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows (Command Prompt):
venv\Scripts\activate.bat

# On Windows (PowerShell):
venv\Scripts\Activate.ps1
```

#### Step 3: Install All Required Libraries

**Option A: Install from requirements.txt (Recommended)**
```bash
pip install -r requirements.txt
```

**Option B: Install libraries individually**
```bash
# Core Framework
pip install fastapi==0.128.0
pip install uvicorn[standard]==0.40.0

# Database
pip install sqlalchemy==2.0.45
pip install aiomysql==0.3.2
pip install pymysql==1.1.2
pip install alembic==1.18.0

# Authentication & Security
pip install python-jose[cryptography]==3.5.0
pip install passlib[bcrypt]==1.7.4
pip install bcrypt==4.0.1
pip install cryptography==46.0.3

# Data Validation
pip install pydantic==2.12.5
pip install pydantic-settings==2.12.0
pip install email-validator==2.2.0

# Utilities
pip install python-dotenv==1.2.1
pip install python-multipart==0.0.21
pip install aiofiles==25.1.0
pip install jinja2==3.1.6

# Optional: Firebase Authentication
pip install firebase-admin==6.5.0
```

**Library Purpose Breakdown:**

| Library | Version | Purpose |
|---------|---------|---------|
| **fastapi** | 0.128.0 | Modern web framework for building APIs |
| **uvicorn** | 0.40.0 | ASGI server to run FastAPI application |
| **sqlalchemy** | 2.0.45 | ORM for database operations |
| **aiomysql** | 0.3.2 | Async MySQL driver for SQLAlchemy |
| **pymysql** | 1.1.2 | Pure Python MySQL client |
| **alembic** | 1.18.0 | Database migration tool |
| **python-jose** | 3.5.0 | JWT token creation and validation |
| **passlib** | 1.7.4 | Password hashing library |
| **bcrypt** | 4.0.1 | Secure password hashing algorithm |
| **pydantic** | 2.12.5 | Data validation using Python type hints |
| **pydantic-settings** | 2.12.0 | Settings management with Pydantic |
| **email-validator** | 2.2.0 | Email address validation |
| **python-dotenv** | 1.2.1 | Read environment variables from .env file |
| **python-multipart** | 0.0.21 | Multipart form data parsing |
| **cryptography** | 46.0.3 | Cryptographic operations |

#### Step 4: Setup Database
```sql
-- Connect to MySQL as root
mysql -u root -p

-- Create database
CREATE DATABASE fastapi_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user
CREATE USER 'fastapi_user'@'localhost' IDENTIFIED BY 'your_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON fastapi_db.* TO 'fastapi_user'@'localhost';

-- Apply privileges
FLUSH PRIVILEGES;

-- Verify
SHOW DATABASES;
SELECT user, host FROM mysql.user WHERE user = 'fastapi_user';

-- Exit MySQL
EXIT;
```

#### Step 5: Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
# On Linux/Mac:
nano .env
# or
vim .env

# On Windows:
notepad .env
```

Update the following variables in `.env`:
```bash
DATABASE_URL=mysql+aiomysql://fastapi_user:your_password@localhost:3306/fastapi_db
DB_USER=fastapi_user
DB_PASSWORD=your_password
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
```

#### Step 6: Initialize Database Migrations
```bash
# Initialize Alembic (already done in this project)
# alembic init database/migrations

# Generate initial migration
alembic revision --autogenerate -m "Initial migration - create users table"

# Apply migrations
alembic upgrade head

# Verify migration
alembic current
```

#### Step 7: Start Development Server
```bash
# Start with auto-reload (development)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or start without reload (production-like)
uvicorn main:app --host 0.0.0.0 --port 8000

# Start with custom workers
uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/login` | ❌ | Login with email/password |
| POST | `/api/auth/refresh` | ❌ | Refresh access token |

### Users

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/users` | ❌ | Create new user (register) |
| GET | `/api/users/me` | ✅ | Get current user profile |
| GET | `/api/users/{id}` | ✅ | Get user by ID |
| GET | `/api/users` | 👑 | Get all users (superuser only) |
| PATCH | `/api/users/{id}` | ✅ | Update user (own or superuser) |
| DELETE | `/api/users/{id}` | 👑 | Delete user (superuser only) |

**Legend**: ❌ None | ✅ JWT Required | 👑 Superuser Required

## Usage Examples

### Register a new user
```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "securepass123",
    "full_name": "John Doe"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get current user profile
```bash
curl -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Update user profile
```bash
curl -X PATCH http://localhost:8000/api/users/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Updated Name"
  }'
```

## Project Structure

```
CapstoneProjectFastAPI2/
├── app/
│   ├── models/              # Database models (SQLAlchemy)
│   │   ├── BaseModel.py     # Base model with common fields
│   │   └── User.py          # User model
│   ├── schemas/             # Request/response schemas (Pydantic)
│   │   ├── user_schema.py   # User schemas
│   │   └── auth_schema.py   # Auth schemas
│   ├── repositories/        # Data access layer
│   │   ├── BaseRepository.py
│   │   └── UserRepository.py
│   ├── services/            # Business logic
│   │   ├── UserService.py
│   │   └── AuthService.py
│   ├── controllers/         # HTTP handlers
│   │   ├── UserController.py
│   │   └── AuthController.py
│   ├── routes/              # Route definitions
│   │   ├── user_routes.py
│   │   ├── auth_routes.py
│   │   └── firebase_routes.py
│   ├── utils/               # Utilities
│   │   ├── security.py      # Password hashing, JWT
│   │   ├── dependencies.py  # Auth dependencies
│   │   └── firebase_auth.py # Firebase integration
│   └── middleware/          # Middleware
│       └── cors.py          # CORS configuration
├── config/
│   ├── settings.py          # App configuration
│   └── database.py          # Database setup
├── database/
│   └── migrations/          # Alembic migrations
├── main.py                  # Application entry point
├── .env                     # Environment variables
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── docker-compose.yml       # Docker configuration
```

## Architecture

The application follows a clean MVC architecture:

```
Request → Route → Controller → Service → Repository → Database
                     ↓
                 Validation (Pydantic)
                     ↓
                 Authorization (Dependencies)
```

### Layers

1. **Routes** - HTTP endpoint definitions
2. **Controllers** - Request/response handling
3. **Services** - Business logic
4. **Repositories** - Database operations
5. **Models** - Database tables (SQLAlchemy)
6. **Schemas** - Validation (Pydantic)

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Application
APP_NAME=FastAPI Application
APP_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=mysql+aiomysql://fastapi_user:password@db:3306/fastapi_db
DB_HOST=db
DB_PORT=3306
DB_NAME=fastapi_db
DB_USER=fastapi_user
DB_PASSWORD=your-password

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Firebase (Optional)
FIREBASE_CREDENTIALS_PATH=./config/firebase-credentials.json
```

## Database Migrations

### Create migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

## Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Rebuild
docker-compose up -d --build

# Reset database (warning: deletes all data)
docker-compose down -v
```

## Complete CLI Commands Reference

### Quick Command Reference

Most commonly used commands for this project:

| Task | Command |
|------|---------|
| **Start development server** | `uvicorn main:app --reload` |
| **Start with Docker** | `docker-compose up -d` |
| **View Docker logs** | `docker-compose logs -f app` |
| **Stop Docker** | `docker-compose down` |
| **Install dependencies** | `pip install -r requirements.txt` |
| **Create migration** | `alembic revision --autogenerate -m "message"` |
| **Apply migrations** | `alembic upgrade head` |
| **Rollback migration** | `alembic downgrade -1` |
| **Access MySQL** | `mysql -h localhost -P 3306 -u fastapi_user -p` |
| **View API docs** | http://localhost:8000/docs |
| **Test health endpoint** | `curl http://localhost:8000/health` |
| **Activate venv (Linux/Mac)** | `source venv/bin/activate` |
| **Activate venv (Windows)** | `venv\Scripts\activate` |
| **Git status** | `git status` |
| **Git commit** | `git add . && git commit -m "message"` |

---

### Python & Virtual Environment

```bash
# Check Python version
python --version
python3 --version

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate              # Linux/Mac
venv\Scripts\activate                 # Windows CMD
venv\Scripts\Activate.ps1             # Windows PowerShell

# Deactivate virtual environment
deactivate

# Check installed packages
pip list
pip freeze

# Upgrade pip
pip install --upgrade pip

# Install specific package version
pip install package_name==version

# Uninstall package
pip uninstall package_name

# Show package details
pip show package_name
```

### Package Management

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Generate requirements.txt from current environment
pip freeze > requirements.txt

# Update all packages (be careful!)
pip list --outdated
pip install --upgrade package_name

# Install with extras
pip install "uvicorn[standard]"
pip install "passlib[bcrypt]"
pip install "python-jose[cryptography]"

# Clean pip cache
pip cache purge
```

### Database Operations (MySQL/MariaDB)

```bash
# Connect to MySQL
mysql -u root -p
mysql -h localhost -P 3306 -u fastapi_user -p fastapi_db

# Execute SQL file
mysql -u root -p < script.sql

# Export database
mysqldump -u root -p fastapi_db > backup.sql

# Import database
mysql -u root -p fastapi_db < backup.sql

# Show databases
mysql -u root -p -e "SHOW DATABASES;"

# Show tables
mysql -u root -p fastapi_db -e "SHOW TABLES;"

# Drop database (careful!)
mysql -u root -p -e "DROP DATABASE fastapi_db;"
```

### Alembic Migration Commands

```bash
# Initialize Alembic (first time only)
alembic init database/migrations

# Create new migration (auto-generate from models)
alembic revision --autogenerate -m "Description of changes"

# Create empty migration
alembic revision -m "Description of changes"

# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade <revision_id>

# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>

# Rollback all migrations
alembic downgrade base

# Show current migration version
alembic current

# Show migration history
alembic history

# Show verbose history
alembic history --verbose

# Stamp database without running migrations
alembic stamp head

# Show SQL that would be executed (dry run)
alembic upgrade head --sql

# Merge multiple heads
alembic merge -m "Merge branches" <rev1> <rev2>
```

### Uvicorn Server Commands

```bash
# Basic start
uvicorn main:app

# Development mode with auto-reload
uvicorn main:app --reload

# Specify host and port
uvicorn main:app --host 0.0.0.0 --port 8000

# Production mode with workers
uvicorn main:app --workers 4

# With access log
uvicorn main:app --access-log

# Disable access log (production)
uvicorn main:app --no-access-log

# Use specific event loop
uvicorn main:app --loop uvloop

# Enable SSL
uvicorn main:app --ssl-keyfile key.pem --ssl-certfile cert.pem

# Set log level
uvicorn main:app --log-level debug
uvicorn main:app --log-level info
uvicorn main:app --log-level warning
uvicorn main:app --log-level error

# Combination (typical development)
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level info

# Combination (typical production)
uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000 --no-access-log
```

### Docker & Docker Compose Commands

```bash
# Build images
docker-compose build

# Build without cache
docker-compose build --no-cache

# Start services
docker-compose up

# Start in detached mode
docker-compose up -d

# Start and rebuild
docker-compose up -d --build

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers with volumes
docker-compose down -v

# View running containers
docker-compose ps

# View logs
docker-compose logs

# Follow logs (real-time)
docker-compose logs -f

# Logs for specific service
docker-compose logs -f app
docker-compose logs -f db

# Tail last N lines
docker-compose logs --tail=100 app

# Execute command in running container
docker-compose exec app bash
docker-compose exec app python
docker-compose exec app alembic upgrade head

# Execute command without starting new container
docker-compose run --rm app alembic upgrade head

# Restart services
docker-compose restart

# Restart specific service
docker-compose restart app

# Scale services
docker-compose up -d --scale app=3

# View resource usage
docker-compose top

# Pull latest images
docker-compose pull

# Remove stopped containers
docker-compose rm

# Validate docker-compose.yml
docker-compose config

# Pause services
docker-compose pause

# Unpause services
docker-compose unpause
```

### Docker Direct Commands

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# List images
docker images

# Remove container
docker rm container_id

# Remove image
docker rmi image_id

# Remove unused images
docker image prune

# Remove unused containers
docker container prune

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a

# View logs
docker logs container_id

# Follow logs
docker logs -f container_id

# Execute bash in container
docker exec -it container_id bash

# Copy file from container
docker cp container_id:/path/to/file ./local/path

# Copy file to container
docker cp ./local/file container_id:/path/to/destination

# Inspect container
docker inspect container_id

# View container stats
docker stats

# Export container
docker export container_id > container.tar

# Import container
docker import container.tar
```

### Git Commands (Version Control)

```bash
# Initialize repository
git init

# Check status
git status

# Add files to staging
git add .
git add file_name
git add *.py

# Commit changes
git commit -m "Commit message"

# View commit history
git log
git log --oneline
git log --graph

# Create branch
git branch branch_name

# Switch branch
git checkout branch_name
git switch branch_name

# Create and switch to new branch
git checkout -b branch_name
git switch -c branch_name

# Merge branch
git merge branch_name

# Pull changes
git pull origin main

# Push changes
git push origin main

# Clone repository
git clone <repository_url>

# View remotes
git remote -v

# Add remote
git remote add origin <repository_url>

# Reset changes (dangerous!)
git reset --hard HEAD

# Stash changes
git stash
git stash pop
git stash list

# View differences
git diff
git diff file_name

# Ignore files
echo ".env" >> .gitignore
echo "__pycache__/" >> .gitignore
```

### Testing & Debugging

```bash
# Python interactive shell
python
python -i main.py

# Run Python script
python script.py

# Check syntax without executing
python -m py_compile file.py

# Profile code
python -m cProfile main.py

# Test imports
python -c "import fastapi; print(fastapi.__version__)"

# Check installed package location
python -c "import fastapi; print(fastapi.__file__)"

# Lint code (if you have flake8)
pip install flake8
flake8 app/

# Format code (if you have black)
pip install black
black app/

# Type checking (if you have mypy)
pip install mypy
mypy app/
```

### API Testing Commands (cURL)

```bash
# Health check
curl http://localhost:8000/health

# Create user
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"test","password":"test1234","full_name":"Test User"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test1234"}'

# Get current user (with token)
curl -X GET http://localhost:8000/api/users/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Update user
curl -X PATCH http://localhost:8000/api/users/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"full_name":"Updated Name"}'

# Delete user
curl -X DELETE http://localhost:8000/api/users/1 \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Pretty print JSON response (with jq)
curl http://localhost:8000/api/users/me \
  -H "Authorization: Bearer TOKEN" | jq

# Save response to file
curl http://localhost:8000/api/users/me \
  -H "Authorization: Bearer TOKEN" -o response.json

# View response headers
curl -I http://localhost:8000/health

# Verbose output
curl -v http://localhost:8000/health
```

### Environment & Configuration

```bash
# Create .env file
cp .env.example .env

# Edit .env
nano .env          # Linux/Mac
vim .env           # Linux/Mac
notepad .env       # Windows

# View environment variables
printenv           # Linux/Mac
set                # Windows
echo $VARIABLE     # Linux/Mac
echo %VARIABLE%    # Windows

# Load environment variables (if using direnv)
direnv allow

# Export variable temporarily
export DATABASE_URL="mysql+aiomysql://..."  # Linux/Mac
set DATABASE_URL="mysql+aiomysql://..."     # Windows
```

### Project Maintenance

```bash
# Check for outdated packages
pip list --outdated

# Update requirements.txt
pip freeze > requirements.txt

# Clean Python cache files
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Clean Python cache (Windows)
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"

# Count lines of code
find . -name "*.py" -exec wc -l {} +

# Search for TODO comments
grep -r "TODO" app/

# Search for FIXME comments
grep -r "FIXME" app/

# Find large files
find . -type f -size +1M

# Disk usage
du -sh *
```

### Utility Commands

```bash
# Generate secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate UUID
python -c "import uuid; print(uuid.uuid4())"

# Get current timestamp
python -c "import datetime; print(datetime.datetime.now())"

# Hash password
python -c "from passlib.hash import bcrypt; print(bcrypt.hash('password123'))"

# Encode to base64
echo -n "text" | base64

# Decode from base64
echo "dGV4dA==" | base64 -d

# Check port availability
netstat -an | grep 8000      # Linux/Mac
netstat -an | findstr 8000   # Windows

# Kill process on port
kill -9 $(lsof -ti:8000)     # Linux/Mac
# On Windows: Use Task Manager or
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## Firebase Integration (Optional)

The application includes Firebase authentication support. To enable:

1. **Install Firebase Admin SDK**
```bash
pip install firebase-admin==6.5.0
```

2. **Get Firebase credentials**
- Go to [Firebase Console](https://console.firebase.google.com/)
- Project Settings → Service Accounts
- Generate new private key
- Save as `config/firebase-credentials.json`

3. **Update environment variables**
```bash
FIREBASE_CREDENTIALS_PATH=./config/firebase-credentials.json
```

4. **Firebase endpoints**
- `GET /api/firebase/verify` - Verify Firebase token
- `GET /api/firebase/profile` - Get Firebase user profile
- `POST /api/firebase/sync-user` - Sync Firebase user to database

## Development

### Adding new features

1. Create model in `app/models/`
2. Create schema in `app/schemas/`
3. Create repository in `app/repositories/`
4. Create service in `app/services/`
5. Create controller in `app/controllers/`
6. Create routes in `app/routes/`
7. Register routes in `main.py`
8. Generate migration: `alembic revision --autogenerate -m "description"`
9. Apply migration: `alembic upgrade head`

### Testing endpoints

Use the interactive Swagger UI at http://localhost:8000/docs to test all endpoints directly in your browser.

## Security Features

- **Password Hashing** - Bcrypt with 12 rounds
- **JWT Tokens** - HS256 algorithm with configurable expiration
- **Access Control** - Role-based authorization (user/superuser)
- **CORS Protection** - Configurable allowed origins
- **SQL Injection Protection** - Parameterized queries via SQLAlchemy
- **Input Validation** - Pydantic schema validation

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Features:
- Try out endpoints directly
- View request/response schemas
- Test authentication
- See validation rules

## Error Handling

All errors follow a consistent format:

```json
{
  "detail": "Error message"
}
```

### HTTP Status Codes

- **200** - Success (GET, PATCH)
- **201** - Created (POST)
- **204** - No Content (DELETE)
- **400** - Bad Request
- **401** - Unauthorized
- **403** - Forbidden
- **404** - Not Found
- **422** - Validation Error
- **500** - Server Error

## Production Deployment

### Checklist

- [ ] Set `APP_ENV=production`
- [ ] Use strong `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Configure HTTPS/SSL
- [ ] Set up proper CORS origins
- [ ] Enable rate limiting
- [ ] Configure logging
- [ ] Set up database backups
- [ ] Use production database credentials
- [ ] Review security settings
- [ ] Set up monitoring

### Production Settings

```bash
# .env.production
APP_ENV=production
APP_DEBUG=False
SECRET_KEY=<strong-random-key>
JWT_SECRET_KEY=<strong-random-key>
DATABASE_URL=mysql+aiomysql://user:password@prod-host:3306/prod_db
ALLOWED_ORIGINS=https://yourdomain.com
```

## Troubleshooting

### Database connection error
```bash
docker-compose restart db
```

### Port already in use
```bash
docker-compose down
# Change port in docker-compose.yml
```

### Migration conflicts
```bash
alembic downgrade -1
# Delete problematic migration file
alembic revision --autogenerate -m "new migration"
alembic upgrade head
```

### Reset everything
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec app alembic upgrade head
```

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy 2.0** - SQL toolkit and ORM
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **MySQL/MariaDB** - Relational database
- **JWT** - Token-based authentication
- **Docker** - Containerization
- **Uvicorn** - ASGI server

## Requirements

- Python 3.8+
- MySQL 8.0+ or MariaDB 10.5+
- Docker & Docker Compose (for containerized deployment)

## License

MIT License

## Support

For issues or questions:
- Check Swagger UI: http://localhost:8000/docs
- Review server logs: `docker-compose logs -f app`
- Check database: http://localhost:8080 (phpMyAdmin)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic Documentation](https://alembic.sqlalchemy.org)
- [Pydantic Documentation](https://docs.pydantic.dev)
