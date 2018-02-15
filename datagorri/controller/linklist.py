# Helper class to manage link list additions from outside the view


class Linklist:
    """
    This is a helper class to manage link list additions from outside the view.
    """
    observers = []

    @staticmethod
    def on_update(function):
        Linklist.observers.append(function)
        return True

    @staticmethod
    def add(link):
        for observer_function in Linklist.observers:
            observer_function(link)

        return True
