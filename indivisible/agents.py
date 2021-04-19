#!python3

"""
Defines agents with various kinds of valuation functions over indivisible items.

Programmer: Erel Segal-Halevi
Since: 2020-04
"""

from fairpy.indivisible.valuations import *

from abc import ABC, abstractmethod
from typing import *
Item = Any
Bundle = Set[Item]


class Agent(ABC):
    """
    An abstract class that describes a participant in an algorithm for indivisible item allocation.
    It can evaluate a set of items.
    It may also have a name, which is used only in demonstrations and for tracing. The name may be left blank (None).

    Optionally, it can also represent several agents with an identical valuation function.
    """

    def __init__(self, valuation:Valuation, name:str=None, duplicity:int=1):
        """
        :param valuation: represents the agents' valuation function.
        :param name [optional]: a display-name for the agent in logs and printouts.
        :param duplicity [optional]: the number of agent/s with the same valuation function.
        """
        self.valuation = valuation
        if name is not None:
            self._name = name
        self.duplicity = duplicity

    def name(self):
        if hasattr(self, '_name') and self._name is not None:
            return self._name
        else:
            return "Anonymous"

    def value(self, bundle:Bundle)->float:
        return self.valuation.value(bundle)

    def total_value(self)->float:
        return self.valuation.total_value()


    def best_index(self, allocation:List[Bundle])->int:
        """
        Returns an index of a bundle that is most-valuable for the agent.
        :param   partition: a list of k sets.
        :return: an index in [0,..,k-1] that points to a bundle whose value for the agent is largest.
        If there are two or more best bundles, the first index is returned.

        >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 3})
        >>> a.best_index(["xy","z"])
        0
        >>> a.best_index(["y","xz"])
        1
        """
        return self.valuation.best_index(allocation)


    def value_except_best_c_goods(self, bundle:Bundle, c:int=1)->int:
        """
        Calculates the value of the given bundle when the "best" (at most) c goods are removed from it.
        Formally, it calculates:
              min [G subseteq bundle] value (bundle - G)
        where G is a subset of duplicity at most c.
        This is a subroutine in checking whether an allocation is EF1.

        >>> a = MonotoneAgent({"x": 1, "y": 2, "xy": 4})
        >>> a.value_except_best_c_goods(set("xy"), c=1)
        1
        >>> a.value_except_best_c_goods(set("xy"), c=2)
        0
        >>> a.value_except_best_c_goods(set("x"), c=1)
        0
        >>> a.value_except_best_c_goods(set(), c=1)
        0
        """
        return self.valuation.value_except_best_c_goods(bundle,c)

    def value_except_worst_c_goods(self, bundle:Bundle, c:int=1)->int:
        """
        Calculates the value of the given bundle when the "worst" c goods are removed from it.
        Formally, it calculates:
              max [G subseteq bundle] value (bundle - G)
        where G is a subset of duplicity at most c.
        This is a subroutine in checking whether an allocation is EFx.

        >>> a = MonotoneAgent({"x": 1, "y": 2, "xy": 4})
        >>> a.value_except_worst_c_goods(set("xy"), c=1)
        2
        """
        return self.valuation.value_except_worst_c_goods(bundle,c)


    def values_1_of_c_partitions(self, c:int=1):
        """
        Generates the minimum values in all partitions into c bundles.

        >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 4, "w":0})
        >>> sorted(a.values_1_of_c_partitions(c=2))
        [1, 2, 3]

        """
        return self.valuation.values_1_of_c_partitions(c)


    def value_1_of_c_MMS(self, c:int=1)->int:
        """
        Calculates the value of the 1-out-of-c maximin-share ( https://en.wikipedia.org/wiki/Maximin-share )

        >>> a = MonotoneAgent({"x": 1, "y": 2, "xy": 4})
        >>> a.value_1_of_c_MMS(c=1)
        4
        >>> a.value_1_of_c_MMS(c=2)
        1
        >>> a.value_1_of_c_MMS(c=3)
        0
        >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 4, "w":0})
        >>> a.value_1_of_c_MMS(c=2)
        3
        """
        return self.valuation.value_1_of_c_MMS(c)

    def partition_1_of_c_MMS(self, c: int, items: list) -> List[Bundle]:
        return self.valuation.partition_1_of_c_MMS(c, items)


    def value_proportional_except_c(self, num_of_agents:int, c:int):
        """
        Calculates the proportional value of that agent, when the c most valuable goods are ignored.
        This is a subroutine in checking whether an allocation is PROPc.
        """
        return self.valuation.value_proportional_except_c(num_of_agents, c)

    def is_EFc(self, own_bundle:Bundle, all_bundles:List[Bundle], c: int) -> bool:
        """
        Checks whether the current agent finds the given allocation envy-free-except-c-goods (EFc).
        :param own_bundle:   the bundle consumed by the current agent.
        :param all_bundles:  the list of all bundles.
        :return: True iff the current agent finds the allocation EFc.
        """
        return self.valuation.is_EFc(own_bundle, all_bundles, c)

    def is_EF1(self, own_bundle:Bundle, all_bundles:List[Bundle]) -> bool:
        """
        Checks whether the current agent finds the given allocation envy-free-except-1-good (EF1).
        :param own_bundle:   the bundle given to the family of the current agent.
        :param all_bundles:  a list of all bundles.
        :return: True iff the current agent finds the allocation EF1.
        """
        return self.valuation.is_EF1(own_bundle, all_bundles)

    def is_EFx(self, own_bundle:Bundle, all_bundles:List[Bundle])->bool:
        """
        Checks whether the current agent finds the given allocation EFx.
        :param own_bundle:   the bundle given to the family of the current agent.
        :param all_bundles:  a list of all bundles.
        :return: True iff the current agent finds the allocation EFx.
        """
        return self.valuation.is_EFx(own_bundle, all_bundles)

    def is_EF(self, own_bundle:Bundle, all_bundles:List[Bundle])->bool:
        """
        Checks whether the current agent finds the given allocation envy-free.
        :param own_bundle:   the bundle given to the family of the current agent.
        :param all_bundles:  a list of all bundles.
        :return: True iff the current agent finds the allocation envy-free.
        """
        return self.valuation.is_EF(own_bundle, all_bundles)

    def is_1_of_c_MMS(self, own_bundle:Bundle, c:int, approximation_factor:float=1)->bool:
        return self.valuation.is_1_of_c_MMS(own_bundle, c, approximation_factor)

    def is_PROPc(self, own_bundle:Bundle, num_of_agents:int, c:int)->bool:
        """
        Checks whether the current agent finds the given allocation PROPc
        When there are k agents, an allocation is PROPc for an agent
        if his value for his own bundle is at least 1/k of his value for the following bundle:
            [all the goods except the best c].
        :param own_bundle:   the bundle consumed by the current agent.
        :param num_of_agents:  the total number of agents.
        :param c: how many best-goods to exclude from the total bundle.
        :return: True iff the current agent finds the allocation PROPc.
        """
        return self.valuation.is_PROPc(own_bundle, num_of_agents, c)

    def is_PROP(self, own_bundle:Bundle, num_of_agents:int)->bool:
        """
        Checks whether the current agent finds the given allocation proportional.
        :param own_bundle:     the bundle consumed by the current agent.
        :param num_of_agents:  the total number of agents.
        :return: True iff the current agent finds the allocation PROPc.
        """
        return self.valuation.is_PROP(own_bundle, num_of_agents)

    def __repr__(self):
        if self.duplicity==1:
            return f"{self.name()} is an agent with a {self.valuation.__repr__()}"
        else:
            return f"{self.name()} are {self.duplicity} agents with a {self.valuation.__repr__()}"



