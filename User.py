class User:
    countID = 0

    def __init__(self, firstname, lastname, membership, gender, remarks):
        User.countID +=1
        self.__userID = User.countID
        self.__firstname = firstname
        self.__lastname = lastname
        self.__membership = membership
        self.__gender = gender
        self.__remarks = remarks

    def get_userID(self):
        return self.__userID
    def get_firstname(self):
        return self.__firstname
    def get_lastname(self):
        return self.__lastname
    def get_membership(self):
        return self.__membership
    def get_gender(self):
        return self.__gender
    def get_remarks(self):
        return self.__remarks

    def set_userID(self, userID):
        self.__userID = userID
    def set_firstname(self, firstname):
        self.__firstname = firstname
    def set_lastname(self, lastname):
        self.__lastname = lastname
    def set_membership(self, membership):
        self.__membership = membership
    def set_gender(self, gender):
        self.__gender = gender
    def set_remarks(self, remarks):
        self.__remarks = remarks