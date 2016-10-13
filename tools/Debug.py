class Debug:
    DEBUGGING = False

    @staticmethod
    def printMessage(text):
        if Debug.DEBUGGING:
            print(text)
