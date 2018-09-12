# tweet-stargazer

This is a set of openfaas Serverless functions that handles github stared event and tweet about it

Here's how it works:

* Star a GitHub repository (configured by placing a webhook in your settings page)
* github-star function receives the JSON, downloads the user's avatar
* tweet-stargazer is called with the image - invokes a polaroid function with the image and Tweets it

Dependencies:
* [OpenFaaS](https://github.com/openfaas/faas)

Functions:
* Functions in stack.yml
 * github-star (python)
 * tweet-stargazer (python)
 * get-avatar (python)
 * polaroid (bash)

Your Twitter API tokens need to go into a `twitter_secrets.yml` file.
