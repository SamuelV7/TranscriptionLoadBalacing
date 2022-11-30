from turtle import down
import main
import os
from datetime import  datetime
import pytest

@pytest.fixture(scope="module")
def file_fixture():
    # save file with following test
    print("Creating File for test")
    the_test_file = "test.txt"
    main.save_file(the_test_file, "Soli Deo Gloria")
    yield the_test_file
    # delete files after all test are run
    print("Deleting file")
    os.remove(the_test_file)

@pytest.fixture(scope="module")
def download_file():
    url = "https://www.youtube.com/watch?v=2Nc7_9I76HI"
    output = main.download_yt(url, None)
    assert output == "GraceLife London.mp3"
    yield output
    print("Deleting File")
    os.remove("GraceLife London.mp3")

def test_hugo_header():
    # Can generate date here since it will be the same, given
    # output is asserted on the same date formatted_date here is created
    the_date = datetime.now()
    formatted_date = the_date.strftime("%y-%m-%d")
    output = main.hugo_header("Sermon 01", "false")

    assert output == "---\n" + "title: " + "Sermon 01" + "\n" + "date: " + formatted_date + "\n" + "draft: " + "false" + "\n" + "---" + "\n"

def test_hugo_with_content():
    hugo_content = main.hugo_with_content("Sermon 01", "false", "Soli Deo Gloria")
    assert main.hugo_with_content("Sermon 01", "false", "Soli Deo Gloria") \
           == main.hugo_header("Sermon 01", "false") + "Soli Deo Gloria"

def test_save_file_contents(file_fixture):
    # create a file to test
    with open(file_fixture, 'r', encoding="utf-8") as f:
    # read the contents of the file
        text = f.read()
    assert text == "Soli Deo Gloria"

def test_open_results(file_fixture):
    # check if it returns expected string
    # expected string is from fixture
    assert main.open_results(file_fixture) == "Soli Deo Gloria"

def test_download_yt():
    # if already downloaded it will return the exisitng file
    # delete file that was downloaded for testing
    url = "https://www.youtube.com/watch?v=2Nc7_9I76HI"
    save_name = "GraceLife London_test"
    output = main.download_yt(url, save_name)
    file_mp3_save = f"{save_name}.mp3"
    assert output == file_mp3_save
    os.remove(file_mp3_save)

def test_transcribe_save(download_file):
    file_name_no_extension = download_file.split(".")[-2]
    # compare two files and if they are equal test passed
    # TODO
    # assert main.transcribe_save(download_file) == main.open_results(download_file)
    
    # test file was saved
    assert os.path.exists(f"results/{file_name_no_extension}.md") == True
    
    # TODO have a robust vector-dot product based comparison of 
    # two texts and test fails if they are below a threshold.  

def test_transcribe(download_file):
    text_expected = r""" This is London, a city without walls, everybody's busy without cause. This is London, a city seemingly without flaws because the truth is net outlawed. This is London, the capital where capital appears to be the life source. This is London, the city that never sleeps is without pause, living life and fast forward from south-east to west-north, the people just ignore God, as though he doesn't reign and as though his son isn't coming again, but the gospel cannot be chained as the truth is boldly proclaimed, the Lord is gathering in saints, our preaching is not in vain and so we anticipate the day that this London will know Jesus saves. London is a very dark place, there is very little light in London. We become more of an agnostic and atheist country. Materialistic, heavy on celebrities. It's somewhere where people can just get swept along with the busyness of life. That really started to really burden my heart that this land that we live in really needs the truth, needs the gospel. To begin a church in central London just seems impossible and yet God opened the doors. Within literally a few weeks we were here. So we knew from the start that our job every day was not to do something remarkable to transform London, our job every day was to be faithful, to bring God's word to God's children so that they might grow and go into the world with the gospel. It's the word of God that changes lives and it's the word of God that equips the saints for the work of the ministry and so that was our focus, we didn't have any strategy only to just do what the word taught us to do. And that's it, it's so simple, heartfelt, humble obedience to God's word. God's word just brings people to life. It's something which if you're only exposed to it and you only hear the word of God, as God's child, as Jesus said, my sheep hear my voice. It's crazy because we came on the first Sunday, Tom and Ross both spoke and they said, you know, we're going to preach about, we're going to preach the Bible, we're actually going to preach the Bible verse by verse, we're going to go verse by verse and we're going to tell you, we're going to preach the Bible, we're going to talk about sin, we're going to talk about Christ, we're going to talk about all of these biblical concepts. You don't get some kind of fake interpretation or this is Tom's interpretation of this passage, this is Ross's, this is just, this is the word. The reason we spend so much time preparing is because we need it to be not our message but the message that comes from God. It leads us to want to learn it in that way as well. It encourages us to go and research, not just to read the Bible and if we don't understand just kind of leave it and, you know, but actually, you know, go and search up theologians, go and search up these preachers. You know, to be a part of a hungry congregation is just, there are not many words to explain it but it's so very encouraging. Coming to Grace to Life London, you could really, like, it just came to life. It was like the Bible, the people who were in Acts and stuff, it was like, that's them. It's like real life Christianity. I love the fellowship at Grace to Life. It's something I can't really put my finger on. It's godly, I think. That's the word. It's really godly. It's just a great, great church family feel. You feel like you want to live with these people? That's right. You feel like if it could be, like, we could all live, like, in the basement or something, like, forever. The community, the church family, just want to serve the Lord and how they would serve the Lord is by serving each other with selfless love. It's just been an amazing thing to see. We are living in the most exciting point of redemptive history, outside of being a disciple walking with Christ. Tom and Ross have come in and kind of given us, implanted in our hearts, you know, the idea to save London and to make London known, make the gospel known. Gospel, gospel, gospel, gospel, like, there's not, I don't remember, in the past few months I've been, I don't remember one sermon where the gospel was not preached. Anything is possible. It's possible for this country to be re-evangelised, to be, to be one again for Christ. There needs to be another generation of young men confident in the Bible that they have in their hands, willing to die for it if necessary, willing to go out with that Bible and nothing else and just to say to people, this is what God says. If we can pass on this truth and train other teachers and teach men and women to be passing on the truth to the next generation, then it doesn't all stop here and who knows what God will do in the future."""
    
    assert main.transcribe(download_file) == text_expected