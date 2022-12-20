from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config, AutoTokenizer, AutoModelWithLMHead, \
    AutoModelForSeq2SeqLM
import torch
import string
from wordcounter.wordcounter import WordCounter

class Summarization:

    def PreProcess(self, Document):
        preprocess_text = Document.strip().replace("\n", " ")
        preprocess_text = preprocess_text.lower()
        preprocess_text = preprocess_text.translate(str.maketrans('', '', string.punctuation))
        return preprocess_text

    def Summarize(self, Document, CompressionRate):
        model = T5ForConditionalGeneration.from_pretrained('t5-small')
        tokenizer = T5Tokenizer.from_pretrained('t5-small')
        device = torch.device('cpu')
        preprocess_text = self.PreProcess(Document)
        t5_prepared_Text = "summarize: " + preprocess_text
        tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt", max_length=5000, truncation=True).to(
            device)
        wordcounter = WordCounter(Document, delimiter=' ')
        docLength = wordcounter.get_word_count()

        maxLength = int(docLength * (CompressionRate / 100))
        summary_ids = model.generate(tokenized_text,
                                     num_beams=2,
                                     no_repeat_ngram_size=2,
                                     min_length=maxLength,
                                     max_length=docLength,
                                     early_stopping=False)

        output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        return output