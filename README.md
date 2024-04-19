# Extended Plain String Object Notation

## Example

### JSON multi-line string

```
{
    "key": "line1\nline2\nline3\n"
}
```

### EPSON multi-line string

like a shell-script's here-document...

```
{
    "key": "".
line1
line2
line3

.
}
```

## Syntax

* any JSON Syntax
* multi-line-string
    * '"' '"' guard-string '\n' raw-string '\n' guard-string '\n'
        * former guard-sting and later one MUST be same sequence of characters
        * line-feed characters (\n) around raw-string are exclusive of raw-string
* guard-string
    * characters
* raw-string
    * raw-characters
* raw-characters
    * raw-character raw-characters
* raw-character
    * character
    * ws
