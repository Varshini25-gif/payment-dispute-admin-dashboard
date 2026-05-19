# Payment Dispute Admin Dashboard

A modern, responsive Streamlit-based admin dashboard for managing payment disputes efficiently. This application provides real-time monitoring, analytics, and management tools for payment dispute resolution.

## 🚀 Features

- **Dashboard Overview**: Real-time metrics and key performance indicators
- **Dispute Management**: Monitor and manage all payment disputes
- **Analytics**: Comprehensive analytics and reporting
- **User Management**: Manage admin users and access control
- **Settings**: Configure application settings and preferences
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Dark Mode Support**: Built-in dark mode theme support

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/payment-dispute-admin-dashboard.git
cd payment-dispute-admin-dashboard
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual configuration
```

**Environment Variables**:
- `API_BASE_URL`: Backend API endpoint (default: http://localhost:8000)
- `API_TIMEOUT`: API request timeout in seconds (default: 30)
- `DB_HOST`: Database host (default: localhost)
- `DB_PORT`: Database port (default: 5432)
- `DB_NAME`: Database name (default: payment_disputes)
- `DB_USER`: Database username (default: admin)
- `DB_PASSWORD`: Database password
- `DEBUG`: Enable debug mode (default: false)
- `LOG_LEVEL`: Logging level (default: INFO)

## 🎯 Quick Start

### Run the Application

```bash
# Windows
streamlit run app\main.py

# macOS/Linux
streamlit run app/main.py
```

The application will open at `http://localhost:8501`

### Run Tests

```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=app
```

## 📁 Project Structure

```
payment-dispute-admin-dashboard/
│
├── app/
│   ├── main.py                 # Main application entry point
│   ├── __init__.py
│   ├── pages/                  # Page modules
│   │   ├── dashboard.py       # Dashboard page
│   │   └── __init__.py
│   ├── components/             # Reusable UI components
│   │   └── __init__.py
│   ├── services/               # Business logic and API services
│   │   └── __init__.py
│   ├── utils/                  # Utility functions
│   │   └── __init__.py
│   └── state/                  # Application state management
│       └── __init__.py
│
├── assets/                     # Static assets (images, etc.)
├── tests/                      # Unit and integration tests
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment variables
├── .gitignore                 # Git ignore rules
└── README.md                  # Project documentation
```

## 🛠️ Development

### Add New Pages

1. Create a new file in `app/pages/`:
```python
# app/pages/new_page.py
import streamlit as st

def render():
    st.header("Your Page Title")
    st.write("Your content here")
```

2. Add navigation in `app/main.py`:
```python
elif page_name == "Your Page":
    from app.pages.new_page import render as render_new_page
    render_new_page()
```

### Add New Components

Create reusable components in `app/components/`:
```python
# app/components/your_component.py
import streamlit as st

def render_component(param1, param2):
    # Component logic here
    st.write(f"Param 1: {param1}")
```

### Add Services

Create API services in `app/services/`:
```python
# app/services/api_client.py
import requests
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("API_BASE_URL")

def fetch_disputes():
    response = requests.get(f"{BASE_URL}/disputes")
    return response.json()
```

## 🧪 Testing

Tests are located in the `tests/` directory. Use pytest for testing:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_main.py

# Run with coverage report
pytest --cov=app
```

## 📊 Configuration

### Streamlit Config (`config.toml`)

The application is configured via `.streamlit/config.toml` with:
- **Theme Colors**: Customizable primary, secondary, and text colors
- **Server Settings**: Port (8501), headless mode, XSRF protection
- **Browser Settings**: Usage statistics disabled for privacy
- **Logger Level**: Info level logging

### Customize Theme

Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

## 🔐 Security

- ✅ XSRF protection enabled
- ✅ Environment variables for sensitive data
- ✅ Secrets management via `.streamlit/secrets.toml`
- ✅ Git ignore configured for sensitive files

### Best Practices

1. Never commit `.env` file
2. Always use `.env.example` as template
3. Keep `secrets.toml` in `.gitignore`
4. Use environment variables for API keys and passwords

## 📝 Logging

Configure logging in your modules:
```python
import logging
import os

log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)
```

## 🚢 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [streamlit.io/cloud](https://share.streamlit.io/)
3. Click "New app" and connect your GitHub repository
4. Configure secrets in Streamlit Cloud settings
5. Deploy!

### Deploy to Docker

```bash
# Create Dockerfile
docker build -t payment-dispute-dashboard .
docker run -p 8501:8501 payment-dispute-dashboard
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Support

For support, email support@paymentsolutions.com or open an issue on GitHub.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Dashboard design inspired by modern admin interfaces
- Icons from Streamlit's built-in emoji support

---

**Version**: 0.1.0  
**Last Updated**: May 2026  
**Status**: Active Development