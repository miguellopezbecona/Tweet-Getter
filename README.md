## Overview
This repo consists in a simple app using [python-twitter](https://github.com/bear/python-twitter) library to fetch all the tweets the service allows from a determined user, and dumps them to a text file. It is intended to be a fast solution to those who do not want to lose time fighting with the API. I will not include my private dev keys, so **you have to put your own in your local copy of the source code before using it**.

## Using
As mentioned before, the app depends on [python-twitter](https://github.com/bear/python-twitter) library, so you must need to have it installed, though it is quite easy (the link provides a installation guide if needed). Then, you can use the app by typing:

```bash
python Tweet-Getter.py -u username_whose_tweets_will_be_fetched [-rt]
```

*u* parameter is mandatory, while the *rt* flag (it must not include a value) is not. This flag simply chooses wheter to fetch retweets as well or not. If everything went okay, the app will generate a text fille called *username_whose_tweets_will_be_fetched*.txt where the tweets will be dumped.

## License
You are completely free to adapt part of the source code to your project.
