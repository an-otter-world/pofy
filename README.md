# Pyyo (Python yaml objects)

## Overview

Pyyo is a tiny library allowing to declare classes that can be deserialized
from YAML, using pyyaml. Classes declares a schema as a list of fields, used
to check for data validation during deserialization.

Pyyo is distributed under the term of the WTFPL V2 (See COPYING file).

## Installation

Pyyo is tested with Python 3.8. It be installed through pip :

  `pip install pyyo`

## Quickstart

To use Pyyo, you must declare a schema in the class you want to deserialize :

  ```python
      from pyyo import StringField, load

      class SomeObject:
          class Schema:
              field = StringField()

      deserialized_object = load(SomeObject, 'field: value')
      assert deserialized_object.field == 'value`
  ```

## Reference

### Fields

#### Common parameters

#### StringField

#### IntField

#### DictField

#### ListField

#### ObjectField

### Tags

#### '!include' Tag

#### '!class' Tag

### Validation

### load options

## Contributing
