from transformers import AutoModelWithLMHead, AutoTokenizer
from allennlp.predictors.predictor import Predictor
from rake_nltk import Rake

tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")
model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-question-generation-ap")

def get_question(answer, context, max_length=64):
  input_text = "answer: %s  context: %s </s>" % (answer, context)
  features = tokenizer([input_text], return_tensors='pt')

  output = model.generate(input_ids=features['input_ids'],
               attention_mask=features['attention_mask'],
               max_length=max_length)

  return tokenizer.decode(output[0])

# context = "Manuel has created RuPERTa-base with the support of HF-Transformers and Google"
context = "the effectiveness of transfer learning has given rise to a diversity of approaches, methodologies, and practice." \
          " in this paper, we explore the landscape of transfers learning techniques for natural language processing (NLP)" \
          " the systematic study compares pre-training objectives, architectures, unlabeled datasets and transfer approaches" \
          " on dozens of language understanding tasks. we achieve state-of-the-art results on many benchmarks covering summarization," \
          " question answering, text classification."

r = Rake()
r.extract_keywords_from_text(context)
ans = r.get_ranked_phrases()[0]
print(ans)
answer = ans

question_to_answer = get_question(answer, context)
print("Question:" + question_to_answer)






## Old Model commented
# predictor = Predictor.from_path("https://s3-us-west-2.amazonaws.com/allennlp/models/bidaf-model-2017.09.15-charpad.tar.gz")
predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/bidaf-model-2020.03.19.tar.gz")

passage = """
By 55,000 years ago, the first modern humans, or Homo sapiens., had arrived on the Indian subcontinent from Africa, where they had earlier evolved.[63][64][65] The earliest known modern human remains in South Asia date to about 30,000 years ago.[66] Nearly contemporaneous human rock art sites have been found in many parts of the Indian subcontinent, including at the Bhimbetka rock shelters in Madhya Pradesh.[67] After 6500 BCE, evidence for domestication of food crops and animals, construction of permanent structures, and storage of agricultural surplus, appeared in Mehrgarh and other sites in what is now Balochistan.[68] These gradually developed into the Indus Valley Civilisation,[69][68] the first urban culture in South Asia,[70] which flourished during 2500–1900 BCE in what is now Pakistan and western India.[71] Centred around cities such as Mohenjo-daro, Harappa, Dholavira, and Kalibangan, and relying on varied forms of subsistence, the civilization engaged robustly in crafts production and wide-ranging trade
India is the world's most populous democracy.[203] A Parliamentary Republic with a multi-party system,[204] it has seven recognised national parties, including the Indian National Congress and the Bharatiya Janata Party (BJP), and more than 40 regional parties.[205] The Congress is considered centre-left in Indian political culture,[206] and the BJP right-wing.[207][208][209] For most of the period between 1950—when India first became a republic—and the late 1980s, the Congress held a majority in the parliament. Since then, however, it has increasingly shared the political stage with the BJP,[210] as well as with powerful regional parties which have often forced the creation of multi-party coalition governments at the centre
India is a federal union comprising 29 states and 7 union territories.[243] All states, as well in addition to the union territories of Puducherry and the National Capital Territory of Delhi, have elected legislatures and governments following on the Westminster system of governance. The remaining five union territories are directly ruled by the centre through appointed administrators. In 1956, under the States Reorganisation Act, states were reorganised on a linguistic basis.[244] There are over a quarter of a million local government bodies at city, town, block, district and village levels
According to the International Monetary Fund (IMF), the Indian economy in 2017 was nominally worth US$2.611 trillion; it is the sixth-largest economy by market exchange rates, and is, at US$9.459 trillion, the third-largest by purchasing power parity, or PPP.[16] With its average annual GDP growth rate of 5.8% over the past two decades, and reaching 6.1% during 2011–2012,[280] India is one of the world's fastest-growing economies.[281] However, the country ranks 140th in the world in nominal GDP per capita and 129th in GDP per capita at PPP.[282] Until 1991, all Indian governments followed protectionist policies that were influenced by socialist economics. Widespread state intervention and regulation largely walled the economy off from the outside world. An acute balance of payments crisis in 1991 forced the nation to liberalise its economy;[283] since then it has slowly moved towards a free-market system[284][285] by emphasising both foreign trade and direct investment inflows.[286] India has been a member of WTO since 1 January 1995
With 1,210,193,422 residents reported in the 2011 provisional census report,[330] India is the world's second-most populous country. Its population grew by 17.64% during 2001–2011,[331] compared to 21.54% growth in the previous decade (1991–2001).[331] The human sex ratio, according to the 2011 census, is 940 females per 1,000 males.[330] The median age was 27.6 as of 2016.[268] The first post-colonial census, conducted in 1951, counted 361.1 million people.[332] Medical advances made in the last 50 years as well as increased agricultural productivity brought about by the "Green Revolution" have caused India's population to grow rapidly.[333] India continues to face several public health-related challenges.[334][335]

Life expectancy in India is at 68 years, with life expectancy for women being 69.6 years and for men being 67.3.[336] There are around 50 physicians per 100,000 Indians.[337] Migration from rural to urban areas has been an important dynamic in the recent history of India. The number of Indians living in urban areas grew by 31.2% between 1991 and 2001.[338] Yet, in 2001, over 70% still lived in rural areas.[339][340] The level of urbanisation increased further from 27.81% in the 2001 Census to 31.16% in the 2011 Census. The slowing down of the overall growth rate of population was due to the sharp decline in the growth rate in rural areas since 1991.[341] According to the 2011 census, there are 53 million-plus urban agglomerations in India; among them Mumbai, Delhi, Kolkata, Chennai, Bangalore, Hyderabad and Ahmedabad, in decreasing order by population.[342] The literacy rate in 2011 was 74.04%: 65.46% among females and 82.14% among males.[343] The rural-urban literacy gap, which was 21.2 percentage points in 2001, dropped to 16.1 percentage points in 2011. The improvement in literacy rate in rural area is two times that in urban areas.[341] Kerala is the most literate state with 93.91% literacy; while Bihar the least with 63.82%
"""

result=predictor.predict(
  passage=context,
  question= question_to_answer
  # "how are union territoris managed?"
)
print("Answer:" + result['best_span_str'])
