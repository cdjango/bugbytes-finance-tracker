```sh
uv init --bare --python 3.15
uv add -r <(
  if file -bi requirements.txt | grep -qi "utf-16"; then
    iconv -f UTF-16 -t UTF-8 requirements.txt
  else
    cat requirements.txt
  fi | sed 's/==/>=/g'
)

find . -path "*/migrations/*.py" ! -path '*/.venv/*' -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
find . -path "*.*" -name "db.sqlite3" -delete
find ~ \( -path '*/__pycache__/*' -o -name __pycache__ \) -delete

uv lock --upgrade
uv sync --locked

uv run manage.py makemigrations users tracker
uv run manage.py migrate
uv run manage.py createsuperuser --username admin --email admin@admin.com
uv run manage.py generate_transactions
uv run manage.py runserver
```
