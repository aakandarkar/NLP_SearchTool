import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import spacy
import string
import gensim
import operator
import re
from fuzzywuzzy import fuzz
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

#pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)


brands_url = 'https://drive.google.com/file/d/1hPCAp4xx4PaDG_OLTJhYlhICc4WdgbDy/view?usp=sharing'
categories_url = 'https://drive.google.com/file/d/1SR6oGRnB4ULk9umnxZztHYKiHDI-VSag/view?usp=sharing'
offers_url = 'https://drive.google.com/file/d/18krLxNoBx9wFgtkXZiyL9Oh8B6w1hN40/view?usp=sharing'
brands_url='https://drive.google.com/uc?id=' + brands_url.split('/')[-2]
categories_url='https://drive.google.com/uc?id=' + categories_url.split('/')[-2]
offers_url='https://drive.google.com/uc?id=' + offers_url.split('/')[-2]

brands_df = pd.read_csv(brands_url)
categories_df= pd.read_csv(categories_url)
offers_df = pd.read_csv(offers_url)

# brands_df = pd.DataFrame(brands)
# offers_df = pd.DataFrame(offers)
# categories_df = pd.DataFrame(categories)


def map_retailer(offer_text):
    for retailer in reatiler_list:
        if retailer.lower() in offer_text.lower():
            return retailer
    return 'Unknown'

def get_matching_string(str1, str2):
    similarity_score = fuzz.token_set_ratio(str1, str2)
    return str2 if similarity_score >= similarity_threshold else 'Unknown'

def vectorize_data_based_on_metadata(product_input):

    vec = count_vec.transform(pd.Series(product_input))

    simil = cosine_similarity(vec, count_vec_matrix)

    simil_scores = pd.DataFrame(simil.reshape(count_vec_matrix.shape[0],), index = all_merge_df.index, columns=['score'])

    # Don't return scores of zero, only as many positive scores as exist
    non_zero_scores = simil_scores[simil_scores['score'] > 0]

    if len(non_zero_scores) == 0:
        print('--from vectorize_data_based_on_metadata() --> No similar products found.  Please refine your search terms and try again')
        return pd.DataFrame(columns=['Offers', 'score']), pd.DataFrame(columns=['score'])

    if len(non_zero_scores) < 10:
        item_count = len(non_zero_scores)
    else:
        item_count = 10

    similarity_scores = simil_scores.sort_values(['score'], ascending=False)[:item_count]
    data = {
    'Offers': all_merge_df['OFFER'].iloc[similarity_scores.index],
    # 'Search_Score': similarity_scores
    }
    df = pd.DataFrame(data)

    return df,similarity_scores


#offers_df  #---We can see here there are Null values present in Reailer columns

brands_df.rename(columns={'BRAND_BELONGS_TO_CATEGORY': 'PRODUCT_CATEGORY'}, inplace=True)
#We dont need RECEIPTS column in this tool as there is no use of receipts in the tool search.
brands_df.drop("RECEIPTS", axis=1, inplace=True)

#Now we will check if we have any duplicates for pair of Brand and Product category
brands_df.drop_duplicates(subset=['BRAND', 'PRODUCT_CATEGORY'], inplace=True)


#print(brands_df.info())
#brands_df have null value in brand columns which we can get rid of.
brands_df = brands_df.dropna()
#print(brands_df.info())
#print(offers_df.info())
#Retailer columns have 146 null values which will create issues, but we can not remove these null value rows because 146 is 38% of total records.
#To solve this problem we will look for any reatilers present in offers column, to see if we get any match.
#print(categories_df.info())
#categories_df doesnt have any null values in either of the columns

reatiler_list = offers_df['RETAILER'].dropna().unique()



offers_df['Mapped Retailer'] = offers_df['OFFER'].apply(map_retailer)
#print(offers_df.info())
#print("Unknown Retailers:",offers_df['Mapped Retailer'].value_counts().get('Unknown', 0))

#offers_df
# We can see that for cases like given below
#### "Spend $50 on a Full-Priced new Club Membership"	"SAMS CLUB"	"SAMS CLUB"
# we can not map directly the SAMS CLUB from the offer as the whole keyword is not present
# We can try the partial matching of the keywords

# Lets find the similarity in the keywords first
similarity_threshold = 50
# We stareted with threshold 80 but there were no significant matches
offers_df['Match_Retailer'] = offers_df.apply(lambda row: get_matching_string(row['OFFER'], row['RETAILER']), axis=1)

#print("Unknown Retailers:",offers_df['Mapped Retailer'].value_counts().get('Unknown', 0))
#Even after finding partial matches we got the same result as orignal values.

#At this point we dont have any other option to move ahead with Retailer value "Unknwon"
#only column we will use is match_retailer named as RETAILER
columns_to_drop = ['Mapped Retailer',"RETAILER"]
offers_df.drop(columns_to_drop, axis=1, inplace=True)
offers_df.rename(columns={'Match_Retailer': 'RETAILER'}, inplace=True)

brand_categ_df = pd.merge(brands_df, categories_df, on=['PRODUCT_CATEGORY'])

all_merge_df = pd.merge(brand_categ_df,offers_df, on = ["BRAND"])

all_merge_df['metadata'] = all_merge_df.apply(lambda x : x['BRAND']+' '+x['PRODUCT_CATEGORY']+' '+x['IS_CHILD_CATEGORY_TO']+' '+x['OFFER'], axis = 1)
count_vec = CountVectorizer(stop_words='english')
count_vec_matrix = count_vec.fit_transform(all_merge_df['metadata'])

@app.route('/', methods=['GET'])
def index():
      return render_template('index.html')

@app.route('/search', methods=['GET','POST'])
def search_offers():
        if request.method == 'POST':
            offers_df,score = vectorize_data_based_on_metadata(request.form['searchbar'])
            offers_df['score'] = score
            result_df = offers_df.reset_index(drop=True)
            if offers_df is not None:
                if len(offers_df) > 0:
                    return render_template('result.html', tables=[offers_df.to_html(classes='data')], titles=offers_df.columns.values)
                else:
                    error_message = "No similar products found. Please refine your search terms and try again."
                    return render_template('result.html', error_message=error_message)
            else:
                error_message = "An error occurred during processing. Please try again later."
                return render_template('result.html', error_message=error_message)
        else:
             return render_template('result.html', error_message="Please use the search form to submit a query.")

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=3001)
