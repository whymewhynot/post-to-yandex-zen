from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import InvalidArgumentException
import pickle
import time


class YandexZenPoster:

    def __init__(self, login, password, headless=True):

        self.login = login
        self.password = password

        self.paragraph = 0

        chrome_options = Options()

        if headless:
            chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

        # Check if there are any saved cookies:
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            self.driver.get('https://ya.ru/')
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.get('https://zen.yandex.ru/')
        # No cookies:
        except:
            self.driver.get('https://zen.yandex.ru/')
            # Log in to Zen
            enter_button = self.driver.find_element_by_link_text('Войти')
            enter_button.click()

            # Login field
            login_field = self.driver.find_element_by_id('passp-field-login')
            login_field.send_keys(self.login)
            login_enter_button = self.driver.find_element_by_class_name('passp-sign-in-button')
            login_enter_button.click()

            # Password field
            password_field = self.driver.find_element_by_id('passp-field-passwd')
            password_field.send_keys(self.password)
            password_enter_button = self.driver.find_element_by_class_name('passp-sign-in-button')
            password_enter_button.click()

            # "Enter your phone number". Not now
            try:
                self.driver.find_element_by_id('passp-field-phoneNumber')
                not_now = self.driver.find_element_by_class_name('Button2_view_pseudo')
                not_now.click()
            except:
                pass

            # "Enter additional email'. Not now
            try:
                self.driver.find_element_by_id('passp-field-additional_email')
                not_now = self.driver.find_element_by_class_name('Button2_view_pseudo')
                not_now.click()
            except:
                pass

        # Post editor
        my_profile = self.driver.find_element_by_css_selector('button.zen-ui-avatar')
        my_profile.click()
        editor = self.driver.find_element_by_link_text('Редактор')
        editor.click()
        self.save_cookie()
        time.sleep(5)

    def save_cookie(self):
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def create_new_post(self):
        new_post = self.driver.find_element_by_class_name('zen-header__add-button')
        new_post.click()
        article = self.driver.find_element_by_class_name('new-publication-dropdown__button-text')
        article.click()

        # Close the hint popup
        try:
            help_popup = self.driver.find_element_by_class_name('close-cross')
            help_popup.click()
        except:
            pass

    def title(self, text):
        # Call this method only after create_new_post()

        title = self.driver.find_element_by_tag_name('h1')
        title.send_keys(text)

    def text_block(self, text):
        # Call this method only after create_new_post()

        text_block = self.driver.find_elements_by_class_name('zen-editor-block-paragraph')[self.paragraph]
        text_block.send_keys(text)
        text_block.send_keys(Keys.ENTER)
        self.paragraph += 1
        time.sleep(3)

    def hashtags(self, tags):
        # Call this method only after create_new_post()
        # Tags should be passed as list or str (if there is a single hashtag)

        text_block = self.driver.find_elements_by_class_name('zen-editor-block-paragraph')[self.paragraph]
        if isinstance(tags, (list, set, tuple)):
            for tag in tags:
                text_block.send_keys('#' + tag)
                text_block.send_keys(Keys.ENTER)
                time.sleep(3)
        elif isinstance(tags, dict):
            raise Exception('Tags should be passed as list, set, tuple or string, not dict')
        else:
            tags = str(tags)
            text_block.send_keys('#' + tags)
            text_block.send_keys(Keys.ENTER)
            time.sleep(3)
        text_block.send_keys(Keys.ENTER)
        time.sleep(5)

    def photo(self, path):
        # Call this method only after create_new_post()
        # The absolute path is required!

        add_image_icon = self.driver.find_element_by_class_name('side-button_logo_image')
        add_image_icon.click()
        upload_file_button = self.driver.find_element_by_class_name('image-popup__file-input')
        try:
            upload_file_button.send_keys(path)
        except InvalidArgumentException:
            raise Exception(f'Error while uploading photo "{path}"\nThe absolute path is required!')
        time.sleep(5)

    def post(self, description=None):
        # Call this method only after create_new_post() and other methods

        post_button = self.driver.find_element_by_class_name('editor-header__edit-btn')
        post_button.click()

        if description:
            description_field = self.driver.find_elements_by_tag_name('textarea')[1]
            description_field.clear()
            time.sleep(2)
            description_field.send_keys(description)

        post_button2 = self.driver.find_element_by_class_name('_view-type_yellow')
        post_button2.click()
        time.sleep(3)

        published = self.driver.find_element_by_xpath('//input[@value="published"]')
        published.click()
        articles_links = self.driver.find_elements_by_xpath('//a[@class="card-cover-publication-background"]')[0]
        latest_article = articles_links.get_attribute('href').split('?')[0]
        print(f'Your post is published: {latest_article}')
        return latest_article











