import re # We will make use of regex to remove noise -check Regex101-
import nltk # Natural Language Toolkit. You need to pip install nltk first.
nltk.download('stopwords')
from nltk.corpus.reader.tagged import word_tokenize
nltk.download('punkt') # Tokenizer trained on unsupervised manner
import string

class ArCleaner(object):
  extra_stopwords = ['لقد' , "قد" ]
  stopwords = set(nltk.corpus.stopwords.words('arabic') + extra_stopwords)
  punctuations = '؛ـ،؟”…“–' + string.punctuation

  def remove_noise(self, txt):
    txt = re.sub(r'[\n]+', ' ', txt) # Remove \n
    txt = re.sub(r'[\s]+', ' ', txt) # Remove extra whitepaces
    return txt.strip()

  def remove_repetitions(self, txt, rep = 3, leave = 2):
    '''
      Remove >= {rep} repetitions of a character and leaving only {leave} repetitions
      Args:-
        rep: # consecutive occurences of a character
        leave: how many repetitions of the character you want to leave
    '''
    pattern = r'(.)\1{' + f'{rep}' + r',}'
    return re.sub( pattern, r'\1' * leave, txt)

  def remove_stopwords(self, txt):
    return ' '.join([ w for w in word_tokenize(txt) if w not in self.stopwords and len(w)>=2 ])

  def normalize_alif(self, txt, dagger_alif = True):
    '''
      Args:-
        dagger_alif: Specify whether you want to replace dagger alif with normal alif "ا" or not.
    '''
    # to "ا"
    txt = txt.replace(u"\u0623", u"\u0627")  # أ
    txt = txt.replace(u"\u0625", u"\u0627")  # إ
    txt = txt.replace(u"\u0622", u"\u0627")  # آ
    if dagger_alif:
      txt = txt.replace(u"\u0670", u"\u0627")  # dagger alif
    return txt

  def normalize_yaa(self, txt):
    return txt.replace(u"\u064A", u"\u0649") # "ي" to "ى"

  def remove_diacritics(self, txt, shaddah = True):
    '''
      Args:-
        shaddah: If True, this will remove shaddah from txt. If False, it will leave it.
    '''
    txt = txt.replace(u"\u064B", "")  # ً
    txt = txt.replace(u"\u064C", "")  # ٌ
    txt = txt.replace(u"\u064D", "")  # ٍ
    txt = txt.replace(u"\u064E", "")  # َ
    txt = txt.replace(u"\u064F", "")  # ُ
    txt = txt.replace(u"\u0650", "")  # ِ
    txt = txt.replace(u"\u0652", "")  # ْ
    if shaddah:
      txt = txt.replace(u"\u0651", "")  # shaddah
    return txt

  def remove_punctuations(self, txt):
    return ''.join([ ch for ch in txt if ch not in self.punctuations ])

  def clean_nuumbers(self, txt, toEng = False):
    '''
      This will remove all numbers in the txt unless toEng is True, then it will only change Arabic numbers to English.
      Args:-
        toEng: If true, numbers in txt will be only changed from Arabic to English. If false, all numbers will be removed.
    '''
    if toEng:
      txt = list(txt)
      for i,ch in enumerate(txt):
        if ch == '١':
            txt[i] = '1'
        elif ch == '٢':
            txt[i] = '2'
        elif ch == '٣':
            txt[i] = '3'
        elif ch == '٤':
            txt[i] = '4'
        elif ch == '٥':
            txt[i] = '5'
        elif ch == '٦':
            txt[i] = '6'
        elif ch == '٧':
            txt[i] = '7'
        elif ch == '٨':
            txt[i] = '8'
        elif ch == '٩':
            txt[i] = '9'
      return ''.join(txt)

    txt = re.sub('[\d+]', ' ', txt)
    return txt

"""Useful Resources for Regex:-
- [Regex Cheatsheet](https://www.dataquest.io/blog/regex-cheatsheet/)
- [Python Regex Documentation](https://docs.python.org/3/library/re.html)
- [Regex in Python Tutorial](https://realpython.com/regex-python/)

Other Arabic Preprocessing Tools:-
- [TCAR](https://github.com/Abdullah955/Text_cleaning_arabic_TCAR/tree/master)
"""