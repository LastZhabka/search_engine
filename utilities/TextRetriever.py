from bs4 import BeautifulSoup
import PyPDF2
import io

class TextRetriever:
    def retrievePDFText(responseContent):
        file = PyPDF2.PdfReader(io.BytesIO(responseContent))
        textContent = []
        for page_num in range(len(file.pages)):
            page = file.pages[page_num].extract_text().split('\n')
            for text in page:
                if len(textContent) == 0 or len(text) == 0 or text[0] < 'a':
                    textContent.append(text)
                else:
                    textContent[len(textContent) - 1] += text
        return textContent

    def retrieveHTMLText(responseСontent):
        return BeautifulSoup(responseСontent, "html.parser").get_text(separator = " # ", strip = True).split(" # ")