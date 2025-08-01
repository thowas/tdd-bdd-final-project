######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Web Steps

Steps file for web interactions with Selenium

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import logging
from behave import when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support import expected_conditions as EC

ID_PREFIX = 'product_'


@when('I visit the "Home Page"')
def step_impl(context):
    """ Make a call to the base URL """
    context.driver.get(context.base_url)
    # Uncomment next line to take a screenshot of the web page
    # context.driver.save_screenshot('home_page.png')

@then('I should see "{message}" in the title')
def step_impl(context, message):
    """ Check the document title for a message """
    assert(message in context.driver.title)

@then('I should not see "{text_string}"')
def step_impl(context, text_string):
    element = context.driver.find_element(By.TAG_NAME, 'body')
    assert(text_string not in element.text)

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)

@when('I select "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = Select(context.driver.find_element(By.ID, element_id))
    element.select_by_visible_text(text)

@then('I should see "{text}" in the "{element_name}" dropdown')
def step_impl(context, text, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = Select(context.driver.find_element(By.ID, element_id))
    assert(element.first_selected_option.text == text)

@then('I should see "{product_name}" in the search results')
def step_impl(context, product_name):
    table = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "search_results"))
    )
    assert product_name in table.text, f'Expected "{product_name}" in search results, but not found.\n\nSearch Results:\n{table.text}'

@then('the "{element_name}" field should be empty')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    assert(element.get_attribute('value') == u'')


##################################################################
# These two function simulate copy and paste
##################################################################
@when('I copy the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    context.clipboard = element.get_attribute('value')
    logging.info('Clipboard contains: %s', context.clipboard)

@when('I paste the "{element_name}" field')
def step_impl(context, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(context.clipboard)

##################################################################
# This code works because of the following naming convention:
# The buttons have an id in the html hat is the button text
# in lowercase followed by '-btn' so the Clean button has an id of
# id='clear-btn'. That allows us to lowercase the name and add '-btn'
# to get the element id of any button
##################################################################

## UPDATE CODE HERE ##

@given('I create a product with  eeeee')
def step_impl(context):
    for row in context.table:
        field_name = row[0].lower()
        value = row[1]

        if field_name == 'name':
            element_id = 'product_name'
        elif field_name == 'description':
            element_id = 'product_description'
        elif field_name == 'price':
            element_id = 'product_price'
        elif field_name == 'available':
            element_id = 'product_available'
        elif field_name == 'category':
            element_id = 'product_category'
        else:
            raise ValueError(f"Unbekanntes Feld: {field_name}")

        if element_id in ['product_available', 'product_category']:
            # Select-Felder
            select_element = Select(context.driver.find_element(By.ID, element_id))
            select_element.select_by_visible_text(value)
        else:
            input_element = context.driver.find_element(By.ID, element_id)
            input_element.clear()
            input_element.send_keys(value)
    
    create_btn = context.driver.find_element(By.ID, 'create-btn')
    create_btn.click()


@given('I create a product with')
def step_impl(context):
    for row in context.table:
        for heading in row.headings:
            element_id = f"product_{heading.lower()}"
            try:
                element = context.driver.find_element(By.ID, element_id)
            except Exception as e:
                logging.error(f"Element with ID '{element_id}' not found: {e}")
                raise
          
            tag_name = element.tag_name.lower()

            if tag_name == "select":
                select = Select(element)
                select.select_by_visible_text(row[heading])
                logging.info(f"Selected '{row[heading]}' in '{element_id}'")
            elif tag_name == "input" or tag_name == "textarea":
                element.clear()
                element.send_keys(row[heading])
                logging.info(f"Filled input '{element_id}' with '{row[heading]}'")
            else:
                logging.warning(f"Unbekannter Feldtyp '{tag_name}' für '{element_id}'")

        create_btn = context.driver.find_element(By.ID, 'create-btn')
        create_btn.click()


@given(u'I store the product id')
def step_impl(context):
    id_input = context.driver.find_element(By.ID, "product_id")
    context.product_id = id_input.get_attribute("value")
    logging.info(f"Stored product ID: {context.product_id}")


@then(u'I store the product id')
def step_impl(context):
    id_input = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "product_id"))
    )
    context.product_id = id_input.get_attribute("value")
    assert context.product_id, "Product ID could not be read or is empty"
    logging.info(f"[STORE] Stored product ID: {context.product_id}")

@when('I clear the form')
def step_impl(context):
    try:
        clear_btn = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "clear-btn"))
        )
        clear_btn.click()
        logging.info("Clear button clicked successfully.")
        print("DEBUG: Page Source:")
        print(context.driver.page_source)
    except TimeoutException:
        context.driver.save_screenshot("clear_form_timeout.png")
        raise AssertionError("Clear button ('clear-btn') was not found or not clickable.")
    

@when(u'I enter the stored product id')
def step_impl(context):
    id_input = context.driver.find_element(By.ID, "product_id")
    id_input.clear()
    id_input.send_keys(context.product_id)

@when(u'I click the "Search" button')
def step_impl(context):
    search_btn = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "search-btn"))
    )
    search_btn.click()


@when(u'I change the "price" to "79.95"')
def step_impl(context):
    price_input = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "product_price"))
    )
    price_input.clear()
    price_input.send_keys("79.95")
    print("DEBUG: Preisfeld aktualisiert auf: 79.95")


