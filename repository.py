import abc
import pickle
import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        self.session.add(batch)

    def get(self, reference):
        return self.session.query(model.Batch).filter_by(reference=reference).one()

    def list(self):
        return self.session.query(model.Batch).all()

class PickleRepository(AbstractRepository):
    '''Complete the definition of this class.'''
    def __init__(self, path=None):
        self._path = path
        try:
            with open (path, 'rb') as f:
                self._data = pickle.load(f)
        except IOError:
            self._data = dict()
        
    def add(self, batch):
        self._data[batch.reference] = batch
        # save
        if self._path:
            with open (self._path, 'wb') as f:
                pickle.dump(self._data, f)

    def get(self, reference):
        return self._data[reference]

    def list(self):
        return self._data.values()
