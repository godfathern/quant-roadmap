# HAI : housing analytics and insights
## I build this to help first time home owner "time" the market to purchase a house

## Since condominiums represent the largest share of the market, we are prioritizing them for our initial price predictions.

In particular, we gonna predict the price "trend" of the 3.5 unit because it reprense the largest share of the market

In November 2025, the Montreal residential market confirmed notable changes in the pace of sales and in the composition of 
sales by property type. These developments are important for anyone who wants to understand turnover rates, 
demand pressure, and the most active segments of the market.

Property type	            % of sale	        Average time to sell
Condominiums	               51%	                    59 days
Single-family homes	           26%	                    52 days
Plexs	                       23%	                    59 days


## Implementation : 

We use STL + PCA --> SEQ2SEQ to predict

## Test : 

we use ratio 8:2 
8 for training and 2 for testing

## Target period : 

20 years : 2005-2025

## HPI : 
We use the seanally ajusted per month version of CREA





## Phase 2 : we preduct single-family homes and plexs


