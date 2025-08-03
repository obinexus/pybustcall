# Install package
pip install -e .

# Basic usage
python -c "
from pybustcall import BustcallClient
client = BustcallClient()
result = client.bust_cache('assets/main.css')
print(f'Cache bust: {result.success}')
"
