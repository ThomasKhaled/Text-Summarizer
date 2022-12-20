from kivy.app import App
from kivy.lang import Builder  # used to work with builder and apply any design file
from kivy.core.window import Window  # used to change the color of the back ground
from kivy.uix.screenmanager import ScreenManager, Screen  # used to apply multiple screens


from ReadDocument import ReadDocument
from SummarizeFunction import Summarization
from VideoCaptions.Video2Text import VideoCaptions
from wordcounter.wordcounter import WordCounter


# building different pages
from webScraping import webScraping

running_app = App.get_running_app()


class MainPage(Screen):
    pass


myText = ""


class TextPage(Screen):

    def __init__(self, text="", type_id=None, **kwargs):
        super(TextPage, self).__init__(**kwargs)
        self.text = text
        self.type_id = type_id

    ##########################################################

    def Summarize(self):
        print("printed: " + self.ids.userWrittenText.text)
        summarizer = Summarization()
        summarized_text = summarizer.Summarize(self.ids.userWrittenText.text, self.ids.slider.value)
        self.ids.summarized_label_id.text = summarized_text

        word_counter = WordCounter(self.ids.userWrittenText.text, delimiter=' ')
        doc_len = word_counter.get_word_count()

        word_counter = WordCounter(summarized_text, delimiter=' ')
        sum_len = word_counter.get_word_count()

        rate = str( round(sum_len/doc_len,3)*100 ) + '%'
        self.ids.compression_Ratio_Label_ID.text = rate

        print("done")

    ##########################################################
    def compression_Rate_Picked(self, value):
        self.ids.compression_Ratio_Label_ID.text = value


class FilePage(Screen):

    def viewselecteFile(self, filePath):
        try:
            self.ids.fileSelectedtxt.text = filePath[0]
        except:
            self.ids.fileSelectedtxt.text = ""

    def selectedVideo(self, filePath):
        captions = VideoCaptions()
        captions.getChunkCaption(filePath)
        print(captions.WriteCaptionInFile())
        layout = self.manager.get_screen('textPage').layout
        layout.text = captions.WriteCaptionInFile()

    def selectedFile(self, ischeckboxActive, filePath, first_page, last_page):
        if ischeckboxActive == False:
            self.ids.fileSelectedtxt.text = filePath[0]
            first_page = self.ids.startPagePDFtext.text
            last_page = self.ids.endPagePDFtext.text
            layout = self.manager.get_screen('textPage').layout
            # print("test: "+ReadingFromPDF(filename=filePath[0], f=1, l=4))
            docReader = ReadDocument()
            layout.text = docReader.ReadingFromPDF(filename=filePath[0], firstPage=first_page, lastPage=last_page)
        else:
            self.selectedVideo(filePath)


class UrlPage(Screen):
    def UserUrl(self, url):
        self.ids.urltxt.text = url
        layout = self.manager.get_screen('textPage').layout
        webScraper = webScraping()
        layout.text = webScraper.ReadFromWebSite(URL=url)

    pass


class PageManager(ScreenManager):
    pass


######################################################

# calling and building the design file (GUI)


TheApp = Builder.load_file('summarizeEnterpriseGUI.kv')


######################################################


######################################################
class SummarizeEnterprise(App):

    def build(self):
        # setting the color of the background
        Window.clearcolor = (52 / 255.0, 73 / 255.0, 94 / 255.0, 1)
        return TheApp  # sm


if __name__ == '__main__':
    SummarizeEnterprise().run()