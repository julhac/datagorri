
class Linklist:
    """
    This is a helper class to manage link list additions from outside the view.
    """
    observers = []

    @staticmethod
    def on_update(func):
        """
        Appends a specified observer function to the observers list
        :param func:
        :return: (boolean)

        """
        Linklist.observers.append(func)
        return True

    @staticmethod
    def add(link):
        """
        Executes the all observer functions in the osservers list with the given link parameter
        :param link:
        :return: (boolean)

        """
        for observer_function in Linklist.observers:
            observer_function(link)

        return True
