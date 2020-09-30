# scrappy
scrapy best practice you don't want to miss
## requirements
    pip install requirements.txt
## structrue
	|____bin    #bash scripts
	|____requirements.txt
	|____scrappy
	| |____dbs    #storge dao
	| |____extensions    #scrapy extensions
	| |____items
	| |____middlewares
	| |____resources    #static resources
	| |____scripts    #py scripts
	| |____services    #py services
	| |____spiders    #spiders definition
	| |____utils    #python utils
	|____scrapy.cfg
	
## usage
&#160; &#160; &#160; &#160;_code some spider in spiders_

1.	extends CrawlSpider

2.	define name

3.	define [start_urls](http://doc.scrapy.org/en/latest/topics/spiders.html?highlight=start_urls#scrapy.spiders.Spider.start_urls) or [start_requests](http://doc.scrapy.org/en/latest/topics/spiders.html?highlight=start_requests#scrapy.spiders.Spider.start_requests) function

4.	define [parse](http://doc.scrapy.org/en/latest/topics/spiders.html?highlight=parse#scrapy.spiders.Spider.parse) function to parse the response

5.	define models in items

6.	define pipeline in pipelines

## notice

### items
*	__handleInsert__.

	parse the item before insert

*	__handleUpdate__.

	parse the item before update
	
### spiders
extends BaseSpider

*	__CrawlSpider__.

	normal spider
	
	_the spider will distributly if set __ENABLE_REDIS__ value to True in settings_
	
*	__scrappy.extensions.scrapy_redis.spiders.RedisSpider__.

	spider will not shutdown , always pop request form redis

### resource
*	__ResourceHelper__.

	reading, wirting and creating files
	
### middlewares
*	__RemoveCookieMiddleware__.

	remove cookie before request

*	__RandomProxyMiddleware__.

	random switch proxy before request
	
*	__UserAgentMiddleware__.

	random switch UserAgent before request
	
### setting

&#160; &#160; &#160; &#160;it will automatic switch configuration file (Linux as product platform)

*	__ENABLE_REDIS__.

	Enable redis distribution , redis stat



_have a nice day :)_
