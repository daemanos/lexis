# Lexis

Utilities for writing dictionaries in Markdown.

## panick

panick is a pandoc filter that auto-collates a dictionary from Markdown source.
The source consists of a dictionary list, like so:

```markdown
read
  ~ to speak aloud words or other information that is written
  ~ to consist of certain text
  ~ of text, etc., to be interpreted or read in a particular way

write
  ~ to form letters, words, or symbols on a surface in order to communicate
  ~ to be the author of (a book, article, poem, etc.)
  ~ to be an author
```

Optionally, you can specify a `sort_order` parameter in the front-matter which
specifies a custom collation. For example, the default value is:

```yaml
---
sort_order:
    - "a"
    - "b"
    - "c"
    - "d"
    ...
    - "z"
---
```

The elements of the list can be either single characters or lists of
characters, in which case all elements of the list will be treated equally.
