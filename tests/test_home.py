from datetime import datetime
from seleniumbase import BaseCase
import pytest


blog_name = 'seleniumbase-test'
blog_password = 'seleniumbase-test'
nav_element = '#target'
entry_element = '#writer'
publish_element = '#publish'


class HomeTest(BaseCase):
    def login(self):
        # open website
        self.open("https://write.as/")

        # click on login
        self.click('a[href="/login"]')
        self.wait(3)

        # generate data and fill
        self.update_text('input[name=alias]', blog_name)
        self.update_text('input[name=pass]', blog_password)
        self.click('#btn-login')
        self.wait(3)

    def hover_and_execute_action(self, action: str):
        print('action', action)
        self.click(f'a[href="/{blog_name}/"]')
        self.hover_on_element('article[id^=post]')
        self.click(f'a[href$="{action}"]')
        self.wait(3)

    @pytest.mark.order(1)
    def test_write_post(self):
        # login
        self.login()

        # create a text entry
        self.update_text(
            entry_element,
            f'This is an automated bot writing a blog entry on Write.as at { str(datetime.now()) }'
        )
        self.wait(3)

        # publish
        self.click(publish_element)
        self.wait(3)
        print('Writing to Blog - Done')

    @pytest.mark.order(2)
    def test_edit_last_post(self):
        # login
        self.login()

        # go to dashboard
        self.click('a[href="/me/c/"]')
        self.wait(3)

        # go to blog
        self.hover_and_execute_action(action='edit')
        self.update_text(
            selector=entry_element,
            text=f'An edited entry using SeleniumBase at { str(datetime.now()) }'
        )
        self.wait(3)

        # publish update
        self.click(publish_element)
        self.wait(3)
        print('Editing Entry - Done')

    @pytest.mark.order(3)
    def test_delete_last_post(self):
        # login
        self.login()

        # go to dashboard
        self.click('a[href="/me/c/"]')
        self.wait(3)

        # go to blog
        self.hover_and_execute_action(action='delete')
        self.wait(10)

        # confirm deletion
        self.wait_for_and_switch_to_alert()
        self.accept_alert()
        self.wait(3)
        print('Deleting Entry - Done')
