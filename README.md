# Requirements

## Ubuntu/Debian

```
apt-get update
apt-get install -y python3 python3-pip
cd /path/to/sources/where/requirements.txt/resides
pip install -r requirements.txt
```

# Testing

```
python -m unittest -v discover
```

# Start

```
python queue_manager.py \
--agents <Number_of_Agents>
--callers <Number_of_Callers>
```

Example:

```
python queue_manager.py --agents 2 --callers 5
```