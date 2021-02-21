import scrapy


class ArticlesSpider(scrapy.Spider):   #class du framework spider
    name = "articles"
    start_urls = [                                          #urls to scrape
                  'https://ar.hibapress.com/details-282361.html',
                   'https://ar.hibapress.com/details-284877.html',
                   'https://ar.hibapress.com/details-284846.html',
                    'https://ar.hibapress.com/details-284843.html',
                    'https://ar.hibapress.com/details-284788.html',
                    'https://ar.hibapress.com/details-284348.html'
                  ]

    def parse(self, response):              #la fonction qui definie les parties à scraper
        article_text = response.css('.tie-col-xs-12')

        title = article_text.css('.entry-title::text').extract()

        text = article_text.css('.aligncenter+ p , p::text').extract()
        article = ""                         #regrouper le texte scrapé
        for p in text:
            article += p

        # insertion dans la bdd
        yield {
            'title': title,
            'article': article,
            'label': 'True'
        }
