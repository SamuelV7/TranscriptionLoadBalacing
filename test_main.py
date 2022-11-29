import pytest
import main

def test_hugo_header():
    # Can generate date here since it will be the same, given
    # output is asserted on the same date formatted_date here is created
    formatted_date = the_date.strftime("%Y-%m-%d")
    output = main.hugo_header("Sermon 01", "Soli Deo Gloria")

    assert output == "---\n" + "title: " + "Sermon 01" + "\n" + "date: " + formatted_date + "\n" + "draft: " + "Soli Deo Gloria" + " ---\n"