class MonotoneAgent(Agent):
    """
    Represents an agent or several agents with a general monotone valuation function.

    >>> a = MonotoneAgent({"x": 1, "y": 2, "xy": 4}, name="Alice")
    >>> a
    Alice is an agent with a Monotone valuation on ['x', 'y'].
    >>> a.value("")
    0
    >>> a.value({"x"})
    1
    >>> a.value("yx")
    4
    >>> a.value({"y","x"})
    4
    >>> a.is_EF({"x"}, [{"y"}])
    False
    >>> a.is_EF1({"x"}, [{"y"}])
    True
    >>> a.is_EFx({"x"}, [{"y"}])
    True
    >>> MonotoneAgent({"x": 1, "y": 2, "xy": 4}, duplicity=2)
    Anonymous are 2 agents with a Monotone valuation on ['x', 'y'].

    """
    def __init__(self, map_bundle_to_value:Dict[Bundle,float], name:str=None, duplicity:int=1):
        """
        Initializes an agent with a given valuation function.
        :param map_bundle_to_value: a dict that maps each subset of goods to its value.
        :param duplicity: the number of agents with the same valuation.
        """
        super().__init__(MonotoneValuation(map_bundle_to_value), name, duplicity)


class AdditiveAgent(Agent):
    """
    Represents an agent or several agents with an additive valuation function.

    >>> a = AdditiveAgent({"x": 1, "y": 2, "z": 4, "w":0}, name="Alice")
    >>> a
    Alice is an agent with a Additive valuation: w=0 x=1 y=2 z=4.
    >>> a.value(set())
    0
    >>> a.value({"w"})
    0
    >>> a.value({"x"})
    1
    >>> a.value("yx")
    3
    >>> a.value({"y","x","z"})
    7
    >>> a.is_EF({"y"}, [{"y"},{"x"},{"z"},set()])
    False
    >>> a.is_PROP({"y"}, 4)
    True
    >>> a.is_PROP({"y"}, 3)
    False
    >>> a.is_PROPc({"y"}, 3, c=1)
    True
    >>> a.is_EF1({"y"}, [{"x","z"}])
    True
    >>> a.is_EF1({"x"}, [{"y","z"}])
    False
    >>> a.is_EFx({"x"}, [{"y"}])
    True
    >>> a.value_1_of_c_MMS(c=4)
    0
    >>> a.value_1_of_c_MMS(c=3)
    1
    >>> a.value_1_of_c_MMS(c=2)
    3
    >>> AdditiveAgent({"x": 1, "y": 2, "z": 4}, duplicity=2)
    Anonymous are 2 agents with a Additive valuation: x=1 y=2 z=4.

    """
    def __init__(self, map_good_to_value:dict, name:str=None, duplicity:int=1):
        """
        Initializes an agent with a given additive valuation function.
        :param map_good_to_value: a dict that maps each single good to its value.
        :param duplicity: the number of agents with the same valuation.
        """
        super().__init__(AdditiveValuation(map_good_to_value), name=name, duplicity=duplicity)

