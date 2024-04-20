# Extended Plain String Object Notation

## Usage

### Convert from JSON file

```
$ python -m epson.json2epson <json_file >epson_file
```

### Convert to JSON file

```
$ python -m epson.epson2json <epson_file >json_file
```

## Notation Example

### JSON multi-line string

```
{
    "key": "line1\nline2\nline3\n"
}
```

### EPSON multi-line string

Like a shell-script's here-document...

```
{
    "key": "".
line1
line2
line3

.
}
```

In above example, period character (.) is guard-string.

And if you carefully choose guard-string, you will put raw-binary data as string.

## Syntax

* any [JSON Syntax](https://www.json.org/)
* multi-line-string
    * '"' '"' guard-string '\n' raw-string '\n' guard-string '\n'
        * former guard-sting and later one MUST be same sequence of characters
        * line-feed characters (\n) around raw-string are exclusive of raw-string self
* guard-string
    * characters
* raw-string
    * raw-characters
* raw-characters
    * raw-character raw-characters
* raw-character
    * character
    * ws
