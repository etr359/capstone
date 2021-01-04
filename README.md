# Predicting Professional Soccer Players Transfer Values 

**Author**: Eric Roberts

## Business Problem

Soccer is the worlds most popular sport with an estimated 4 billion fans worldwide. Increasingly it is becoming big business; during the 2017/2018 season the European football market generated €28.4 billion in revenue, €15.6 billion from the 'big 5' European leagues alone (the big 5 leagues are the top tier leagues in England, France, Germany, Italy, and Spain). Winning, often the primary goal, is also key to capitalizing on this market opportunity.  Transfers, the buying and selling of player registrations between professional clubs, is key to both on-field success and also represents a huge area of investment.  During the 2019 summer transfer window clubs from Europe's big 5 leagues spent a record €5.5 billion on transfers.

Problematically, the transfer market is notoriously volatile and emotional with selling clubs often holding the power to set prices and ardent fan bases putting pressure on clubs to "do business". Machine Learning can bring levity to this process by providing information to purchasing clubs.  Here I build build a prediction model of professional soccer player's transfer values to help purchasing clubs benchmark quoted prices for players they are interested in purchasing.

***
Goal:
* Build a prediction model for the transfer value of professional soccer players.
***

## Data

Demographic and performance data was scraped from [fbref](https://fbref.com/en/).  More than 175 features including age, nationality and detailed performance data covering shooting, passing, pass types, goal and shot creation, defensive actions, possession, playing time and miscellaneous statistics was scraped.  Detailed performance data was available on fbref only for the Big 5 European leagues for the 2017/2018, 2018/2019, 2019/2020 seasons. It is not uncommon for players to play for multiple teams in one season.  Therefore to fully capture a season's worth of performance data, performance statistics were summed by player name, date of birth and year.  As goalkeepering is an intrinsically differenent position with different performance metrics they were excluded from our analytic sample.

Data on transfers was scraped from [Transfermarkt](https://www.transfermarkt.us/). I decided to model the transfer value as a function of performance data lagged by one year.  Therefore, to faciliate merging transfer information with demographic and performance data I gathered infomation on all incoming transfers for all clubs in the top tier of the English, French, German, Italian, Spanish, Russian, Dutch and Portuguese leagues for the winter and summer transfer windows for the past 3 years (starting with transfers in summer 2018 and ending with summer 2020).  Winter transfers were modeled as a function of the preceding full season, e.g., a transfer from January 2019 was modeled as a function of that players performance in the 2017/2018 season. The Russian, Dutch and Portuguese leagues (the next 3 strongest leagues in the world according to UEFA rankings) were included to increase the sample size for cases in which teams in those leagues purchased a player from a Big 5 league.

## Methods

Exploratory data analysis assessed the distribution of the transfer value and its association with demographics and key performance metrics overall and stratified by position.  To predict the transfer value I compared the performance of a series of three different linear regressions (OLS, Ridge and Lasso), on two different sets of features (a reduced set of features chosen for interpretability, and the first 6 principle components on a PCA of the full set of features) for both first and second order polynomials. Models were compared using the RMSE and adjusted r-squared on a 20% train-test split. 


## Results

We scraped information on 9666 transfers.  Our final analytic sample was 678 transfers after the following exclusions - 288 duplicate entries, 5056 loans, 1139 free transfers, 1010 academy promotions, 1448 transfers were from clubs not in the Big 5 of Europe and 47 Goalkeepers were excluded.

The mean transfer fee was £11,944,740 (std = £14,806,470) with a median value of £7,200,000 (IQR: £2,700,000 - £16,200,000).  Figure 1 shows the distribution of transfer fee overall and logged to correct the skewness.  All models utilized the logged outcome. 

### Figure 1
![Figure 1](/Images/transfer_fee_dist_unlogged_and_logged.png)
![Figure 1](/images/transfer_fee_dist_unlogged_and_logged.png)

Figure 2 shows the distribution of logged transfer fee by positions. Attackers had a highest mean transfer fees (£13,949,840), midfielders second highest (£11,165,590) and defenders the lowest (£10,418,530). 

### Figure 2
![Figure 2](/Images/dist_trans_fee_by_position.png)

The distribution of transfer fee was significantly (p-value = 0.02) different by nationality with English (£19,684,760) and Brazilian (£19,142,800) players having the highest mean transfer fees (Figure 3). 

### Figure 3
![Figure 3](/Images/dist_trans_fee_by_nationality.png)

Generally speaking, the relationship between performance metrics and transfer fee was small to moderate with most correlations between 0.15 and 0.35.  The metrics that tended to have the highest correlation with transfer fee were offensive statistics.   Stratified by position the relationship between transfer fee and offensive performance metrics was strongest for attackers and midfielders had moderate relationships for most metrics.  Defenders, however, tended to have the smallest correlation between transfer fee and performance metrics even for key defensive performance metrics. 

To illustrate the relationship between performance metrics and transfer fee we present two key findings in figure 4.  Generally speaking, performance metrics only had a small to moderate correlation with the logged transfer fee with 

overall correlation of xg with fee: r=0.326, p=0.0
correlation of xg with fee for attackers: r=0.431, p=0.0
correlation of xg with fee for midfielders : r=0.319, p=0.0
correlation of xg with fee for defenders: r=0.227, p=0.001

overall correlation of clearances with fee: r=0.038, p=0.343
correlation of clearances with fee for attackers: r=0.176, p=0.005
correlation of clearances with fee for midfielders : r=0.224, p=0.006
correlation of clearances with fee for defenders: r=0.131, p=0.051


### Figure 4
![Figure 4](/Images/Scatter_trans_fee_xg_clearances.png)

### Table 1. Correlation of transfer fee with expected goals and clearances overall and by position.
Correlation of transfer fee with expected goals and clearances overall and by position.
|             | Expected Goals |         | Clearances     |         |
|-------------|----------------|---------|----------------|---------|
| Group       | Correlation    | P-value | Correlation    | P-value |
| Overall     | 0.326          | <0.05   | 0.038          | 0.34    |
| Attackers   | 0.431          | <0.05   | 0.176          | 0.01    |
| Midfielders | 0.319          | <0.05   | 0.224          | 0.01    |
| Defenders   | 0.227          | <0.05   | 0.131          | 0.05    |


## Conclusions and Next Steps

We report a model to classify the sentiment of technology related tweets with over 92% accuracy.  Our content analysis created actionable insights for stakeholders.

The dataset is restricted to tweets from one festival in one year limiting its generalizability. To illustrate, this data set is from the 2011 SXSW when the iPad 2 was released, hence it's high frequency count among tweets with a positive valence.  However, it's likely that as technology updates older versions of products may be referenced negatively.  Incorporating tweets from consequtive years may help address this shortcoming.

Furthermore, our prediction model was fit to the entire dataset.  It's possible improvements in prediction, and utility, may come from training the model to identify positive and negative tweets related to specific brands.

## For More Information

Please review our full analysis in [our Jupyter Notebook](./SentimentAnalysis.ipynb) or our [presentation](https://docs.google.com/presentation/d/1Yv25gIvnjTro58RzoQQlWH8ScWMWAmlaDA5BKMhcFyI/edit?usp=sharing).

For any additional questions, please contact Eric Roberts etr359@gmail.com**

## Repository Structure

```
├── README.md                    <- The top-level README for reviewers of this project
├── SentimentAnalysis.ipynb      <- Narrative documentation of analysis in Jupyter NB
├── AncillaryAnalyses            <- Notebooks containing ancillary analyses 
├── data                         <- Both sourced externally and generated from code
└── images                       <- Both sourced externally and generated from code