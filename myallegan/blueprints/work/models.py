from collections import OrderedDict

from sqlalchemy import or_

from myallegan.extensions import db
from lib.util_sqlalchemy import ResourceMixin

from myallegan.models import Business


class Work(ResourceMixin, db.Model):
    __tablename__ = 'work'
    id = db.Column(db.Integer, primary_key=True)

    # Enums
    EMPLOYMENT_STATUS = OrderedDict([
        ('part', 'Part-Time'),
        ('full', 'Full-Time'),
        ('casual', 'Casual'),
        ('intern', 'Internship')
    ])

    # Relationships
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'),
                            index=True, nullable=False)

    # Details
    title = db.Column(db.String(128), nullable=False, index=True)
    salary = db.Column(db.Float())
    employment_status = db.Column(db.Enum(*EMPLOYMENT_STATUS, name='role_types', 
        native_enum=False), index=True, nullable=False, server_default='part')


    # Properties
    @property
    def status_title(self):
        return self.EMPLOYMENT_STATUS[self.employment_status]

    @property
    def salary_text(self):
        return '%.2f' % self.salary

    @property
    def business(self):
        business = Business.query.get(self.business_id)
        return business


    # Standard methods
    def __init__(self, **kwargs):
        super(Work, self).__init__(**kwargs)


    @classmethod
    def create(cls, params):
        """Initialize a new Work, and commit it to the database.

        Args:
            params (dict): **kwargs for `__init__`-method.

        Returns:
            bool: True if succesful, otherwise SQLAlchemy will raise an exception.

        """

        db.session.add(Work(**params))
        db.session.commit()

        return True


    @classmethod
    def search(cls, query):
        """This is a generalized search-field for Work.
        Seperate methods should be written for more specificity.

        Args:
            query (str)

        Returns:
            result

        """

        if not query:
            return ''

        search_query = '%{0}%'.format(query)
        search_chain = (Work.title.ilike(search_query),
                        None)

        if search_chain[-1] is None:
            return or_(*search_chain[0])
        else:
            return or_(*search_chain)
