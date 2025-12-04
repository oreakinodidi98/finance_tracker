# 💰 Finance Tracker

A modern web application for managing your personal finances built with React frontend, Flask backend and Azure Postgres database. Track your income, expenses, and savings goals with powerful analytics and beautiful visualizations to take control of your financial future.

![Finance Tracker](https://img.shields.io/badge/Status-Active-green)
![React](https://img.shields.io/badge/Frontend-React-blue)
![Flask](https://img.shields.io/badge/Backend-Flask-red)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)

## ✨ Features

### 💳 Transaction Management

- **Income Tracking** - Record all sources of income with categories and dates
- **Expense Logging** - Track spending across customizable categories
- **Transaction History** - View complete financial history with filtering and search
- **Recurring Transactions** - Set up automatic entries for regular income/expenses
- **Smart Categories** - Pre-defined and custom categories for organized tracking

### 📊 Financial Analytics

- **Balance Overview** - Real-time view of total income, expenses, and net balance
- **Monthly Breakdown** - Detailed monthly analysis of spending patterns
- **Category Insights** - Visual breakdown of spending by category
- **Trend Analysis** - Track financial trends over time with interactive charts
- **Budget Variance** - Compare actual spending against planned budgets

### 🎯 Budget & Goals

- **Budget Planning** - Set monthly or annual budgets for each category
- **Savings Goals** - Create and track progress toward financial goals
- **Alert System** - Notifications when approaching or exceeding budget limits
- **Goal Milestones** - Visual progress tracking with milestone celebrations
- **What-If Scenarios** - Project future savings based on current patterns

### 📈 Reporting & Insights

- **Financial Dashboard** - Comprehensive overview of your financial health
- **Custom Reports** - Generate reports for specific date ranges or categories
- **Export Functionality** - Download transaction data in CSV or PDF format
- **Visual Charts** - Interactive pie charts, line graphs, and bar charts
- **Spending Patterns** - AI-powered insights into your spending habits

### 🔒 Security & Privacy

- **Secure Authentication** - User accounts with encrypted passwords
- **Data Encryption** - All financial data encrypted at rest and in transit
- **Privacy First** - Your data belongs to you, never shared or sold
- **Session Management** - Automatic logout for enhanced security

### 🎨 Modern Interface

- **Intuitive Design** - Clean, professional interface inspired by leading fintech apps
- **Responsive Layout** - Seamless experience across desktop, tablet, and mobile
- **Dark Mode** - Easy on the eyes with optional dark theme
- **Quick Actions** - Fast transaction entry with keyboard shortcuts
- **Drag & Drop** - Intuitive bulk operations and transaction organization

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.9 or higher)
- **PostgreSQL** database (local or Azure)
- **npm** or **yarn** package manager

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd finance-tracker
```

### 2. Backend Setup

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
# Windows PowerShell:
$env:DATABASE_URL = 'postgresql://username:password@host:5432/financetracker?sslmode=require'
$env:SECRET_KEY = 'your-secret-key-here'
$env:FLASK_ENV = 'development'

# Linux/macOS:
export DATABASE_URL='postgresql://username:password@host:5432/financetracker?sslmode=require'
export SECRET_KEY='your-secret-key-here'
export FLASK_ENV='development'

# Initialize database
python init_db.py

# Start the Flask server
python app.py
```

The backend will run on `http://localhost:5000`

### 3. Frontend Setup

```bash
# create scafolding
npm create vite@latest frontend -- --template react

# Navigate to frontend folder (in a new terminal)
cd frontend

# Install dependencies
npm install
# or
yarn install

# Create environment file
cp .env.example .env

# Edit .env with your configuration
# REACT_APP_API_URL=http://localhost:5000

# Start the React development server
npm start
# or
yarn start
```

The frontend will run on `http://localhost:3000`

### 4. Access the Application
Open your browser and navigate to `http://localhost:3000` to start managing your finances!

## 🗂️ Project Structure

```
finance-tracker/
├── backend/                      # Flask API server
│   ├── app.py                   # Main Flask application
│   ├── models.py                # Database models
│   ├── routes/                  # API route handlers
│   │   ├── transactions.py     # Transaction endpoints
│   │   ├── budgets.py          # Budget endpoints
│   │   ├── goals.py            # Goals endpoints
│   │   └── analytics.py        # Analytics endpoints
│   ├── services/               # Business logic layer
│   │   ├── transaction_service.py
│   │   ├── budget_service.py
│   │   └── analytics_service.py
│   ├── utils/                  # Helper utilities
│   │   ├── auth.py            # Authentication helpers
│   │   └── validators.py      # Input validation
│   ├── migrations/            # Database migrations
│   ├── init_db.py            # Database initialization
│   ├── requirements.txt      # Python dependencies
│   └── config.py            # Configuration settings
├── frontend/                  # React application
│   ├── public/               # Static assets
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── Dashboard/   # Dashboard components
│   │   │   ├── Transactions/ # Transaction components
│   │   │   ├── Budgets/     # Budget components
│   │   │   ├── Goals/       # Goals components
│   │   │   └── Common/      # Shared components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API service layer
│   │   ├── utils/           # Helper functions
│   │   ├── styles/          # CSS/SCSS files
│   │   ├── App.js          # Main App component
│   │   └── index.js        # React entry point
│   ├── package.json        # Node dependencies
│   └── .env.example        # Environment variables template
├── database/                # Database scripts
│   ├── schema.sql          # Database schema
│   └── seed.sql            # Sample data
├── docs/                   # Documentation
│   ├── API.md             # API documentation
│   └── USER_GUIDE.md      # User guide
├── docker-compose.yml     # Docker setup
├── .gitignore
└── README.md             # This file
```

## 🎯 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/user` - Get current user info

### Transactions
- `GET /api/transactions` - Get all transactions (with filters)
- `POST /api/transactions` - Create new transaction
- `GET /api/transactions/{id}` - Get specific transaction
- `PUT /api/transactions/{id}` - Update transaction
- `DELETE /api/transactions/{id}` - Delete transaction
- `GET /api/transactions/export` - Export transactions as CSV/PDF

### Budgets
- `GET /api/budgets` - Get all budgets
- `POST /api/budgets` - Create new budget
- `PUT /api/budgets/{id}` - Update budget
- `DELETE /api/budgets/{id}` - Delete budget
- `GET /api/budgets/{id}/progress` - Get budget progress

### Goals
- `GET /api/goals` - Get all savings goals
- `POST /api/goals` - Create new goal
- `PUT /api/goals/{id}` - Update goal
- `DELETE /api/goals/{id}` - Delete goal
- `POST /api/goals/{id}/contribute` - Add contribution to goal

### Analytics
- `GET /api/analytics/overview` - Get financial overview
- `GET /api/analytics/trends` - Get spending trends
- `GET /api/analytics/categories` - Get category breakdown
- `GET /api/analytics/monthly` - Get monthly comparison
- `GET /api/analytics/insights` - Get AI-powered insights

### Categories
- `GET /api/categories` - Get all categories
- `POST /api/categories` - Create custom category
- `PUT /api/categories/{id}` - Update category
- `DELETE /api/categories/{id}` - Delete category

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
DATABASE_URL=postgresql://user:password@host:5432/financetracker
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
JWT_SECRET_KEY=your-jwt-secret
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

#### Frontend (.env)

```bash
REACT_APP_API_URL=http://localhost:5000
REACT_APP_ENV=development
REACT_APP_ENABLE_ANALYTICS=true
```

### Database Setup

#### Option 1: Local PostgreSQL

```bash
# Install PostgreSQL
# Create database and user
psql -U postgres -c "CREATE USER financeuser WITH PASSWORD 'securepassword';"
psql -U postgres -c "CREATE DATABASE financetracker OWNER financeuser;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE financetracker TO financeuser;"

# Run initialization script
cd backend
python init_db.py
```

#### Option 2: Azure PostgreSQL Flexible Server

```bash
# Create Azure PostgreSQL
az postgres flexible-server create \
  --resource-group myResourceGroup \
  --name finance-tracker-db \
  --location eastus \
  --admin-user financeadmin \
  --admin-password YourSecurePassword123! \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32

# Create database
az postgres flexible-server db create \
  --resource-group myResourceGroup \
  --server-name finance-tracker-db \
  --database-name financetracker

# Configure firewall (allow your IP)
az postgres flexible-server firewall-rule create \
  --resource-group myResourceGroup \
  --name finance-tracker-db \
  --rule-name AllowMyIP \
  --start-ip-address YOUR_IP \
  --end-ip-address YOUR_IP

# Connection string
postgresql://financeadmin:YourSecurePassword123!@finance-tracker-db.postgres.database.azure.com:5432/financetracker?sslmode=require
```

#### Option 3: Docker PostgreSQL

```bash
# Use docker-compose
docker-compose up -d

# Connection string
postgresql://financeuser:financepass@localhost:5432/financetracker
```

## 🛠️ Development

### Adding New Features

1. **Backend**:
   - Add models in `models.py`
   - Create routes in `routes/`
   - Implement business logic in `services/`
   - Write tests in `tests/`

2. **Frontend**:
   - Create components in `src/components/`
   - Add pages in `src/pages/`
   - Update API services in `src/services/`
   - Style with CSS/SCSS in `src/styles/`

3. **Database**:
   - Create migration scripts
   - Update `schema.sql`
   - Test with seed data

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test
# or
yarn test

# E2E tests
npm run test:e2e
```

### Code Quality

```bash
# Backend linting
cd backend
flake8 .
black .

# Frontend linting
cd frontend
npm run lint
npm run format
```

## 🔄 Version History

### Version 2.0 (Current) - Advanced Analytics

- ✅ AI-powered spending insights
- ✅ Custom report generation
- ✅ Export to CSV/PDF
- ✅ Dark mode support
- ✅ Recurring transactions
- ✅ Budget alerts

### Version 1.5 - Goals & Budgets

- ✅ Savings goals tracking
- ✅ Budget management
- ✅ Category customization
- ✅ Monthly comparisons

### Version 1.0 - Initial Release

- ✅ Transaction tracking
- ✅ Basic analytics dashboard
- ✅ User authentication
- ✅ Category management

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Contribution Guidelines

- Write clear commit messages
- Add tests for new features
- Update documentation
- Follow existing code style
- Ensure all tests pass

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**Database Connection Failed**

```bash
# Verify DATABASE_URL
echo $DATABASE_URL

# Check PostgreSQL is running
# Local:
sudo systemctl status postgresql
# Docker:
docker ps | grep postgres

# Test connection
psql $DATABASE_URL -c "SELECT 1;"
```

**Authentication Errors**

```bash
# Check SECRET_KEY is set
echo $SECRET_KEY

# Clear browser cookies
# Restart Flask server
```

**Frontend Not Loading**

```bash
# Clear cache
npm cache clean --force

# Remove and reinstall
rm -rf node_modules package-lock.json
npm install

# Check API URL in .env
cat .env | grep REACT_APP_API_URL
```

**Port Already in Use**

```bash
# Kill process on port 5000 (backend)
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### Getting Help
- 📖 Check [API Documentation](docs/API.md)
- 📚 Read [User Guide](docs/USER_GUIDE.md)
- 🐛 Report bugs via GitHub Issues
- 💬 Join our community discussions

## 🚀 Deployment

### Deploy to Azure App Service
```bash
# Create App Service
az webapp up \
  --resource-group myResourceGroup \
  --name finance-tracker-app \
  --runtime "PYTHON:3.9" \
  --sku B1

# Configure environment variables
az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name finance-tracker-app \
  --settings DATABASE_URL="..." SECRET_KEY="..."
```

### Deploy with Docker

```bash
# Build and run all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Install ArgoCD

# 1. Create ArgoCD namespace
kubectl create namespace argocd

# 2. Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# 3. Wait for ArgoCD pods to be ready
kubectl wait --for=condition=ready pod --all -n argocd --timeout=300s

# 4. Get the initial admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | ForEach-Object { [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($_)) }

# 5. Expose ArgoCD server (choose ONE option below)

## Option A: Port Forward (for testing)

kubectl port-forward svc/argocd-server -n argocd 8080:443

- Access at: https://localhost:8080
- Username: admin
- Password: (from step 4)

## Option B: LoadBalancer (for production)

kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'

Wait for external IP
kubectl get svc argocd-server -n argocd -w
Access at: https://<EXTERNAL-IP>

## Option C: Ingress (recommended for production)

1. First, install nginx-ingress controller if you don't have one
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml

2. Create ArgoCD ingress
@"
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: argocd-server-ingress
  namespace: argocd
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-passthrough: "true"
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
spec:
  ingressClassName: nginx
  rules:
  - host: argocd.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: argocd-server
            port:
              name: https
  tls:
  - hosts:
    - argocd.yourdomain.com
    secretName: argocd-server-tls
"@ | kubectl apply -f -

## Install ArgoCD CLI 

1. Download ArgoCD CLI for Windows
Invoke-WebRequest -Uri https://github.com/argoproj/argo-cd/releases/latest/download/argocd-windows-amd64.exe -OutFile argocd.exe

2. Move to a folder in your PATH
Move-Item argocd.exe $env:USERPROFILE\bin\argocd.exe

3. Login via CLI
argocd login localhost:8080 --username admin --password <password-from-step-4> --insecure

For production deployment with security hardening, see [SECURITY.md](SECURITY.md).

## 🔐 Security & Vulnerability Scanning

This project implements comprehensive security best practices and provides tools for vulnerability scanning.

### Quick Security Scan

Run the automated security scanner:

```powershell
.\security-scan.ps1
```

This script will:
- Build Docker images with security optimizations
- Scan all images for vulnerabilities using Docker Scout
- Check for exposed secrets in the codebase
- Audit Python and npm dependencies
- Generate detailed reports in `security-reports/`

### Security Features

- **Non-root containers** - All services run as non-privileged users
- **Production WSGI server** - Using Gunicorn instead of Flask dev server
- **Security headers** - HSTS, CSP, X-Frame-Options, etc.
- **Dependency pinning** - Exact versions to prevent supply chain attacks
- **Minimal attack surface** - Multi-stage builds, minimal base images
- **Network isolation** - Database not exposed to host

### Vulnerability Scanning Tools

We support multiple scanning tools:

1. **Docker Scout** (Recommended) - Built into Docker Desktop
   ```powershell
   docker scout cves finance_tracker-backend:latest
   docker scout recommendations finance_tracker-backend:latest
   ```

2. **Trivy** - Comprehensive open-source scanner
   ```powershell
   trivy image --severity HIGH,CRITICAL finance_tracker-backend:latest
   ```

3. **Snyk** - Commercial tool with free tier
   ```powershell
   snyk container test finance_tracker-backend:latest
   ```

For detailed security documentation, scanning procedures, and remediation guidance, see [SECURITY.md](SECURITY.md).

## 🌟 Features Roadmap

### Coming Soon
- [ ] Mobile app (React Native)
- [ ] Bank account integration via Plaid
- [ ] Receipt scanning with OCR
- [ ] Bill reminders
- [ ] Investment tracking
- [ ] Multi-currency support
- [ ] Shared accounts/family mode
- [ ] Tax report generation

## 📞 Support & Contact

- **Email**: support@financetracker.com
- **Documentation**: [docs.financetracker.com](https://docs.financetracker.com)
- **Issues**: [GitHub Issues](https://github.com/yourusername/finance-tracker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/finance-tracker/discussions)

---

## 📋 Recommended Priority Order

**PRIORITY 1: Authentication System (2-3 weeks) ⚠️ CRITICAL**
The research revealed your app needs:

- JWT-based login/registration system
- Password hashing (bcrypt)
- Protected routes with @token_required decorator
- Token refresh mechanism
- React authentication context
- Protected frontend routes
- Why Critical? Currently anyone can access all financial data. This blocks production deployment.

**PRIORITY 2: Multi-User Support (2 weeks)**

- Remove hardcoded user_id=1 from all endpoints
- Proper user isolation
- Profile management
- User preferences & settings

**PRIORITY 3: Advanced Financial Features (3-4 weeks)**

- Recurring transactions
- Bill reminders with notifications
- Budget alerts
- PDF/CSV export
- Receipt OCR with Azure Form Recognizer

PRIORITY 4: Enhanced GenAI (2 weeks)

Your chatbot exists but needs:

Personalized insights based on user's actual data
Spending pattern analysis
Predictive budgeting
Natural language transaction entry

**PRIORITY 5: DevOps & Monitoring (1-2 weeks)**

- Environment separation (dev/staging/prod)
- Automated testing in CI/CD
- Azure Application Insights
- Database backup strategy

🚀 Quick Start: Login System
The detailed plan includes complete code for:

- Backend: auth.py module with JWT generation, password hashing, @token_required decorator
- Frontend: AuthContext, LoginPage, RegisterPage, ProtectedRoute component
- Security: Rate limiting, CORS restrictions, password validation
- 8 new endpoints: /auth/register, /auth/login, /auth/logout, /auth/me, /auth/refresh, /auth/change-password

**Take Control of Your Finances Today! 💰📊**

Built with ❤️ using React, Flask, PostgreSQL, and powered by modern fintech principles

*Your financial data is private and secure. We never sell or share your information.*