import sys
sys.path.append('../')
import main

def test_valid_email():
    email = 'jmoswal@hotmail.com'
    assert main.check_email_validation(email), f"Failed: {email} should be valid"

def test_invalid_email():
    email = 'jmoswal@@@hotmail'
    assert not main.check_email_validation(email), f"Failed: {email} should be invalid"

def test_empty_email():
    email = ''
    assert not main.check_email_validation(email), f"Failed: {email} should be invalid"
