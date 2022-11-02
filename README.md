# JSONC

Parser for JSONC (JSON with comments) files.

## Example

```python
from jsonc import loads

print(
    loads(
        """
        {
            // This is a comment
            "foo": "bar", // This is another comment
        }
        """,
        allow_trailing_comma=True,
    )
)  # {'foo': 'bar'}
```
