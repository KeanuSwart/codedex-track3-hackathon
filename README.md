# codedex-track3-hackathon
My implementation of Track 3 for Codedex Summer Hackathon 2024.

The purpose behind this Track was to predict the winners of the 2024 Paris Summer Olympics.

In my implementation I made use of Pyhton (Flask) in order to make a web application that displays my predicted findings.

I will go over how I was able to produce my Project:
So, initially I got the following dataset from Kaggle: https://www.kaggle.com/datasets/piterfm/olympic-games-medals-19862018 [results.csv]. This dataset holds all Olympic event results from 1896-2022.
I started cleaning this dataset, since I realised we will only need historic data for the Summer Olympics and fiured that it wouldn't really be relevant to include data so old that it would not effect current predictions. With this in mind, deleted all Winter Olympics records as well as all Summer Olympics records older than London 2012. In addition, I simplified the data into the following fields:
discipline_title,event_title,slug_game,medal_type,rank_equal,rank_position,country_name,country_code,country_3_letter_code
This can be seen in the cleaned dataset [updated_filtered_results.csv].


