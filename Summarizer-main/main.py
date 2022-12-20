from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config, AutoTokenizer, AutoModelWithLMHead
import torch
from webScraping import ReadFromWebSite
from ReadDocument import ReadingFromPDF


def Summarize(document):
    model = T5ForConditionalGeneration.from_pretrained('t5-small')
    tokenizer = T5Tokenizer.from_pretrained('t5-small')
    device = torch.device('cpu')
    preprocess_text = document.strip().replace("\n", " ")
    t5_prepared_Text = "summarize: " + preprocess_text
    tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt", max_length=5000, truncation=True).to(device)
    summary_ids = model.generate(tokenized_text,
                                 num_beams=2,
                                 no_repeat_ngram_size=2,
                                 min_length=10,
                                 max_length=100,
                                 early_stopping=False)

    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return output


def main():
    print('''
    please choose one of those choices :
        1) Summarize PDF
        2) Summarize Website
    ''')
    choice = input()
    Text = ''
    if choice == '1':
        # put PDF in project Directory 
        Text = ReadingFromPDF(filename="example.pdf",f=1,l=7)

        Text =   """
        The US has "passed the peak" on new coronavirus cases, President Donald Trump said and predicted that some states would reopen this month.

        The US has over 637,000 confirmed Covid-19 cases and over 30,826 deaths, the highest for any country in the world.

        At the daily White House coronavirus briefing on Wednesday, Trump said new guidelines to reopen the country would be announced on Thursday after he speaks to governors.

        "We'll be the comeback kids, all of us," he said. "We want to get our country back."

        The Trump administration has previously fixed May 1 as a possible date to reopen the world's largest economy, but the president said some states may be able to return to normalcy earlier than that.
        """

# Output
        print(Text)
    elif choice == '2':
        Text = ReadFromWebSite(WEBSITE='https://markmanson.net/best-articles')
        print(Text)

    print('************Summarized Text**************** : \n' + Summarize(Text))
        
if __name__ == "__main__":
    main()