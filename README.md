## Aspect Based Sentiment Analysis for Hindi (ABSA)

### problem statement 
In recent years, millions of people are into social media networking, blogs and review sites, where they express opinions of various entities including movies, restaurants, products etc. These websites provide myriad amount of information that are not only useful to the creators of these entities, but also to their customers and rivals. The field of Aspect Based Sentiment Analysis (ABSA) collects and analyzes the opinions expressed on various aspects of these entities to make decisive recommendations. Rather than considering the overall polarity of a review expressed by a customer, it would be more helpful to analyze feature specific opinions, since people tend to have mixed opinions about them. Consider the sentence,

> The ***pizza*** was delicious but the ***service*** was awful

In this sentence, the customer has expressed his opinion on the aspect, pizza, with a positive sentiment and service with a negative sentiment. Hence, it is of utmost importance to extract these feature specific sentiments and their categories to provide a granular level of recommendation. Our project aims at developing and analyzing ABSA models on Hindi reviews.

### Requirements

Required Python packages
- numpy >= 1.12.1
- scipy >= 0.19.0
- scikit-learn >= 0.18
- pandas >= 0.19

Additional packages
 - [CRF++ 0.58](https://taku910.github.io/crfpp/) 
 - Hindi Wordnet by [Siva Reddy](http://sivareddy.in/downloads)
 - Hindi Sentiwordnet
 - Hindi dependency parser by [Siva Reddy](http://sivareddy.in/downloads)


You can install project dependencies by running following command:
```sh
$pip install -r requirements.txt
```
---
Authors

- [Nisarg Patel](https://github.com/pnisarg)
- [Nikhil Pachpande](https://github.com/pachpandenikhil)
- [Abijith Sankar KN](https://github.com/abijithsankar)
- [Atharva Kale](https://github.com/athkale)


---
##### License
MIT
