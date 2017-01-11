#!/usr/bin/env python
# -*- coding: utf-8 -*-


import readweekpaire

#34 2015 = 17 aout
#36 2015 : aout sept

letableau = readweekpaire.readweek(34, 2015, 'AUDUSD')
tabcandle = readweekpaire.candelize(letableau)
print(tabcandle)

