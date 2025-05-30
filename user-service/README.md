# HealthCare System - User Service

Đây là microservice quản lý người dùng cho hệ thống HealthCare System, được xây dựng bằng Django REST Framework.

## Tính năng

- **Đăng ký và đăng nhập người dùng** với JWT authentication
- **Quản lý profile người dùng** với thông tin mở rộng
- **Phân quyền theo role**: Admin, Doctor, Patient, Staff
- **Quản lý session** và theo dõi hoạt động người dùng
- **API RESTful** đầy đủ cho tất cả các thao tác
- **Docker support** để dễ dàng triển khai
- **Celery** cho xử lý background tasks
- **PostgreSQL** database
- **Redis** cho caching và message broker

## Cấu trúc dự án

\`\`\`
userservice/
├── userservice/          # Django project settings
├── users/               # Users app
│   ├── models.py       # User, UserProfile, UserSession models
│   ├── serializers.py  # DRF serializers
│   ├── views.py        # API views
│   ├── permissions.py  # Custom permissions
│   └── urls.py         # URL routing
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose setup
└── Makefile          # Development commands
\`\`\`

## Cài đặt và chạy

### 1. Clone repository
```bash
git clone <repository-url>
cd userservice
```
### 2. Tạo file environment

```shellscript
cp .env.example .env
# Chỉnh sửa các biến môi trường trong file .env
```

### 3. Chạy với Docker

```shellscript
# Build và start services
make build
make up

# Chạy migrations
make migrate

# Tạo superuser
make createsuperuser
```

### 4. Truy cập ứng dụng

- API: [http://localhost:8000/api/v1/users/](http://localhost:8000/api/v1/users/)
- Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- Health check: [http://localhost:8000/api/v1/users/health/](http://localhost:8000/api/v1/users/health/)


## API Endpoints

### Authentication

- `POST /api/v1/users/register/` - Đăng ký người dùng mới
- `POST /api/v1/users/login/` - Đăng nhập
- `POST /api/v1/users/logout/` - Đăng xuất
- `POST /api/v1/users/token/refresh/` - Refresh JWT token


### Profile Management

- `GET /api/v1/users/profile/` - Lấy thông tin profile
- `PUT /api/v1/users/profile/` - Cập nhật profile
- `POST /api/v1/users/change-password/` - Đổi mật khẩu
- `GET /api/v1/users/sessions/` - Xem các session
- `GET /api/v1/users/dashboard/` - Dashboard người dùng


### Admin Management

- `GET /api/v1/users/manage/` - Danh sách người dùng
- `POST /api/v1/users/manage/{id}/verify_user/` - Xác thực người dùng
- `POST /api/v1/users/manage/{id}/deactivate_user/` - Vô hiệu hóa người dùng
- `GET /api/v1/users/manage/statistics/` - Thống kê người dùng


## Models

### User Model

- Kế thừa từ AbstractUser
- Thêm các trường: role, phone_number, date_of_birth, gender, address, etc.
- Support cho 4 roles: admin, doctor, patient, staff


### UserProfile Model

- Thông tin mở rộng cho người dùng
- Thông tin y tế (cho bệnh nhân)
- Thông tin chuyên môn (cho bác sĩ)
- Cài đặt privacy


### UserSession Model

- Theo dõi các session đăng nhập
- Thông tin device, IP, location
- Quản lý security


## Development Commands

```shellscript
# Xem logs
make logs

# Restart services
make restart

# Django shell
make shell

# Run tests
make test

# Clean up
make clean
```

## Environment Variables

Xem file `.env.example` để biết các biến môi trường cần thiết.

## Security Features

- JWT authentication với refresh tokens
- Password validation
- Session tracking
- IP address logging
- Role-based permissions
- CORS configuration


## Monitoring và Logging

- Structured logging với Python logging
- Health check endpoint
- User activity tracking
- Session monitoring


## Tích hợp với các microservices khác

Service này được thiết kế để tích hợp với:

- PatientService
- DoctorService
- AppointmentService
- AIChatService


Sử dụng JWT tokens để authenticate giữa các services.

## Production Deployment

Để deploy production:

1. Thay đổi `DEBUG=False` trong settings
2. Cập nhật `SECRET_KEY` và các credentials
3. Cấu hình proper database và Redis
4. Setup reverse proxy (nginx)
5. Configure SSL/TLS
6. Setup monitoring và logging


## Contributing

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request