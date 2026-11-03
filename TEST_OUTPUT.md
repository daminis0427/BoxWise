# BoxWise – Test Execution Output

## 1. Django System Check

**Command:**

```bash
python manage.py check
```

**Actual Output:**

```text
System check identified no issues (0 silenced).
```

**Status:** PASSED

---

## 2. Automated Test Execution

**Command:**

```bash
python manage.py test boxes
```

**Actual Output:**

```text
Found 22 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......................
----------------------------------------------------------------------
Ran 22 tests in 0.315s

OK
Destroying test database for alias 'default'...
```

**Status:** PASSED

### Test Summary

| Metric | Result |
|---|---|
| Total tests discovered | 22 |
| Tests passed | 22 |
| Tests failed | 0 |
| Execution time | 0.315 seconds |
| Overall status | PASSED |

---

## 3. Development Server Execution

**Command:**

```bash
python manage.py runserver
```

**Observed Output:**

```text
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 6.1.2, using settings 'config.settings'
Starting WSGI development server at http://127.0.0.1:8000/
```

**Status:** STARTED

---

## 4. Features Covered by Automated Tests

The 22 automated tests cover the following areas:

### Product and Shipping Box Management
- Product creation
- Shipping box creation

### Product Packing
- Product orientation and rotation
- Product fitting inside available space
- Successful product packing
- Failed packing when products cannot fit
- Packing with no shipping box
- Empty order handling
- Multiple product quantities

### Box Recommendation
- Finding suitable shipping boxes
- Checking shipping box weight restrictions
- Recommending the cheapest suitable box
- Handling cases where no suitable box exists

### Cost Optimization
- Calculating potential cost savings
- Calculating savings percentage
- Handling orders without suitable shipping boxes

### Django Web Pages
- Home page loading
- Displaying orders on the home page
- Recommendation page loading
- Displaying the recommended shipping box
- Handling missing orders with a 404 response
- Calculating packing analysis metrics

---

## 5. Final Test Result

The BoxWise Django application passed all 22 automated tests.

The Django system check reported no configuration issues, and the development server started successfully.

**Final Result: PASSED**

