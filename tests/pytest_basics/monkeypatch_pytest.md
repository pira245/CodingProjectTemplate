# Monkeypatch in pytest

## What is `monkeypatch` in pytest?
In **pytest**, `monkeypatch` is a built-in fixture that allows you to **modify or replace** parts of the code temporarily during testing.  
It is useful when:
- You need to **mock functions or methods** to avoid real API calls or database queries.
- You want to **change environment variables** during tests.
- You need to **patch objects** to test different behaviors.

---

## 1. Replacing a Function using `monkeypatch.setattr`
You can use `monkeypatch.setattr` to override a function with a mock.

### Example: Mocking `datetime.now()`
```python
import datetime
import pytest

def get_current_time():
    return datetime.datetime.now()

def test_get_current_time(monkeypatch):
    class MockDateTime:
        @staticmethod
        def now():
            return datetime.datetime(2025, 1, 1, 12, 0, 0)

    monkeypatch.setattr(datetime, "datetime", MockDateTime)
    
    assert get_current_time() == datetime.datetime(2025, 1, 1, 12, 0, 0)
```
- This replaces `datetime.datetime.now()` with a **mocked value**.

---

## 2. Replacing a Global Variable using `monkeypatch.setattr`
You can also modify **global variables** for testing.

```python
import pytest

GLOBAL_VAR = "original_value"

def get_global_var():
    return GLOBAL_VAR

def test_global_var(monkeypatch):
    monkeypatch.setattr("__main__.GLOBAL_VAR", "patched_value")
    
    assert get_global_var() == "patched_value"
```
- `monkeypatch.setattr("__main__.GLOBAL_VAR", "patched_value")` changes `GLOBAL_VAR` temporarily.

---

## 3. Mocking an External Function
When testing a function that calls an external API, you can **mock** it.

### Example: Mocking `requests.get()`
```python
import requests
import pytest

def fetch_data():
    response = requests.get("https://example.com/api")
    return response.status_code

def test_fetch_data(monkeypatch):
    class MockResponse:
        status_code = 200

    def mock_get(url):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    
    assert fetch_data() == 200
```
- This prevents real API calls and returns a **mock response**.

---

## 4. Modifying Environment Variables using `monkeypatch.setenv`
You can **mock environment variables** for testing.

### Example: Mocking `os.getenv()`
```python
import os
import pytest

def get_api_key():
    return os.getenv("API_KEY", "default_key")

def test_get_api_key(monkeypatch):
    monkeypatch.setenv("API_KEY", "mocked_key")
    
    assert get_api_key() == "mocked_key"
```
- `monkeypatch.setenv("API_KEY", "mocked_key")` changes the environment variable.

---

## 5. Preventing Function Calls using `monkeypatch.delattr`
To **disable a function** during a test, use `monkeypatch.delattr()`.

### Example: Disabling `os.remove()`
```python
import os
import pytest

def delete_file(filename):
    os.remove(filename)

def test_delete_file(monkeypatch):
    monkeypatch.delattr(os, "remove")  # This disables os.remove()
    
    with pytest.raises(AttributeError):  # os.remove() no longer exists
        delete_file("test.txt")
```
- `monkeypatch.delattr(os, "remove")` **removes** `os.remove()` temporarily.

---

## Summary of Key `monkeypatch` Methods

| Method | Purpose |
|---------|---------|
| `monkeypatch.setattr(obj, "attribute", new_value)` | Replace an attribute or function. |
| `monkeypatch.delattr(obj, "attribute")` | Delete an attribute or function. |
| `monkeypatch.setenv("VAR", "value")` | Set an environment variable. |
| `monkeypatch.delenv("VAR")` | Delete an environment variable. |

