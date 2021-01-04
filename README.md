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

Exploratory data analysis assessed the distribution of the transfer value and its association with demographics and key performance metrics overall and stratified by position.  To predict the transfer value I compared the performance of a series of three different linear regressions (OLS, Ridge and Lasso), on two different sets of features (a reduced set of features chosen for interpretability, and the first 6 principle components on a PCA of the full set of features) for both first and second order polynomials. Models were compared using the RMSE and adjusted r-squared on a 20% train-test split. The values of lambda for Ridge and Lasso regression were determined using GridSearch.


## Results

We scraped information on 9666 transfers.  Our final analytic sample was 678 transfers after the following exclusions - 288 duplicate entries, 5056 loans, 1139 free transfers, 1010 academy promotions, 1448 transfers were from clubs not in the Big 5 of Europe and 47 Goalkeepers were excluded.

The mean transfer fee was £11,944,740 (std = £14,806,470) with a median value of £7,200,000 (IQR: £2,700,000 - £16,200,000).  Figure 1 shows the distribution of transfer fee overall and logged to correct the skewness.  All models utilized the logged outcome. 

### Figure 1
![Figure 1](/Images/transfer_fee_dist_unlogged_and_logged.png)

Figure 2 shows the distribution of logged transfer fee by positions. Attackers had a highest mean transfer fees (£13,949,840), midfielders second highest (£11,165,590) and defenders the lowest (£10,418,530). 

### Figure 2
![Figure 2](/Images/dist_trans_fee_by_position.png)

The distribution of transfer fee was significantly (p-value = 0.02) different by nationality with English (£19,684,760) and Brazilian (£19,142,800) players having the highest mean transfer fees (Figure 3). 

### Figure 3
![Figure 3](/Images/dist_trans_fee_by_nationality.png)

Generally speaking, the relationship between performance metrics and transfer fee was small to moderate with most correlations between 0.15 and 0.35. The metrics that tended to have the highest correlation with transfer fee were offensive statistics. Stratified by position, the relationship between transfer fee and offensive performance metrics was strongest for attackers while midfielders had moderate relationships for most metrics.  Defenders, however, tended to have the smallest correlation between transfer fee and performance metrics even for key defensive performance metrics. To illustrate these relationships we present the relationship between transfer fee and the performance metrics expected goals and clearances in figure 4.  

### Figure 4
![Figure 4](/Images/Scatter_trans_fee_xg_clearances.png)

### Table 1. Correlation of transfer fee with expected goals and clearances overall and by position.
|             | Expected Goals |         | Clearances     |         |
|-------------|----------------|---------|----------------|---------|
| Group       | Correlation    | P-value | Correlation    | P-value |
| Overall     | 0.326          | <0.05   | 0.038          | 0.34    |
| Attackers   | 0.431          | <0.05   | 0.176          | 0.01    |
| Midfielders | 0.319          | <0.05   | 0.224          | 0.01    |
| Defenders   | 0.227          | <0.05   | 0.131          | 0.05    |

Tables 2-5 show the results of the series of models predicting transfer values. Generally speaking, none of the models accurately predict transfer values with no model having an RMSE less than £10,000,000.  It is also clear that without regularization the OLS models are overfit with second order polynomials.  The best model is the Ridge regression (lambda = 50) of second order polynomials on the first 6 principle components of all the features.

### Table 2. RMSE and adjusted R-square (20% train-test split) of OLS, Ridge and Lasso regression of a reduced set of features (first order polynomials) predicting transfer value in pounds.
|                        | train RMSE      | train adj R-square | test RMSE       | test adj R-square |
|------------------------|-----------------|--------------------|-----------------|-------------------|
| OLS                    |        11180629 |        0.31        |        18079019 |        0.127      |
| Ridge (lambda = 27)    |        11380364 |        0.306       |        17988762 |        0.138      |
| Lasso (lambda = 0.007) |        11261099 |        0.308       |        17947248 |        0.144      |

### Table 3. RMSE and adjusted R-square (20% train-test split) of OLS, Ridge and Lasso regression of a reduced set of features (second order polynomials) predicting transfer value in pounds.
|                       | train RMSE      | train adj R-square | test RMSE        | test adj R-square |
|-----------------------|-----------------|--------------------|------------------|-------------------|
| OLS                   |        13543810 |        0.474       |        616948550 |        -3.96E+24  |
| Ridge (lambda = 330)  |        10808972 |        0.365       |        18016336  |        0.14       |
| Lasso (lambda = 0.05) |        11727801 |        0.307       |        18144495  |        0.167      |


### Table 4. RMSE and adjusted R-square (20% train-test split) of OLS, Ridge and Lasso regression on first 6 principle components (first order polynomials) predicting transfer value in pounds.
|                       | train RMSE      | train adj R-square | test RMSE       | test adj R-square |
|-----------------------|-----------------|--------------------|-----------------|-------------------|
| OLS                   |        14494782 |        0.25        |        17085176 |        0.227      |
| Ridge (lambda = 100)  |        13620291 |        0.249       |        17167526 |        0.228      |
| Lasso (lambda = 0.02) |        13629797 |        0.249       |        17198892 |        0.226      |

### Table 5. RMSE and adjusted R-square (20% train-test split) of OLS, Ridge and Lasso regression on first 6 principle components (second order polynomials) predicting transfer value in pounds.
|                       | train RMSE       | train adj R-square | test RMSE       | test adj R-square |
|-----------------------|------------------|--------------------|-----------------|-------------------|
| OLS                   |        519962594 |        -0.207      |        49010846 |        -0.325     |
| Ridge (lambda = 50)   |        12161791  |        0.309       |        16720144 |        0.203      |
| Lasso (lambda = 0.05) |        11895724  |        0.3         |        17303987 |        0.212      |


## Conclusions and Next Steps

I report a model that predicts 20.3% of the variance in the transfer value of professional soccer players with a mean error of £16.7 million. These numbers are in part a reflection of the volatility of the transfer market and the fact that valuation is not soley based on a few demographic characteristics and one year of performance.  Not withstanding the non-trivial error the models may help clubs benchmark player valuations.

Future research could improve these models in a few important ways.  First, incorporating more observations.  I only had access to detailed performance metrics for players in the Big 5 leagues for 3 seasons.  Incorporating more years and more leagues would increase our sample size bringing stability to our estimates.  Second, incorporating more complex data. I modeled transfer fee as a function of performance metrics lagged by one year, however, player valuations are likely based on a body of work.  Models that incorporate career statistics are likely to improve prediction.  Third, incorporating data reflective of other important domains.  One particularly salient domain is the remaining contract which the transfer is purchasing.  It is well known that the length of the remaining contract or the size of a players salary influences the size of the transfer fee.

## For More Information

Please review the full analysis in [the Jupyter Notebook](./Modeling.ipynb) or our [presentation](https://docs.google.com/presentation/d/1ufv4H5kQAGmo9drzWyo7iYLDKzW7xde84ZQoPU704H8/edit?usp=sharing).

For any additional questions, please contact Eric Roberts etr359@gmail.com**

## Repository Structure

```
├── README.md                         <- The top-level README for reviewers of this project
├── Data cleaning.ipynb               <- Narrative documentation of data cleaning in Jupyter NB
├── EDA and feature engineering.ipynb <- Narrative documentation of EDA in Jupyter NB
├── Modeling.ipynb                    <- Narrative documentation of modeling in Jupyter NB
├── Webscrapers                       <- Notebooks containing webscrapers 
├── data                              <- Both sourced externally and generated from code
└── images                            <- Generated from code