# UI Automation Assessment (Python + Selenium + Pytest)

This project implements the interview assessment in Python with Page Object Model (POM).

## Covered Scenario

1. Open `https://insiderone.com/` and verify home page + main blocks.
2. Go to `https://insiderone.com/careers/quality-assurance/`, click **See all QA jobs**.
3. Filter by:
   - Location: **Istanbul, Turkey**
   - Department: **Quality Assurance**
4. Verify jobs list exists and every listed item has:
   - Position contains **Quality Assurance**
   - Department contains **Quality Assurance**
   - Location contains **Istanbul, Turkey**
5. Click **View Role** and verify redirect to a **Lever** application page.

## Project Structure

- `pages/` → POM classes
- `tests/` → test + fixtures
- `screenshots/` → created automatically on failure

## Setup

```bash
pip install -r requirements.txt
```

## Run

Chrome:

```bash
C:/Users/erdogde/Desktop/UI_Automation_Assesment/.venv/Scripts/python.exe -m pytest --browser=chrome
```

Firefox:

```bash
C:/Users/erdogde/Desktop/UI_Automation_Assesment/.venv/Scripts/python.exe -m pytest --browser=firefox
```

If Firefox cannot start because Selenium Manager cannot download driver (common on low disk space), set environment variables and run again:

```bash
set GECKODRIVER_PATH=C:\tools\geckodriver.exe
set FIREFOX_BINARY=C:\Program Files\Mozilla Firefox\firefox.exe
C:/Users/erdogde/Desktop/UI_Automation_Assesment/.venv/Scripts/python.exe -m pytest --browser=firefox
```

## Notes

- No BDD framework is used.
- Browser is parametrically changeable via `--browser`.
- If any step fails, screenshot is automatically captured.