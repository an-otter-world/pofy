# Pofy (Python yaml objects)

[![WTFPL license](https://img.shields.io/badge/License-WTFPL-blue.svg)](https://raw.githubusercontent.com/an-otter-world/pofy/master/COPYING)
[![Actions Status](https://github.com/an-otter-world/pofy/workflows/Checks/badge.svg)](https://github.com/an-otter-world/pofy/actions)
[![Coverage Status](https://coveralls.io/repos/github/an-otter-world/pofy/badge.svg)](https://coveralls.io/github/an-otter-world/pofy)
[![Matrix](https://img.shields.io/matrix/python-pofy:matrix.org?server_fqdn=matrix.org)](https://matrix.to/#/!SwCyFpSTQTLiPCNKTO:matrix.org?via=matrix.org)

Pofy is a tiny library allowing to declare classes that can be deserialized
from YAML, using pyyaml. Classes declares a schema as a list of fields, used
to validate data during deserialization. Features include YAML inclusion,
custom fields & validation.

Pofy is distributed under the term of the WTFPL V2 (See COPYING file).

Contribution are very welcome. Don't hesitate to send pull requests. As English
isn't my native language, I'd be very happy with documentation correction or
improvements. Feel free to join [the Pofy channel on Matrix](https://matrix.to/#/!SwCyFpSTQTLiPCNKTO:matrix.org?via=matrix.org).

- [Pofy (Python yaml objects)](#pofy-python-yaml-objects)
  - [Installation](#installation)
  - [Quickstart](#quickstart)
  - [Reference](#reference)
    - [Fields](#fields)
      - [Common Parameters](#common-parameters)
      - [BoolField](#boolfield)

## Installation

Pofy is tested with Python 3.8. It be installed through pip :

  `pip install pofy`

## Quickstart

To use Pofy, you must declare a schema in the class you want to deserialize :

  ```python
      from pofy import StringField, load

      class Test:
          class Schema:
              field = StringField()

      test = load(SomeObject, 'field: value')
      assert test.field == 'value`
  ```

## Reference

### Fields

Pofy fields are defined in a 'Schema' inner class of the object you want to
deserialize. Pofy comes with predefined fields described below. You can
declare custom fields, to do so, refer to the [Custom Fields][#custom-fields]
section.

#### Common Parameters

All field types accept a 'required' boolean parameter. If it's set and the
field is not declared when loading a YAML document, a
MissingRequiredFieldError will be raised, or the [error handler](#error-handler)
you defined will be called with ErrorCode.MISSING_REQUIRED_FIELD as the
error_code parameter :

```python
  from pofy import StringField, load

  class Test:
    class Schema:
      required_field = StringField(required=True)
      optional_field = StringField()

  load('optional_field: some_value', Test) # Raises MissingRequiredFieldError
```

All field types accept a 'validate' parameter. It's meant to be a python
callable object accepting a ILoadingContext and the field deserialized
object, and returning a boolean. If the returned value is False, pofy will
raise a ValidationError or the [error handler](#error-handler) you defined will
be called with ErrorCode.VALIDATION_ERROR as the error_code parameter. Notice
that whole loaded objects can also be validated.

```python
  from pofy import StringField, load

  def _validate(context, value):
    if value not in ['red', 'green', 'blue']:
      return False

    return True

  class Test:
    class Schema:
      color = StringField()

  load('color: yellow', Test) # Raises ValidationError
  load('color: blue', Test) # Raises ValidationError
```

#### BoolField

BoolField loads a boolean from YAML. No additional parameter is available. The following values are accepted when loading a YAML object :

- For true : y, Y, yes, Yes, YES, true, True, TRUE, on, On, ON
- For false : n, N, no, No, NO, false, False, FALSE, off, Off, OFF

Any other value will raise a ValidationError, or call the defined error_handler
with VALIDATION_ERROR as the error_code parameter.

```python
  from pofy import BoolField, load

  class Test:
    class Schema:
      some_flag = BoolField()

  test = load('some_flag: on', Test)
  assert test.some_flag
  test = load('some_flag: NotValid', Test) # Raises ValidationError
```
