class Debug:
    DEBUGGING = True

    @staticmethod
    def printMessage(text):
        if Debug.DEBUGGING:
            print(text)