@when(u'I click the "Update" button')
def step_impl(context):
    update_button = WebDriverWait(context.driver, 10).until(
        EC.element_to_be_clickable((By.ID, "update-btn"))  # ID anpassen!
    )
    update_button.click()
    # Warten auf Flash-Message "Success" o. Ä.
    WebDriverWait(context.driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), "Success")  # ID anpassen!
    )
    print("DEBUG: Update erfolgreich, Success-Meldung gesehen")


@when(u'I click the "Retrieve" button')
def step_impl(context):
    retrieve_btn = WebDriverWait(context.driver, 5).until(
        EC.element_to_be_clickable((By.ID, "retrieve-btn"))
    )
    retrieve_btn.click()

@then(u'the "price" field should contain "79.95"')
def step_impl(context):
    # Nach Update den Preis nochmal auslesen (möglichst nach Neuladen oder Ajax-Update)
    price_field = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "product_price"))
    )
    actual_price = price_field.get_attribute("value")
    print(f"DEBUG: Sichtbarer Preiswert im Feld: '{actual_price}'")
    assert actual_price == "79.95", f"Expected price to be '79.95', but got '{actual_price}'"

WAIT_TIME = 10

@when(u'I click the "Clear" button')
def step_impl(context):
    clear_btn = WebDriverWait(context.driver, WAIT_TIME).until(
        EC.element_to_be_clickable((By.ID, "clear-btn"))
    )
    clear_btn.click()


@when(u'I delete the product')
def step_impl(context):
    context.execute_steps('When I press the "Delete" button')

@when('I click the "Delete" button')
def step_impl(context):
    try:
        delete_btn = WebDriverWait(context.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "delete-btn"))
        )
        delete_btn.click()
        logging.info("Clicked the Delete button.")
    except TimeoutException:
        context.driver.save_screenshot("delete_btn_timeout.png")
        raise AssertionError("Delete button ('delete-btn') was not found or not clickable.")

@given(u'a product with name "{product_name}"')
def step_impl(context, product_name):
    # Simuliere das Auffinden des Produkts im UI
    # z.B. Produkt-ID herausfinden und ins Formular einfüllen
    # Hier einfach Name ins Name-Feld setzen und Retrieve drücken
    context.execute_steps(f'''
        When I set the "Name" to "{product_name}"
        And I press the "Retrieve" button
    ''')

@then(u'the product\'s name should be "{expected_name}"')
def step_impl(context, expected_name):
    element_id = ID_PREFIX + 'name'
    element = context.driver.find_element_by_id(element_id)
    actual_name = element.get_attribute('value')
    assert actual_name == expected_name, f'Expected name to be {expected_name}, but got {actual_name}'

@then(u'the product should no longer exist')
def step_impl(context):
    context.execute_steps('When I press the "Retrieve" button')
    flash = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.visibility_of_element_located((By.ID, "flash_message"))
    )
    actual_text = flash.text.lower()
    assert 'not found' in actual_text, f"Erwartet 'not found' in Flash, aber bekommen: '{actual_text}'"

##################################################################
# This code works because of the following naming convention:
# The id field for text input in the html is the element name
# prefixed by ID_PREFIX so the Name field has an id='pet_name'
# We can then lowercase the name and prefix with pet_ to get the id
##################################################################

#@then('I should see "{text_string}" in the "{element_name}" field')
#def step_impl(context, text_string, element_name):
    #element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    #found = WebDriverWait(context.driver, context.wait_seconds).until(
        #expected_conditions.text_to_be_present_in_element_value(
            #(By.ID, element_id),
            #text_string
        #)
    #)
    #assert(found)

@then('I should see "{text_string}" in the "{element_name}" field')
def step_impl(context, text_string, element_name):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    input_field = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, element_id))
    )
    actual_value = input_field.get_attribute("value")
    print(f"DEBUG: Field '{element_id}' has value: '{actual_value}'")
    assert actual_value == text_string, f"Expected '{text_string}' in field '{element_name}', but got '{actual_value}'"
    

@when('I change "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.presence_of_element_located((By.ID, element_id))
    )
    element.clear()
    element.send_keys(text_string)


@when('I press the "{button_name}" button')
def step_impl(context, button_name):
    button_id = button_name.lower() + '-btn'
    button = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.element_to_be_clickable((By.ID, button_id))
    )
    button.click()

#@then('I should see the message "{message}"')
#def step_impl(context, message):
    #flash = WebDriverWait(context.driver, 10).until(
       #EC.visibility_of_element_located((By.ID, "flash_message"))
    #)
    #assert message in flash.text

@then('I should see the message "{message_text}"')
def step_impl(context, message_text):
    try:
        alert_box = WebDriverWait(context.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "flash_message"))
        )
        assert message_text in alert_box.text, \
            f'Expected message "{message_text}" not found in "{alert_box.text}"'
        logging.info(f'Success message "{message_text}" found.')
    except TimeoutException:
        context.driver.save_screenshot("message_timeout.png")
        print("DEBUG: Page source on timeout:")
        print(context.driver.page_source)
        raise AssertionError(f'Message "{message_text}" not found within timeout.')
