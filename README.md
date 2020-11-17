# Auto poster to Yandex Zen
Python 3 tool for articles posting to your Yandex Zen channel (based on Selenium). The script takes a title, text and media files supported by Yandex Zen, publishes and returns a link to a new article.

### Requirements ###
The script requires [Selenium](https://pypi.org/project/selenium/) library and the [chromedriver](https://chromedriver.chromium.org/) file in the project folder. And of course you need a Yandex account with your Zen channel.

### Usage ###
Each element of the article (title, paragraph, media file, tags) has its own method.
After creating instance of YandexZenPoster class the script logs into your Yandex account. To initialize creating of new article use `create_new_post()` method. And to finalize article publication use `post()` method.
```python
from post-to-yandex-zen import YandexZenPoster
import os

new_post = YandexZenPoster(login='my_yandex_login', password='my_yandex_password', headless=True)
# headless deafault is True
# set headless=False if you want to see what exactly script does

new_post.create_new_post()
new_post.title(text='Title of my new article')
news_post.text_block(text='Paragraph 1 of my new amazing article')
news_post.photo(path=os.path.abspath("mydir/image.jpg")) # The absolute path is required!
news_post.text_block(text='Paragraph 2 of my new amazing article')
new_post.hashtags(tags=['cats', 'love, 'python'])
link = new_post.post()
```
### List of methods ###
* `create_new_post()`: initializes the creation of the article (i.e. opens the post editor)
* `title(text)`: title of the future article. Variable **text** is required. Call this method only after create_new_post()
* `text_block(text)`: paragraph of the future article. Variable **text** is required. Call this method only after create_new_post()
* `photo(path)`: uploads media file. An absolute path is required. Call this method only after create_new_post()
* `hashtags(tags)`: hastags of the future article. Variable **tags** is required. Tags should be passed as list or str (if there is a single hashtag). Call this method only after create_new_post()
* `create_new_post()`: finalizes the creation of the article (i.e. post_it). Returns link to the new article. Call this method only after all content is ready


