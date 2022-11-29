import main
from datetime import  datetime

def test_hugo_header():
    # Can generate date here since it will be the same, given
    # output is asserted on the same date formatted_date here is created
    the_date = datetime.now()
    formatted_date = the_date.strftime("%Y-%m-%d")
    output = main.hugo_header("Sermon 01", "false")

    assert output == "---\n" + "title: " + "Sermon 01" + "\n" + "date: " + formatted_date + "\n" + "draft: " + "false" + "\n" + " --- " + "\n"

def test_hugo_with_content():
    hugo_content = main.hugo_with_content("Sermon 01", "false", "Soli Deo Gloria")
    assert main.hugo_with_content("Sermon 01", "false", "Soli Deo Gloria") \
           == main.hugo_header("Sermon 01", "false") + "Soli Deo Gloria"