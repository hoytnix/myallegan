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


class SearchForm(Form):
    q = StringField('Search terms', [Optional(), Length(1, 256)])


class BulkDeleteForm(Form):
    SCOPE = OrderedDict([
        ('all_selected_items', 'All selected items'),
        ('all_search_results', 'All search results')
    ])

    scope = SelectField('Privileges', [DataRequired()],
                        choices=choices_from_dict(SCOPE, prepend_blank=False))
