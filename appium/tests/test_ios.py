import os
import json

from time import sleep

def test_send_message(driver):
    driver.find_element_by_accessibility_id('send message').click()

    sleep(3)

    value = driver.find_element_by_accessibility_id('textarea').get_attribute("value")

    assert value != None
    event = json.loads(value)

    assert len(event['breadcrumbs']) > 0
    assert len(event['contexts']) > 0
    assert event['message'] == 'TEST message'
    assert event['extra']['react']
    assert event['tags']['react'] == '1'
    assert event['sdk'] == False
    assert event['sdk']['integrations'][0] == 'react-native'
    assert len(event['user']) > 0

def test_throw_error(driver):
    driver.find_element_by_accessibility_id('throw error').click()
    driver.relaunch_app()
    value = driver.find_element_by_accessibility_id('textarea').get_attribute("value")
    # the crash should have been already sent
    assert value is None

def test_native_crash(driver):
    sleep(2)
    driver.find_element_by_accessibility_id('native crash').click()
    driver.relaunch_app()
    sleep(3)
    value = driver.find_element_by_accessibility_id('textarea').get_attribute("value")
    # the crash should have been already sent
    assert value != None
    event = json.loads(value)

    assert len(event['breadcrumbs']) > 0
    assert len(event['contexts']) > 0
    assert len(event['threads']['values']) > 0
    for thread in event['threads']['values']:
        if thread['crashed']:
            assert len(thread['stacktrace']['frames']) > 0
            cocoa_frames = 0
            js_frames = 0
            for frame in thread['stacktrace']['frames']:
                if frame.get('package', None):
                    cocoa_frames += 1
                if frame.get('platform', None) == 'javascript':
                    js_frames += 1
            assert cocoa_frames > 0
            assert js_frames > 0 # does not work in release build
    assert len(event['exception']['values']) > 0
    assert len(event['debug_meta']['images']) > 0
    assert event['platform'] == 'cocoa'
    assert event['level'] == 'fatal'
    assert event['extra']['react']
    assert event['tags']['react'] == '1'
    assert len(event['user']) > 0
