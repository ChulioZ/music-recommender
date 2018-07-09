The Music Recommender System takes songs as input and recommends songs that are similar to them. Have a song you like and want to hear more like it? Try it out!
You won't get recommendations based on "what other users like that also like your song" as most recommendation systems provide. Instead, songs are compared based on technical, "inner" values - their loudness, their tempo, their mode for example.

Use the Music Recommender System:

1. Install Python (the project was developed with Python 3.6 and was not tested for compatability with other Python versions)

2. Clone the GitHub project (Attention: The files from the project are quite large as we have to deal with roughly 1 million songs and their information, so the txt files containing the JSON objects that hold this information are pretty big)

3. pip install -r requirements.txt

4. python main.py

5. visit your browser on page http://127.0.0.1:5000 and follow the instructions there

This project uses the Million Song Dataset. Want to learn more about it? Check this paper:

Thierry Bertin-Mahieux, Daniel P.W. Ellis, Brian Whitman, and Paul Lamere. The Million Song Dataset. In Proceedings of the 12th International Society for Music Information Retrieval Conference (ISMIR 2011), 2011.