from sqlalchemy import or_

from myallegan.extensions import db
from lib.util_sqlalchemy import ResourceMixin


class Business(ResourceMixin, db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)


    # Relationships.
    # ...


    # Details.
    title = db.Column(db.String(128), nullable=False, index=True)


    def __init__(self, **kwargs):
        super(Business, self).__init__(**kwargs)


    @classmethod
    def create(cls, params):
        """Initialize a new Business, and commit it to the database.

        Args:
            params (dict): **kwargs for `__init__`-method.

        Returns:
            bool: True if succesful, otherwise SQLAlchemy will raise an exception.

        """

        db.session.add(Business(**params))
        db.session.commit()

        return True


    @classmethod
    def search(cls, query):
        """This is a generalized search-field for Businesses.
        Seperate methods should be written for more specificity.

        Args:
            query (str)

        Returns:
            result

        """

        if not query:
            return ''

        search_query = '%{0}%'.format(query)
        search_chain = (Business.title.ilike(search_query))

        return or_(*search_chain)
