## Steps to Check Code Coverage

Install Requirements.
```
pip install -r requirements.txt
```

To run coverage for both the applications.
```
python -m coverage run --source=info,search --omit=*/migrations/* ./manage.py test
```

To generate the report of coverage from above coverage run.
```
python -m coverage report
```

To generate index.html in htmlcov
```
python -m coverage html
```