# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request

class MortgagelistSpider(scrapy.Spider):
    name = "mortgagelist"
    allowed_domains = ["wellsfargo.com"]

    def start_requests(self):
        #self.count = count
        for i in range(1, 21):
            url = 'https://www.wellsfargo.com/mortgage/rates/refinance-assumptions?prod='+str(i)
            print("URL:", url)
            yield Request(url, self.parse)


    def parse(self, response):
        Down_Payment= response.xpath('//*[@id="contentBody"]/table[1]/tbody/tr[4]/td/text()').extract_first()
        Down_Payment = Down_Payment.strip()
        item ={
            'Loan_Category': response.css('h1.c11::text').extract_first(),
            'Credit_Score' : response.css('div#contentBody > p::text').extract_first(),
            'Funding_Type' : response.css('h2.c66title > a[data-content-id="844563516"]::text').extract(),
            'Bank_Product_Name' : response.css('table.c65Table > thead > tr > th.c66tableTitle::text').extract(),
            'Interest_rate' : response.xpath('//*[@id="contentBody"]/table[1]/tbody/tr[1]/td/text()').extract(),
            'APR_Rates' : response.xpath('//*[@id="contentBody"]/table[1]/tbody/tr[2]/td/text()').extract(),
            'Loan_Amount': response.xpath('//*[@id="contentBody"]/table[1]/tbody/tr[3]/td/text()').extract(),
            'Down_Payment':Down_Payment,
            'Term_Tenor' : response.xpath('//*[@id="contentBody"]/table[1]/tbody/tr[5]/td/text()').extract(),
        }
        yield item





