# python-secrules
# OWASP CRS Rules parser

Incomplete parser model and sample application for parsing [Core Rule Set](https://github.com/coreruleset/coreruleset/) written in the ModSecurity DSL SecRule language. It uses the python library [textX](http://www.igordejanovic.net/textX/) for parsing.

## How to use it (CLI):

1. Install dependencies
    Dependencies can be installed system-wide, or just for your user (using `--user`).

    System-wide:
    ```shell
    sudo pip install secrules
    ```
    User:
    ```shell
    pip install --user secrules
    ```

2. Import the library
```python
from secrules import SecRuleParser

config = SecRuleParser().read('../rules/*.conf')
rules = config.__secrules__
rule = rules[0]
rule = rule.actions, rule.operator, rule.variables
```
