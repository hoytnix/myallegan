# Locals
from myallegan.models import Business

from myallegan.extensions import db
from lib.util_sqlalchemy import ResourceMixin

# Globals
from collections import OrderedDict
from math import ceil, floor

from sqlalchemy import or_


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
    salary_percentile = db.Column(db.Integer, nullable=False, default=1)
    employment_status = db.Column(db.Enum(*EMPLOYMENT_STATUS, name='role_types', 
        native_enum=False), index=True, nullable=False, server_default='part')


    # Properties
    @property
    def status_title(self):
        return self.EMPLOYMENT_STATUS[self.employment_status]

    @property
    def salary_text(self):
        if self.salary:
            return '%d' % self.salary
        else:
            return None

    @property
    def business(self):
        business = Business.query.get(self.business_id)
        return business



    # Salary Percentiles ------------------------------------------------------             
    @classmethod
    def init_update_percentiles(cls):
        from myallegan.tasks import adjust_salary_percentile
        adjust_salary_percentile.delay()

    @classmethod
    def update_percentiles(cls):
        jobs = Work.query.order_by(Work.salary.asc(), Work.id.asc()).all()
        jobs_total = jobs.__len__()

        odd = jobs_total % 3
        each = jobs_total / 3
        if odd is 1: 
            amts = {1: floor(each), 2: ceil(each), 3: floor(each)}
        elif odd is 2:
            amts = {1: ceil(each), 2: ceil(each), 3: floor(each)}
        else:
            amts = {1: each, 2: each, 3: each}
        
        percentile = 1
        counter = 0
        for job in jobs:
            counter += 1

            cls.update_percentile(job.id, percentile)

            if counter == amts[percentile]:
                percentile += 1
                counter = 0

    @classmethod
    def update_percentile(cls, id, value):
        Work.query.filter(Work.id==id).update({'salary_percentile': value})
        db.session.commit()


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
        
        cls.init_update_percentiles()

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
