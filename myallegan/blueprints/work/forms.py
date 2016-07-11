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

from myallegan.models import Work


class WorkForm(ModelForm):
    #Details.
    title = StringField(validators=[
        DataRequired(),
        Length(1, 255)
    ])
    salary = FloatField(validators=[Optional(), NumberRange(min=0.01, max=100)])
    employment_status = SelectField('Employment Status', [DataRequired()],
            choices=choices_from_dict(Work.EMPLOYMENT_STATUS, prepend_blank=False))

    # Relationships
    business_id = IntegerField('Business ID', [DataRequired(), 
                                            NumberRange(min=1, max=2147483647)])
