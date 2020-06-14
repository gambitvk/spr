
class GestureManager():

    def __init__(self):
        self._gestures = []
        self._lose_to = {}

    def register_gesture(self, gesture, lose_to):
        self._gestures.append(gesture)
        self._lose_to[gesture] = lose_to

    def available_gestures(self):
        return self._gestures

    def rules_in_str(self):
        result = []
        for gesture, lose_to in self._lose_to.items():
            result.append(f"{gesture} defects {lose_to}")
        return "\n".join(result)

    def lose_to(self, gesture):
        return self._lose_to[gesture]
