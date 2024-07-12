# codedex-track3-hackathon
The purpose behind this Track was to predict the winners of the 2024 Paris Summer Olympics.


In my implementation I made use of Pyhton (Flask) in order to make a web application that displays my predicted findings.


I will go over how I was able to produce my Project:

So, initially I got the following dataset from Kaggle: https://www.kaggle.com/datasets/piterfm/olympic-games-medals-19862018 [results.csv]. This dataset holds all Olympic event results from 1896-2022.
I started cleaning this dataset, since I realised we will only need historic data for the Summer Olympics and fiured that it wouldn't really be relevant to include data so old that it would not effect current predictions. With this in mind, deleted all Winter Olympics records as well as all Summer Olympics records older than London 2012. In addition, I simplified the data into the following fields:
discipline_title,event_title,slug_game,medal_type,rank_equal,rank_position,country_name,country_code,country_3_letter_code

This can be seen in the cleaned dataset [updated_filtered_results.csv]:
![image](https://github.com/user-attachments/assets/0d8f2f80-2c60-48d7-aacd-8b1ebb75528f)

With this dataset, I wanted to simplify it even more by only storing the nations that were in the top 5 of each event. To do this, I ran the following code [remove_data.py]:
![image](https://github.com/user-attachments/assets/599db0d7-c210-4622-b70b-df32c92e6cf6)

The above code produced olympic_rank_counts.csv, which can be seen below:
![image](https://github.com/user-attachments/assets/8c21d120-79de-4e28-adc9-06289e696fdd)

Now that the data is in a more appropriate format, I was able to start making predictions on the dataset. I made use of sklearn in order to develop a prediction model (The following segment can be seen in predict_script.py).

I started with loading the data and started with normalizing the data by assigning weights based on the olympic event. I figurerd that, the more recent the olympic event was, the greater the weight should be since it would be more likely for a nation to achieve gold, silver or bronze is they more recently achieved those medals. I followed this by defining the target variables for the prediction, which were the events per nation and then merged these columns into a new dataframe:
![image](https://github.com/user-attachments/assets/8022348c-a488-4b61-baa0-7047dbd6c8fb)


I then started with the model construction and split data into training and testing sets. Following this, I was able to make predictions and evaluate these predictions with the data that had been trained:
![image](https://github.com/user-attachments/assets/2bea7382-5ab2-4a28-964f-85c9437a66ab)


I then stored the prediction data in a file named olympic_predictions_2024.csv:
![image](https://github.com/user-attachments/assets/e4856a0e-0ebf-457b-b69c-d3dd54577253)

Which looked like the following:
![image](https://github.com/user-attachments/assets/b60e8607-0615-47c5-97d6-69c80c7f2146)

This was great, however, I wanted to clean this up so that we only have the predicted values instead of the weights as well, so I made use of clean_data.py to clean the data and ended up getting the following [processed_olympic_predictions_2024.csv]:
![image](https://github.com/user-attachments/assets/b84ef47f-5546-4f6f-9ff0-140e70a57314)


And from this point forward, I made use of processed_olympic_predictions.csv as my prediction set :)
