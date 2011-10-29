#-*- coding: utf-8 -*-

def fake_urllib2(*args, **extra):
    class dummy:
        def read(self):
            return '''<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>  
<transaction>  
    <date>2011-02-10T16:13:41.000-03:00</date>  
    <code>9E884542-81B3-4419-9A75-BCC6FB495EF1</code>  
    <reference>REF1234</reference>  
    <type>1</type>  
    <status>3</status>  
    <paymentMethod>  
        <type>1</type>  
        <code>101</code>  
    </paymentMethod>  
    <grossAmount>49900.00</grossAmount>  
    <discountAmount>0.00</discountAmount>  
    <feeAmount>0.00</feeAmount>  
    <netAmount>49900.00</netAmount>  
    <extraAmount>0.00</extraAmount>  
    <installmentCount>1</installmentCount>  
    <itemCount>2</itemCount>  
    <items>  
        <item>  
            <id>0001</id>  
            <description>Notebook Prata</description>  
            <quantity>1</quantity>  
            <amount>24300.00</amount>  
        </item>  
        <item>  
            <id>0002</id>  
            <description>Notebook Rosa</description>  
            <quantity>1</quantity>  
            <amount>25600.00</amount>  
        </item>  
    </items>  
    <sender>  
        <name>Comprador</name>  
        <email>comprador@uol.com.br</email>  
        <phone>  
            <areaCode>11</areaCode>  
            <number>56273440</number>  
        </phone>  
    </sender>  
    <shipping>  
        <address>  
            <street>Av. Brig. Faria Lima</street>  
            <number>1384</number>  
            <complement>5o andar</complement>  
            <district>Jardim Paulistano</district>  
            <postalCode>01452002</postalCode>  
            <city>Sao Paulo</city>  
            <state>SP</state>  
            <country>BRA</country>  
        </address>  
        <type>1</type>  
        <cost>21.50</cost>  
    </shipping>  
</transaction>  '''
    return dummy()
