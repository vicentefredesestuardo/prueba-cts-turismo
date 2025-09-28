# 💕 Concurso San Valentín - Hotel Mirador del Lago

Sistema de concurso web con inscripción, verificación por email y sorteo administrativo.

**Stack:** Frontend (Nuxt 3) + Backend (Django + DRF) + Auth JWT + Emails (Celery + Redis)

## 🚀 Requisitos

- **Python 3.11+**
- **Node.js 18+**
- **Redis** (ver opciones de instalación abajo)

### 🔧 Redis - Opciones de Instalación

#### **Linux/macOS:**

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install redis-server
sudo systemctl start redis-server

# macOS (Homebrew)
brew install redis
brew services start redis
```

#### **Windows:**

```bash
# Opción 1: Memurai (recomendado para Windows)
# Descargar e instalar desde: https://www.memurai.com/
# El servicio se inicia automáticamente

# Opción 2: Redis en WSL
wsl --install
wsl
sudo apt update && sudo apt install redis-server
sudo service redis-server start
```

#### **Docker (Universal):**

```bash
# Cualquier sistema operativo
docker run -d --name redis -p 6379:6379 redis:alpine
```

#### **✅ Verificar instalación:**

```bash
# Probar conexión (cualquier SO)
redis-cli ping
# Debe responder: PONG

# En Windows con Memurai, si no tienes `redis-cli`, puedes usar `memurai-cli ping`
# o verificar que el servicio "Memurai" esté en ejecución.
```

## 🧩 Estructura del Proyecto

```
prueba-cts-turismo/
├── backend/                 # Django + DRF
│   ├── cts_valentine/      # Settings, URLs base, configuración Celery
│   │   ├── settings.py     # Configuración Django
│   │   ├── urls.py         # URLs base del proyecto
│   │   └── celery.py       # Configuración Celery para emails asíncronos
│   ├── contest/            # App principal del concurso
│   │   ├── models.py       # Contestant, EmailVerificationToken, WinnerDraw
│   │   ├── views.py        # API endpoints (registro, verificación, admin)
│   │   ├── serializers.py  # Validación y serialización DRF
│   │   ├── tasks.py        # Emails asíncronos con Celery
│   │   ├── urls.py         # Rutas de la app contest
│   │   ├── utils.py        # Helpers de normalización de datos
│   │   ├── admin.py        # Panel Django admin
│   │   └── tests.py        # Tests básicos
│   ├── requirements.txt    # Dependencias del proyecto (backend)
│   └── manage.py           # CLI de Django
└── frontend/               # Nuxt 3 SPA
    ├── pages/              # Rutas del sitio
    │   ├── index.vue       # Inscripción pública
    │   ├── verify.vue      # Verificación + contraseña
    │   └── admin/          # Panel administrativo
    │       ├── login.vue   # Login administrador
    │       ├── contestants.vue # Lista de concursantes
    │       └── winner.vue  # Sorteo y ganador
    ├── middleware/admin.ts # Protección rutas admin
    ├── composables/useApi.ts # Client API centralizado
    └── nuxt.config.ts      # Configuración Nuxt (SPA, Tailwind, API)
```

## 🔧 Instalación y Configuración

### **Backend (Django + DRF)**

1. **Entorno virtual y dependencias:**

```bash
cd backend
python -m venv .venv

# Windows PowerShell:
.venv\Scripts\Activate.ps1

# Windows CMD:
.venv\Scripts\activate.bat

pip install -r requirements.txt
```

2. **Variables de entorno** - Crear `backend/.env`:

```env
# Obligatorias
DJANGO_SECRET_KEY=tu-clave-secreta-aqui
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
FRONTEND_URL=http://localhost:3000

# Email (Desarrollo - ver emails en consola)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Email (Producción - configurar SMTP real)
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=1
# EMAIL_HOST_USER=tu-email@gmail.com
# EMAIL_HOST_PASSWORD=tu-app-password
# DEFAULT_FROM_EMAIL=tu-email@gmail.com

# Redis/Celery
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/1
```

3. **Base de datos y superusuario:**

```bash
python manage.py migrate
python manage.py createsuperuser
```

4. **Ejecutar servicios** (3 terminales):

**Terminal A - Django:**

```bash
python manage.py runserver
# http://localhost:8000
```

**Terminal B - Celery Worker:**

```bash
# Windows:
celery -A cts_valentine worker -l info -P solo

