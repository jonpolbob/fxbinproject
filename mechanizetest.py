#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'cagibi'

import mechanicalsoup



URL = "http://www.histdata.com/download-free-forex-historical-data/?/ninjatrader/tick-bid-quotes/eurusd/2016/9/"

browser = mechanicalsoup.Browser()
login_page = browser.get(URL)

# we grab the login form
login_form = login_page.soup.find("a", {"id": "a_file"})

print(login_page.links)

print("-----------------")
print(login_page.soup())

#br.open("http://www.histdata.com/download-free-forex-historical-data/?/ninjatrader/tick-bid-quotes/eurusd/2016/9")
print (login_form)
