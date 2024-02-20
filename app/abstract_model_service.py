from abc import ABCMeta

from sqlalchemy import func, inspect
from sqlalchemy.orm import Session

from app.database import Base


class AbstractModelService(metaclass=ABCMeta):
    _model: Base

    @classmethod
    def create(cls, session: Session, **attrs):
        """
        Create model instance

        Args:
            session: session to use
            **attrs: model attributes values

        Returns:
            models.Model
        """
        instance = cls._model(**attrs)
        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def list(cls, session: Session, attributes, **filters):
        """
        List model instances

        Args:
            session: session to use
            attributes: attributes to select
            **filters: model filters

        Returns:
            QuerySet
        """
        return session.query(
            *[getattr(cls._model, attr) for attr in attributes]
        ).filter_by(**filters)

    @classmethod
    def list_json(
        cls,
        session: Session,
        json_object_name: str,
        attributes: dict,
        singleton_filters=None,
        **filters
    ):
        """
        List model instances in json format

        Args:
            session: session to use
            json_object_name: name of the json object
            attributes: attributes to select
            singleton_filters: list of filters to apply on the json object
            **filters: list of model filters

        Returns:
            Json list
        """
        # for each attribute, we get the column name and the desired name
        if singleton_filters is None:
            singleton_filters = []
        object_to_build = []
        for key, value in attributes.items():
            column = getattr(cls._model, value)
            object_to_build.extend([key, column])
        return (
            session.query(
                func.json_build_object(
                    json_object_name,
                    func.json_agg(
                        func.json_build_object(
                            *object_to_build,
                        )
                    ),
                )
            )
            .filter(*singleton_filters)
            .filter_by(**filters)
            .scalar()
        )

    @classmethod
    def get(cls, session: Session, attributes: list, **filters):
        """
        Get model instance

        Args:
            session: session to use
            attributes: attributes to select
            **filters: model filters

        Returns:
            QuerySet
        """
        result = (
            session.query(*[getattr(cls._model, attr) for attr in attributes])
            .filter_by(**filters)
            .first()
        )
        if result:
            return result._mapping

    @classmethod
    def get_json(cls, session: Session, attributes: dict, **filters):
        """
        Get model instance in json format

        Args:
            session: session to use
            attributes: attributes to select
            **filters: list of model filters

        Returns:
            Json
        """
        # for each attribute, we get the column name and the desired name
        object_to_build = []
        for key, value in attributes.items():
            column = getattr(cls._model, value)
            object_to_build.extend([key, column])
        return (
            session.query(
                func.json_build_object(
                    *object_to_build,
                )
            )
            .filter_by(**filters)
            .scalar()
        )

    @classmethod
    def delete_by_pk(cls, session: Session, pk):
        """
        Delete a model by is primary key

        Args:
            session: session to use
            pk: model pk to delete
        """
        pk_name = inspect(cls._model).primary_key[0].name
        if isinstance(pk_name, list):
            pk_name = pk_name[0]
        session.query(cls._model).filter(getattr(cls._model, pk_name) == pk).delete()
        session.commit()

    @classmethod
    def get_by_pk(cls, session: Session, pk):
        """
        Get a model by is primary key

        Args:
            session: session to use
            pk: model pk to get
        """
        pk_name = inspect(cls._model).primary_key[0].name
        if isinstance(pk_name, list):
            pk_name = pk_name[0]
        return (
            session.query(cls._model).filter(getattr(cls._model, pk_name) == pk).one()
        )

    @classmethod
    def get_if_exists(cls, session: Session, **filters):
        """
        Get model instance if it exists
        If not, return None

        Args:
            session: session to use
            **filters: model filters

        Returns:
            QuerySet, None
        """
        return session.query(cls._model).filter_by(**filters).one_or_none()

    @classmethod
    def update(cls, session: Session, filters: dict, values: dict):
        """
        Update model instance

        Args:
            session: session to use
            filters: model filters to update
            values: model values to update

        Returns:
            QuerySet
        """
        query = session.query(cls._model).filter_by(**filters).update(values)
        session.commit()
        return query
