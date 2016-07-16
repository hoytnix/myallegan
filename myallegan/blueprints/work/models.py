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
            return '$%.2f' % self.salary
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
        # Configuration.
        _PERCENTILE_CONFIG = 3  # Nice balance of clean and info.
        _PERCENTILES = range(1, _PERCENTILE_CONFIG + 1)

        jobs = Work.query.order_by(Work.salary.asc(), Work.id.asc()).all()
        jobs_total = jobs.__len__()

        salaries = {}
        for job in jobs:
            key = job.salary
            if key:
                if key not in salaries:
                    salaries[key] = 1
                else:
                    salaries[key] += 1
            else:
                jobs_total -= 1
        salaries = OrderedDict(sorted(salaries.items()))

        # members, member count
        percentiles = {}
        for _PERCENTILE in _PERCENTILES:
            percentiles[_PERCENTILE] = [[], 0]
        
        percentile_counter = 1
        for salary in salaries:
            members = salaries[salary] 
            percentile = percentiles[percentile_counter]

            percentile[0].append(salary)
            percentile[1] += members

            count = percentile[1]
            jobs_available = jobs_total
            if percentile_counter > 1:
                for k in range(1, percentile_counter):
                    jobs_available -= percentiles[k][1]

            if percentile_counter < _PERCENTILE_CONFIG:
                r = count / ((1 / ((_PERCENTILE_CONFIG + 1) - percentile_counter)) * jobs_available)
                if r > 1:
                    percentile_counter += 1

        for job in jobs:
            for percentile_key in percentiles:
                percentile = percentiles[percentile_key]
                if job.salary in percentile[0]:
                    cls.update_percentile(job.id, percentile_key)


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
            return or_(search_chain[0])
        else:
            return or_(*search_chain)
