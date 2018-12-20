from ArduinoHandler import ArduinoHandler

class ArduinoCom:
    """
    Singleton for creation of a serial port connection
    """
    
    @staticmethod
    def instance():
        """
        Creates an instance of this class:
        :return: An ArduinoHandler object.
        """

        if not ArduinoHandler.__instance:
            ArduinoHandler.__instance = Ar