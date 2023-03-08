from selenium.webdriver.common.by import By


class UserPageLocators:
    #############
    #     ID
    #############
    INPUT_LAST_NAME = (By.ID, "lastName")
    INPUT_FIRST_NAME = (By.ID, "firstName")
    INPUT_MIDDLE_NAME = (By.ID, "middleName")
    INPUT_EMAIL = (By.ID, "email")
    INPUT_PWD = (By.ID, "pwd")
    INPUT_RPT_PWD = (By.ID, "rpt-pwd")

    BTN_SAVE = (By.ID, "save")