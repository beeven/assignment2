"""Assignment 2: Organization Hierarchy
You must NOT use list.sort() or sorted() in your code.

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains all of the classes necessary to model the entities
in an organization's hierarchy.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Sophia Huynh

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Sophia Huynh
"""
from __future__ import annotations
from typing import List, Optional, Union, TextIO


# TODO: === TASK 1 ===
# Complete the merge() function and the Employee and Organization classes
# according to their docstrings.
# Go through client_code.py to find additional methods that you must
# implement.
# You may add private attributes and helper methods, but do not change the
# public interface.
# Properly document all methods you write, and document your attributes
# in the class docstring.

# You must NOT use list.sort() or sorted() in your code.
# Write and make use of the merge() function instead.


def merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Pre-condition: <lst1> and <lst2> are both sorted.

    >>> merge([1, 2, 5], [3, 4, 6])
    [1, 2, 3, 4, 5, 6]
    """
    # TODO Task 1: Complete the merge() function.

    i1 = 0
    i2 = 0
    ret = []
    while i1 < len(lst1):
        if lst2[i2] < lst1[i1]:
            ret.append(lst2[i2])
            i2 += 1
            if i2 == len(lst2):
                break
        else:
            ret.append(lst1[i1])
            i1 += 1
    if i2 < len(lst2):
        ret.extend(lst2[i2:])
    else:
        ret.extend(lst1[i1:])

    return ret


class Employee:
    """An Employee: an employee in an organization.

    === Public Attributes ===
    eid:
        The ID number of the employee. Within an organization, each employee ID
        number is unique.
    name:
        The name of the Employee.
    position:
        The name of the Employee's position within the organization.
    salary:
        The salary of the Employee.
    rating:
        The rating of the Employee.

    === Private Attributes ===
    _superior:
        The superior of the Employee in the organization.
    _subordinates:
        A list of the Employee's direct subordinates (Employees that work under
        this Employee).

    === Representation Invariants ===
    - eid > 0
    - Within an organization, each eid only appears once. Two Employees cannot
      share the same eid.
    - salary > 0
    - 0 <= rating <= 100
    """
    eid: int
    name: str
    position: str
    salary: float
    rating: int
    _superior: Optional[Employee]
    _subordinates: List[Employee]

    # === TASK 1 ===
    def __init__(self, eid: int, name: str, position: str,
                 salary: float, rating: int) -> None:
        """Initialize this Employee with the ID <eid>, name <name>,
        position <position>, salary <salary> and rating <rating>.

        >>> e = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e.eid
        1
        >>> e.rating
        50
        """
        # TODO Task 1: Complete the __init__ method.

        self.eid = eid
        self.name = name
        self.position = position
        self.salary = salary
        self.rating = rating
        self._subordinates = []
        self._superior = None

    def __lt__(self, other: Employee) -> bool:
        """Return True iff <other> is an Employee and this Employee's eid is
        less than <other>'s eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1 < e2
        True
        """
        # TODO Task 1: Complete the __lt__ method.

        return self.eid < other.eid

    def get_direct_subordinates(self) -> List[Employee]:
        """Return a list of the direct subordinates of this Employee in order of
        ascending IDs.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e2.get_direct_subordinates()[0].name
        'Emma Ployee'
        """
        # TODO Task 1: Complete the get_direct_subordinates method.

        return self._subordinates

    def get_all_subordinates(self) -> List[Employee]:
        """Return a list of all of the subordinates of this Employee in order of
        ascending IDs.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_all_subordinates()[0].name
        'Emma Ployee'
        >>> e3.get_all_subordinates()[1].name
        'Sue Perior'
        """

        # TODO Task 1: Complete the get_all_subordinates method.

        def get_subordinates(e: Employee):
            if len(e._subordinates) == 0:
                return [e]
            else:
                lst = []
                i = 0
                while i < len(e._subordinates):
                    lst = merge(lst, get_subordinates(e._subordinates[i]))
                    i += 1

                return merge(lst, [e])

        ret = get_subordinates(self)
        i = 0
        while i < len(ret):
            if ret[i].eid == self.eid: break
            i += 1
        ret.pop(i)
        return ret

    def get_organization_head(self) -> Employee:
        """Return the head of the organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_organization_head().name
        'Bigg Boss'
        """
        # TODO Task 1: Complete the get_organization_head method.
        e = self
        while e._superior is not None:
            e = e._superior

        return e

    def get_superior(self) -> Optional[Employee]:
        """Returns the superior of this Employee or None if no superior exists.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_superior() is None
        True
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e1.get_superior().name
        'Sue Perior'
        """
        # TODO Task 1: Complete the get_superior method.

        return self._superior

    # Task 1: Helper methods
    #         While not called by the client_code, these methods may be helpful
    #         to you and will be tested. You can (and should) call them in
    #         the other methods that you implement.
    def become_subordinate(self, superior: Union[Employee, None]) -> None:
        """Set this Employee's superior to <superior> and becomes a direct
        subordinate of <superior>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e1.get_superior().eid
        2
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e1.become_subordinate(None)
        >>> e1.get_superior() is None
        True
        >>> e2.get_direct_subordinates()
        []
        """
        # TODO Task 1: Complete the become_subordinate method.

        if self._superior is not None:
            self._superior.remove_subordinate_id(self.eid)

        self._superior = superior
        if superior is not None:
            superior.add_subordinate(self)

    def remove_subordinate_id(self, eid: int) -> None:
        """Remove the subordinate with the eid <eid> from this Employee's list
        of direct subordinates.

        Does NOT change the employee with eid <eid>'s superior.

        Pre-condition: This Employee has a subordinate with eid <eid>.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e1.become_subordinate(e2)
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e2.remove_subordinate_id(1)
        >>> e2.get_direct_subordinates()
        []
        >>> e1.get_superior() is e2
        True
        """
        # TODO Task 1: Complete the remove_subordinate_id method.

        if len(self._subordinates) == 0:
            return

        i = 0
        while i < len(self._subordinates):
            if self._subordinates[i].eid == eid: break
            i += 1

        if i < len(self._subordinates):
            self._subordinates.pop(i)

    def add_subordinate(self, subordinate: Employee) -> None:
        """Add <subordinate> to this Employee's list of direct subordinates.

        Does NOT change subordinate's superior.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e2.add_subordinate(e1)
        >>> e2.get_direct_subordinates()[0].eid
        1
        >>> e1.get_superior() is None
        True
        """
        # TODO Task 1: Complete the add_subordinate method.

        self._subordinates = merge(self._subordinates, [subordinate])

    def get_employee(self, eid: int) -> Optional[Employee]:
        """Returns the employee with ID <eid> or None if no such employee exists
        as a subordinate of this employee.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_employee(1) is e1
        True
        >>> e1.get_employee(1) is e1
        True
        >>> e2.get_employee(3) is None
        True
        """
        # TODO Task 1: Complete the get_employee method.

        if self.eid == eid:
            return self

        for s in self._subordinates:
            if s.eid == eid:
                return s
            else:
                e = s.get_employee(eid)
                if e is not None:
                    return e

    def get_employees_paid_more_than(self, amount: float) -> List[Employee]:
        """Get all subordinates of this employee that have a salary higher than
        <amount> (including this employee, if this employee's salary is higher
        than <amount>).

        Employees must be returned in increasing order of eid.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Employee(2, "Sue Perior", "Manager", 20000, 30)
        >>> e3 = Employee(3, "Bigg Boss", "CEO", 50000, 60)
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> more_than_10000 = e3.get_employees_paid_more_than(10000)
        >>> len(more_than_10000) == 2
        True
        >>> more_than_10000[0].name
        'Sue Perior'
        >>> more_than_10000[1].name
        'Bigg Boss'
        """
        # TODO Task 1: Complete the get_employees_paid_more_than method.

        employees = merge(self.get_all_subordinates(), [self])
        return list(filter(lambda a: a.salary > amount, employees))

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 1. Write their headers and bodies below.

    def get_higher_paid_employees(self) -> List[Employee]:
        head = self.get_organization_head()
        return head.get_employees_paid_more_than(self.salary)

    def get_closest_common_superior(self, eid: int) -> Employee:
        pass

    # === TASK 2 ===
    def get_department_name(self) -> str:
        """Returns the name of the department this Employee is in. If the
        Employee is not part of a department, return an empty string.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_name()
        ''
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e1.become_subordinate(e2)
        >>> e1.get_department_name()
        'Department'
        """
        # TODO Task 2: Complete the get_department_name method.

        if isinstance(self, Leader):
            return self.get_department_name()
        else:
            s = self.get_superior()
            while s is not None:
                if isinstance(s, Leader):
                    return s.get_department_name()
                s = s.get_superior()

    def get_position_in_hierarchy(self) -> str:
        """Returns a string that describes the Employee's position in the
        organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_position_in_hierarchy()
        'Worker'
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_position_in_hierarchy()
        'Worker, Department, Company'
        >>> e2.get_position_in_hierarchy()
        'Manager, Department, Company'
        >>> e3.get_position_in_hierarchy()
        'CEO, Company'
        """
        # TODO Task 2: Complete the get_position_in_hierarchy method.

        hierarchy = [self.position]
        if isinstance(self, Leader):
            hierarchy.append(self.get_department_name())
        s = self.get_superior()
        while s is not None:
            if isinstance(s, Leader):
                hierarchy.append(s.get_department_name())
            s = s.get_superior()

        return ', '.join(hierarchy)

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 2.

    # === TASK 3 ===
    # Task 3: Helper methods
    #         While not called by the client_code, this method may be helpful
    #         to you and will be tested. You can (and should) call this in
    #         the other methods that you implement.
    def get_department_leader(self) -> Optional[Leader]:
        """Return the leader of this Employee's department. If this Employee is
        not in a department, return None.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_department_leader() is None
        True
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e1.get_department_leader().name
        'Sue Perior'
        >>> e2.get_department_leader().name
        'Sue Perior'
        """
        # TODO Task 3: Complete the get_department_leader method.

        if isinstance(self, Leader):
            return self

        e = self._superior
        while e is not None:
            if isinstance(e, Leader):
                return e
            e = e.get_superior()

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 3.

    def become_leader(self, department: str) -> Leader:
        leader = Leader(self.eid, self.name, self.position, self.salary, self.rating, department)
        leader._subordinates = self._subordinates
        for s in self._subordinates:
            s.become_subordinate(leader)
        if self._superior is not None:
            self._superior.remove_subordinate_id(self.eid)
        leader.become_subordinate(self._superior)
        return leader

    def change_department_leader(self) -> Employee:
        if isinstance(self, Leader):
            return self.get_organization_head()

        original_leader = self.get_department_leader()
        department_name = original_leader.get_department_name()
        self.become_subordinate(original_leader.get_superior())
        original_leader.become_subordinate(self)
        original_leader.become_employee()
        self.become_leader(department_name)
        return self.get_organization_head()

    # Part 4: Helper methods
    #         While not called by the client_code, these methods may be helpful
    #         to you and will be tested. You can (and should) call them in
    #         the other methods that you implement.
    def get_highest_rated_subordinate(self) -> Employee:
        """Return the subordinate of this employee with the highest rating.

        Pre-condition: This Employee has at least one subordinate.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e1.get_position_in_hierarchy()
        'Worker'
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> e3.get_highest_rated_subordinate().name
        'Sue Perior'
        >>> e1.become_subordinate(e3)
        >>> e3.get_highest_rated_subordinate().name
        'Emma Ployee'
        """
        # TODO Task 4: Complete the get_highest_rated_subordinate method.

        return max(self._subordinates, key=lambda a: a.rating)

    def swap_up(self) -> Employee:
        """Swap this Employee with their superior. Return the version of this
        Employee that is contained in the Organization (i.e. if this Employee
        becomes a Leader, the new Leader version is returned).

        Pre-condition: self is not the head of the Organization.

        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
        >>> e1.become_subordinate(e2)
        >>> e2.become_subordinate(e3)
        >>> new_e1 = e1.swap_up()
        >>> isinstance(new_e1, Leader)
        True
        >>> new_e2 = new_e1.get_direct_subordinates()[0]
        >>> isinstance(new_e2, Employee)
        True
        >>> new_e1.position
        'Manager'
        >>> new_e1.eid
        1
        >>> e3.get_direct_subordinates()[0] is new_e1
        True
        """
        # TODO Task 4: Complete the swap_up method.

        if isinstance(self._superior, Leader):
            employee = Leader(self.eid, self.name, self._superior.position, self.salary, self.rating,
                              self._superior.get_department_name())
        else:
            employee = Employee(self.eid, self.name, self._superior.position, self.salary, self.rating)

        if isinstance(self, Leader):
            original_superior = Leader(self._superior.eid, self._superior.name, self.position, self._superior.salary,
                                       self._superior.rating, self.get_department_name())
        else:
            original_superior = Employee(self._superior.eid, self._superior.name, self.position, self._superior.salary,
                                         self._superior.rating)

        for s in self._subordinates:
            s.become_subordinate(original_superior)
        self._superior.remove_subordinate_id(self.eid)
        for s in self._superior._subordinates:
            s.become_subordinate(employee)
        original_superior.become_subordinate(employee)
        return employee

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 4.

    def obtain_subordinates(self, ids: List[int]) -> Employee:
        head = self.get_organization_head()
        for eid in ids:
            if eid != head.eid:
                e = head.get_employee(eid)
                for s in e._subordinates:
                    s.become_subordinate(e._superior)
                e.become_subordinate(self)
            else:
                e = head.get_highest_rated_subordinate()
                head.remove_subordinate_id(e.eid)
                e._superior = None
                for s in head._subordinates:
                    s.become_subordinate(e)
                head.become_subordinate(self)
                head = self.get_organization_head()
        return self.get_organization_head()



class Organization:
    """An Organization: an organization containing employees.

    === Private Attributes ===
    _head:
        The head of the organization.

    === Representation Invariants ===
    - _head is either an Employee (or subclass of Employee) or None (if there
      are no Employees).
    - No two Employees in an Organization have the same eid.
    """
    _head: Optional[Employee]

    # === TASK 1 ===
    def __init__(self, head: Optional[Employee] = None) -> None:
        """Initialize this Organization with the head <head>.

        >>> o = Organization()
        >>> o.get_head() is None
        True
        """
        # TODO Task 1: Complete the __init__ method.

        self._head = head

    def get_employee(self, eid: int) -> Optional[Employee]:
        """
        Return the employee with id <eid>. If no such employee exists, return
        None.

        >>> o = Organization()
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> o.add_employee(e1)
        >>> o.get_employee(1) is e1
        True
        >>> o.get_employee(2) is None
        True
        """
        # TODO Task 1: Complete the get_employee method.

        if self._head is None:
            return None

        else:
            return self._head.get_employee(eid)

    def add_employee(self, employee: Employee, superior_id: int = None) -> None:
        """Add <employee> to this organization as the subordinate of the
        employee with id <superior_id>.

        >>> o = Organization()
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e2)
        >>> o.get_head() is e2
        True
        >>> o.add_employee(e1, 2)
        >>> o.get_employee(1) is e1
        True
        >>> e1.get_superior() is e2
        True
        """
        # TODO Task 1: Complete the add_employee method.
        if superior_id is None:
            self._head = employee
        else:
            e = self.get_employee(superior_id)
            employee.become_subordinate(e)

    def get_average_salary(self, position: Optional[str] = None) -> float:
        """Returns the average salary of all employees in the organization with
        the position <position>.

        If <position> is None, this returns the average salary of all employees.

        If there are no such employees, return 0.0

        >>> o = Organization()
        >>> o.get_average_salary()
        0
        >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> o.add_employee(e2)
        >>> o.add_employee(e1, 2)
        >>> o.get_average_salary()
        15000.0
        """
        # TODO Task 1: Complete the get_average_salary method.

        if self._head is None:
            return 0

        employees = merge(self._head.get_all_subordinates(), [self._head])

        if position is not None:
            employees = list(filter(lambda a: a.position == position, employees))

        return sum(map(lambda e: e.salary, employees)) / len(employees)

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 1.

    def get_head(self):
        return self._head

    def get_employees_with_position(self, position: str) -> List[Employee]:
        employees = []
        if self._head is not None:
            employees = merge([self._head], self._head.get_all_subordinates())

        return list(filter(lambda a: a.position == position, employees))

    def get_next_free_id(self):
        if self._head is None:
            return 1
        else:
            subordinates = self._head.get_all_subordinates()
            if len(subordinates) > 0:
                return subordinates[-1].eid + 1
            else:
                return 2

    # === TASK 3 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 3.

    def set_head(self, e: Employee = None):
        self._head = e

    # === TASK 4 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 4.

    def fire_employee(self, eid: int) -> None:
        employee = self.get_employee(eid)
        superior = employee.get_superior()

        if superior is not None:
            for s in employee.get_direct_subordinates():
                s.become_subordinate(superior)
        else: # fire head
            if len(employee.get_direct_subordinates()) > 0:
                e = employee.get_highest_rated_subordinate()
                head = e.swap_up()
                employee = head.get_employee(eid)
                for s in employee.get_direct_subordinates():
                    s.become_subordinate(head)
                self.set_head(head)
            else:
                self.set_head(None)

    def fire_lowest_rated_employee(self) -> None:
        head = self.get_head()
        if len(head.get_direct_subordinates()) == 0:
            self.set_head(None)
            return

        employees_ordered_by_eid = head.get_all_subordinates()

        index = 0
        lowest_rating = employees_ordered_by_eid[0].rating
        lowest_rating_index = 0

        while index < len(employees_ordered_by_eid):
            if employees_ordered_by_eid[index].rating < lowest_rating:
                lowest_rating = employees_ordered_by_eid[index].rating
                lowest_rating_index = index
            index += 1

        employee = employees_ordered_by_eid[lowest_rating_index]
        if employee.rating > head.rating:
            self.fire_employee(head.eid)
        elif employee.rating < head.rating:
            self.fire_employee(employee.eid)
        elif head.eid < employee.eid:
            self.fire_employee(head.eid)
        else:
            self.fire_employee(employee.eid)

    def fire_under_rating(self, rating):
        pass

    def promote_employee(self, eid):
        pass

# === TASK 2: Leader ===
# TODO: Complete the Leader class and its methods according to their docstrings.
#       You will also need to revisit Organization and Employee to implement
#       additional methods.
#       Go through client_code.py to find additional methods that you must
#       implement.
#
# You may add private attributes and helper methods, but do not change the
# public interface.
# Properly document all methods you write, and document your attributes
# in the class docstring.
#
# After the completion of Task 2, you should be able to run organization_ui.py,
# though not all of the buttons will work.


class Leader(Employee):
    """A subclass of Employee. The leader of a department in an organization.

    === Private Attributes ===
    _department_name:
        The name of the department this Leader is the head of.

    === Inherited Attributes ===
    eid:
        The ID number of the employee. Within an organization, each employee ID
        number is unique.
    name:
        The name of the Employee.
    position:
        The name of the Employee's position within the organization.
    salary:
        The salary of the Employee.
    rating:
        The rating of the Employee.
    _superior:
        The superior of the Employee in the organization.
    _subordinates:
        A list of the Employee's direct subordinates (Employees that work under
        this Employee).

    === Representation Invariants ===
    - All Employee RIs are inherited.
    - Department names are unique within an organization.
    """
    _department_name: str

    # === TASK 2 ===
    def __init__(self, eid: int, name: str, position: str, salary: float,
                 rating: int, department: str) -> None:
        """Initialize this Leader with the ID <eid>, name <name>, position
        <position>, salary <salary>, rating <rating>, and department name
        <department>.

        >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
        >>> e2.name
        'Sue Perior'
        >>> e2.get_department_name()
        'Department'
        """
        # TODO Task 2: Complete the __init__ method.

        self._department_name = department
        super().__init__(eid, name, position, salary, rating)

    # TODO: Go through client_code.py for additional methods you need to
    #       implement in Task 2.
    #       There may also be Employee methods that you'll need to override.

    def get_department_name(self):
        return self._department_name

    def get_department_employees(self):
        return self.get_all_subordinates()

    # === TASK 3 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 3. If there are no methods there, consider if you need to
    #       override any of the Task 3 Employee methods.

    def become_employee(self) -> Employee:
        employee = Employee(self.eid, self.name, self.position, self.salary, self.rating)
        for s in self.get_direct_subordinates():
            s.become_subordinate(employee)
        self._superior.remove_subordinate_id(self.eid)
        employee.become_subordinate(self._superior)
        return employee

    # === TASK 4 ===
    # TODO: Go through client_code.py for the methods you need to implement in
    #       Task 4. If there are no methods there, consider if you need to
    #       override any of the Task 4 Employee methods.


# === TASK 5 ===
# TODO: Complete the create_department_salary_tree() function according to
#       its docstrings and the specifications in the assignment handout.
#
# You may add private helper functions, but do not change the public interface.
# Any helper functions you create should have _ at the start of its name to
# denote it being private (e.g. "def _helper_function()")
# Make sure you properly document (e.g. docstrings, type annotations) your code.

class DepartmentSalaryTree:
    """A DepartmentSalaryTree: A tree representing the salaries of departments.
    The salaries considered only consist of employees directly in a department
    and not in any of their subdepartments.

    Do not change this class.

    === Public Attributes ===
    department_name:
        The name of the department that this DepartmentSalaryTree represents.
    salary:
        The average salary of the department that this DepartmentSalaryTree
        represents.
    subdepartments:
        The subdepartments of the department that this DepartmentSalaryTree
        represents.
    """
    department_name: str
    salary: float
    subdepartments: [DepartmentSalaryTree]

    def __init__(self, department_name: str, salary: float,
                 subdepartments: List[DepartmentSalaryTree]) -> None:
        """Initialize this DepartmentSalaryTree with the department name
        <department_name>, salary <salary>, and the subdepartments
        <subdepartments>.

        >>> d = DepartmentSalaryTree('Department', 30000, [])
        >>> d.department_name
        'Department'
        """
        self.department_name = department_name
        self.salary = salary
        self.subdepartments = subdepartments[:]


def create_department_salary_tree(organization: Organization) -> \
        Optional[DepartmentSalaryTree]:
    """Return the DepartmentSalaryTree corresponding to <organization>.

    If <organization> has no departments, return None.

    Pre-condition: If there is at least one department in <organization>,
    then the head of <organization> is also a Leader.

    >>> o = Organization()
    >>> e1 = Employee(1, "Emma Ployee", "Worker", 10000, 50)
    >>> e2 = Leader(2, "Sue Perior", "Manager", 20000, 30, "Department")
    >>> e3 = Leader(3, "Bigg Boss", "CEO", 50000, 60, "Company")
    >>> o.add_employee(e2)
    >>> o.add_employee(e1, 2)
    >>> o.add_employee(e3)
    >>> dst = create_department_salary_tree(o)
    >>> dst.department_name
    'Company'
    >>> dst.salary
    50000.0
    >>> dst.subdepartments[0].department_name
    'Department'
    >>> dst.subdepartments[0].salary
    15000.0
    """
    # TODO Task 5: Complete the create_department_salary_tree function.


# === TASK 6 ===
# TODO: Complete the create_organization_from_file() function according to
#       its docstrings and the specifications in the assignment handout.
#
# You may add private helper functions, but do not change the public interface.
# Any helper functions you create should have _ at the start of its name to
# denote it being private (e.g. "def _helper_function()")
# Make sure you properly document (e.g. docstrings, type annotations) your code.

def create_organization_from_file(file: TextIO) -> Organization:
    """Return the Organization represented by the information in <file>.

    >>> o = create_organization_from_file(open('employees.txt'))
    >>> o.get_head().name
    'Alice'
    """
    # TODO Task 6: Complete the create_organization_from_file function.


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'doctest', 'typing',
                                   '__future__'],
        'max-args': 7})