class BinaryAgent(Agent):
    """
    Represents an agent with binary valuations, or several agents with the same binary valuations.

    >>> a = BinaryAgent({"x","y","z"}, name="Alice")
    >>> a
    Alice is an agent with a Binary valuation who wants ['x', 'y', 'z'].
    >>> a.value({"x","w"})
    1
    >>> a.value({"y","z"})
    2
    >>> a.is_EF({"x","w"},[{"y","z"}])
    False
    >>> a.is_EF1({"x","w"},[{"y","z"}])
    True
    >>> a.is_EF1({"v","w"},[{"y","z"}])
    False
    >>> a.is_EF1(set(),[{"y","w"}])
    True
    >>> a.is_EF1(set(),[{"y","z"}])
    False
    >>> a.is_1_of_c_MMS({"x","w"}, c=2)
    True
    >>> a.is_1_of_c_MMS({"w"}, c=2)
    False
    >>> BinaryAgent({"x","y","z"}, duplicity=2)
    Anonymous are 2 agents with a Binary valuation who wants ['x', 'y', 'z'].
    """

    def __init__(self, desired_items:Bundle, name:str=None, duplicity:int=1):
        """
        Initializes an agent with a given set of desired goods.
        :param desired_items: a set of strings - each string is a good.
        :param duplicity: the number of agents with the same set of desired goods.
        """
        super().__init__(BinaryValuation(desired_items), name=name, duplicity=duplicity)


if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
