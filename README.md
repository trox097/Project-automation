# Demoblaze UI Automation

Python + Selenium test automation framework using the Page Object Model to validate key Demoblaze shopping flows.

## Project Structure

- `automation/` – reusable page objects and modal abstractions.
- `tests/` – PyTest suite covering login, cart management, and checkout.
- `requirements.txt` – runtime dependencies (Selenium, WebDriver Manager, PyTest).

## Getting Started

1. Create and activate a Python 3.11 (or compatible) virtual environment.
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Execute tests (Chrome by default):

```powershell
pytest --browser chrome
```

### Cross-Browser & Headless Execution

- Run in Firefox:

```powershell
pytest --browser firefox
```

- Headless mode (Chrome or Firefox):

```powershell
pytest --browser chrome --headless
```

## Covered Scenarios

1. `tests/test_login.py` – validates successful login and session indicator.
2. `tests/test_cart.py` – adds multiple products, verifies cart contents and totals.
3. `tests/test_checkout.py` – completes the happy-path checkout and confirms order id.

## Reporting

Generate an HTML execution report:

```powershell
pytest --browser chrome --headless --html=reports/report.html --self-contained-html
```

The report will be created under `reports/`. Ensure the folder exists or create it before running the command.
