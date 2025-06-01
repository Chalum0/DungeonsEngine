from packages.world.entities.EntityTemplate import EntityTemplate
# from packages.world.Entities import *
import time
import numpy as np
from numba import njit


class EntityManager:
    def __init__(self):
        self._max_entities = 500_000
        self._current_eid = 0
        self._entity_overflow_mode = "override"  # override, refuse, error

        self._entities = []
        self._available_eids = []
        self._eid = 0


    def change_max_entity(self, amount: int) -> None:
        """This changes the maximum amount of entities the scene can have simultaneously !!! and removes all current entities !!!"""
        if amount > 0:
            self._max_entities = amount
            self._current_eid = 0
            self._entities = []

    def reset_max_entity(self) -> None:
        """Set the maximum amount of entities the scene can have simultaneously back to 500 000."""
        self._max_entities = 500_000

    def update(self):
        entity_count = len(self._entities) if len(self._entities) == self._max_entities else self._eid

        for i in range(entity_count):
            pass

    def create_entity(self, entity: EntityTemplate) -> None:
        """ In the array, entities are tuples. they are in the following way: ( ) """

        eid = self._next_eid()
        if eid >= self._max_entities:
            if self._entity_overflow_mode == "override":
                eid = 0
                self._eid = 0
            elif self._entity_overflow_mode == "refuse":
                return
            elif self._entity_overflow_mode == "error":
                raise TooManyEntities()
            else:
                raise UnknownOverflowMode()

        e = None
        if eid > len(self._entities) - 1:
            self._entities.append(e)

        else:
            self._entities[eid] = e

        self._eid += 1






    def _next_eid(self) -> int:
        if len(self._available_eids) > 0:
            return self._available_eids.pop()
        else:
            return self._eid

    def delete_entity(self, eid) -> None:
        if len(self._entities) >= eid + 1:
            self._entities[eid] = 0
            self._available_eids.append(eid)


    def set_entity_overflow_to_override(self) -> None:
        """If more entities are created than the maximum amount defined, first entities created will be removed to create the new ones."""
        self._entity_overflow_mode = "override"
    def set_entity_overflow_to_refuse(self) -> None:
        """If more entities are created than the maximum amount defined, attempting to create a new one will have no effect."""
        self._entity_overflow_mode = "refuse"
    def set_entity_overflow_to_error(self) -> None:
        """If more entities are created than the maximum amount defined, attempting to create a new one will throw an error."""
        self._entity_overflow_mode = "error"


class TooManyEntities(Exception):
    def __init__(self):
        super().__init__(
            f'Too many entities are appearing in the scene and overflow mode is set to throw an error. Try changing overflow mode with the EntityManager.set_entity_overflow_to_refuse() or EntityManager.set_entity_overflow_to_override() methods.'
        )

class UnknownOverflowMode(Exception):
    def __init__(self):
        super().__init__(
            f'Too many entities are appearing in the scene and overflow mode has been changed manually to an unknown value. Avoid changing overflow mode manually.'
        )
