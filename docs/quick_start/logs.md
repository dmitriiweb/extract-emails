# Logs

There is [loguru](https://github.com/Delgan/loguru) library under the hood.

## Settings
```python
import sys

from loguru import logger

logger.add(
    sys.stderr,
    format="{time} {level} {message}",
    filter="my_module",
    level="INFO",
)
```

## Disable/Enable
```python
from loguru import logger

logger.disable('extract_emails')
logger.enable('extract_emails')
```
