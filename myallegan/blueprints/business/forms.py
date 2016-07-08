from collections import OrderedDict

from flask_wtf import Form
from wtforms import (
  SelectField,
  TextField,
  StringField,
  BooleanField,
  IntegerField,
  FloatField,
  DateTimeField
)
from wtforms.validators import (
  DataRequired,
  Length,
  Optional,
  Regexp,
  NumberRange
)
from flask_wtf.file import (
  FileField,
  FileAllowed,
  FileRequired
)
from wtforms_components import Unique

from lib.util_wtforms import ModelForm, choices_from_dict


class BusinessForm(ModelForm):
    #Details.
    title = StringField(validators=[
        DataRequired(),
        Length(1, 255)
    ])

    # Relationships
    # ...
