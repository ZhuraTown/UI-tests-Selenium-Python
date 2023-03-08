from selenium.webdriver.common.by import By


class AuthorizationPageLocators:

    INPUT_EMAIL = (By.ID, "email")
    INPUT_PWD = (By.ID, "pwd")

    BTN_LOGIN = (By.ID, "login")
    BTN_FORGOT_PWD = (By.ID, "forgot-pwd")

    ERR_MSG = (By.XPATH, "//div[@class='err-msg'][contains(text(), '{}')]")