# Linux/macOS:
celery -A cts_valentine worker -l info
```

**Terminal C - Redis (si usas Docker):**

```bash
# Solo si usas Docker para Redis
docker start redis

# Si usas Redis nativo (Linux/macOS) o Memurai (Windows), esta terminal no es necesaria.

# Verificar que Redis esté corriendo:
redis-cli ping  # Debe responder: PONG
```

### **Frontend (Nuxt 3)**

1. **Instalación:**

```bash
cd frontend
npm install
```

2. **Ejecutar:**

```bash
npm run dev
# http://localhost:3000
```

## 🚀 Demo Rápida

Para probar el sistema completo, sigue estos pasos:

### **1. Registro de concursante**

- Ingresa a [http://localhost:3000](http://localhost:3000)
- Completa el formulario de inscripción con datos válidos
- **Importante:** Revisa la consola del worker de Celery para ver el email de verificación (si usas EMAIL_BACKEND=console)

### **2. Verificación de cuenta**

- Copia el enlace de verificación desde la consola (ej: `/verify?token=...`)
- Pégalo en el navegador: `http://localhost:3000/verify?token=...`
- Define tu contraseña para activar la cuenta

### **3. Panel administrativo**

- Ingresa a [http://localhost:3000/admin/login](http://localhost:3000/admin/login)
- Usa las credenciales del superusuario creado con `createsuperuser`
- Explora la lista de concursantes en `/admin/contestants` (filtros, paginación)

### **4. Sorteo del ganador**

- Desde `/admin/winner` realiza el sorteo (**solo una vez permitido**)
- El ganador seleccionado recibe automáticamente un email de notificación
- Verifica el email del ganador en la consola del servidor

### **✅ Flujo completo probado:**

✅ Inscripción → ✅ Verificación → ✅ Admin → ✅ Sorteo → ✅ Notificación

## 🛣️ Endpoints de la API

**Base URL:** `http://localhost:8000/api`

### **Endpoints Públicos**

#### **Registro de Concursante**

```http
POST /contestants/
Content-Type: application/json

{
  "first_name": "Juan",
  "last_name": "Pérez",
  "second_last_name": "González",
  "email": "juan@ejemplo.com",
  "phone": "+56912345678"
}
```

**Response 201:**

```json
{
  "message": "¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta.",
  "contestant_id": 1
}
```

---

#### **Verificación de Email + Contraseña**

```http
POST /verification/
Content-Type: application/json

{
  "token": "550e8400-e29b-41d4-a716-446655440000",
  "password": "micontraseña123",
  "password_confirm": "micontraseña123"
}
```

**Response 200:**

```json
{
  "message": "Tu cuenta ha sido activada. Ya estás participando en el sorteo.",
  "contestant": {
    "id": 1,
    "full_name": "Juan Pérez González",
    "email": "juan@ejemplo.com",
    "is_verified": true
  }
}
```

---

### **Endpoints Admin (JWT requerido)**

#### **Login Administrativo**

```http
POST /admin/login/
Content-Type: application/json

{
  "username": "admin",
  "password": "tupassword"
}
```

**Response 200:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

#### **Listar Concursantes**

```http
GET /admin/contestants/?verified=true&search=juan&page=1&page_size=50
Authorization: Bearer <access_token>
```

**Response 200:**

```json
{
  "count": 25,
  "page": 1,
  "page_size": 50,
  "contestants": [
    {
      "id": 1,
      "full_name": "Juan Pérez González",
      "email": "juan@ejemplo.com",
      "phone": "+56912345678",
      "is_verified": true,
      "created_at": "2024-02-14T10:30:00Z"
    }
  ]
}
```

---

#### **Realizar Sorteo**

```http
POST /admin/winner/
Authorization: Bearer <access_token>
```

**Response 201:**

```json
{
  "message": "¡Ganador seleccionado! Juan Pérez González",
  "winner": {
    "id": 1,
    "contestant_name": "Juan Pérez González",
    "contestant_email": "juan@ejemplo.com",
    "contestant_phone": "+56912345678",
    "drawn_at": "2024-02-14T15:45:00Z"
  }
}
```

---

#### **Ver Estado del Sorteo**

```http
GET /admin/winner/
Authorization: Bearer <access_token>
```

**Response 200 (con ganador):**

```json
{
  "winner": {
    "id": 1,
    "contestant_name": "Juan Pérez González",
    "contestant_email": "juan@ejemplo.com",
    "contestant_phone": "+56912345678",
    "drawn_at": "2024-02-14T15:45:00Z"
  }
}
```

**Response 404 (sin ganador):**

```json
{
  "message": "Aún no se ha realizado el sorteo."
}
```

## 🌐 Páginas del Sistema

- **`/`** - Formulario de inscripción público
- **`/verify?token=...`** - Verificación de email y creación de contraseña
- **`/admin/login`** - Login para administradores
- **`/admin/contestants`** - Lista de concursantes con filtros y paginación
- **`/admin/winner`** - Realizar sorteo y ver ganador

## 🔒 Autenticación y Seguridad

- **JWT (SimpleJWT):** Solo rutas admin requieren autenticación
- **Middleware:** `middleware/admin.ts` protege rutas administrativas
- **Permisos DRF:** `IsAdminUser` en endpoints sensibles
- **Validación:** Frontend con mensajes en español + validación backend con DRF

## 📧 Sistema de Emails

- **Desarrollo:** Emails se muestran en consola del servidor Django
- **Producción:** Configurar SMTP en variables de entorno
- **Celery:** Envío asíncrono para no bloquear requests
- **Templates:** HTML responsive con fallback a texto plano

## ✅ Testing

```bash
cd backend
python manage.py test contest
```

**Cobertura:**

- ✅ Registro exitoso de concursante
- ✅ Verificación con token inválido
- ✅ Endpoints admin requieren JWT
- ✅ Sorteo solo permite un ganador

## 🏗️ Decisiones Técnicas

### **Backend**

- **SQLite:** Simplicidad en desarrollo (se recomienda cambiar a PostgreSQL en producción)
- **Celery + Redis:** Emails asíncronos sin bloquear UX
- **DRF:** API REST estándar con serializers y permisos
- **E.164:** Validación internacional de teléfonos

### **Frontend**

- **Nuxt 3 SPA:** `ssr: false` para usar localStorage con JWT
- **Validación client-side:** UX inmediata antes de enviar al servidor
- **Tailwind CSS:** Diseño responsive con gradientes y animaciones
- **Composables:** `useApi.ts` centraliza lógica de requests

### **UX/Branding**

- **Mensajes en español:** Error handling humanizado
- **Accesibilidad:** Labels asociados, ARIA attributes, focus management
- **Visual feedback:** Bordes rojos, spinners, mensajes de estado consistentes

## 🛠️ Troubleshooting

### **Redis Connection Error**

```bash
# 1. Verificar que Redis esté corriendo
redis-cli ping  # Debe responder: PONG

# 2. Si usas localhost, prueba con IPv4 explícita
CELERY_BROKER_URL=redis://127.0.0.1:6379/0

# 3. Si usas Docker, verificar puerto
docker ps | grep redis  # Puerto debe ser 6379:6379

# 4. WSL en Windows: usar IP de WSL
# En WSL: ip addr show eth0 | grep inet
# Usar esa IP en CELERY_BROKER_URL
```

### **Emails no se envían**

```bash
# En desarrollo, verificar logs de Celery worker
# Los emails aparecen en consola si usas EMAIL_BACKEND=console
```

### **Frontend página en blanco**

```bash
# Limpiar cache de Nuxt
rm -rf .nuxt
npm run dev
```

### **JWT Token Expired**

- El middleware cliente valida el exp del JWT y, si expiró, redirige a `/admin/login` y limpia localStorage
- Si el token vencido llega al backend, los endpoints responden 401 y el frontend reacciona igual

## 📝 Scripts Útiles

```bash
# Backend
python manage.py runserver                    # Servidor Django
celery -A cts_valentine worker -l info -P solo # Worker Celery (Windows)
python manage.py test contest                 # Tests
python manage.py createsuperuser              # Admin user

# Frontend
npm run dev                                   # Servidor Nuxt
npm run build                                 # Build producción
npm run preview                               # Preview build
```

## 📦 Producción

1. **Variables de entorno:** Configurar `DJANGO_SECRET_KEY`, SMTP real, PostgreSQL
2. **Static files:** `python manage.py collectstatic`
3. **Frontend:** `npm run build` genera archivos estáticos
4. **Celery:** Usar supervisor/systemd para workers persistentes
5. **Redis:** Configurar persistencia y backup según necesidades

---

**Nota:** Este proyecto fue desarrollado como prueba técnica para CTS Turismo.
