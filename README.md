# post-office
P-uppgift #155. 

Lydelse
Det g aller att simulera k osituationer pa det lilla postombudet i Skruttem ̊ala. Postombudet
öppnar kl 9.00 och stänger kl 18.00. Kunder anländer i genomsnitt var femte minut, dvs
sannolikheten för att en ny kund ska komma under en viss minut  ̈ar 20%. För postexpediten,
fru Franco, tar det exakt två minuter att betjäna ett postärende. Hälften av alla kunder har
ett enda ärende, en fjärdedel har två ärenden, en åttondel tre ärenden osv.
Vid stängningsdags låser fru Franco dörren men betjänar plikttroget de kunder som står i
kö. Därefter för hon dagens kundstatistik (totala antalet kunder, alla kunders sammanlagda
väntetid och genomsnittliga väntetiden per kund). Allt detta ska simuleras av ditt program
enligt följande exempel:
  Kl 9.03 kommer kund 1 in och blir genast betjänad
  Kl 9.05 kommer kund 2 in och ställer sej i kön som nr 2
  Kl 9.07 går kund 1 och kund 2 blir betjänad
  Kl 9.09 kommer kund 3 in och ställer sej i kön som nr 2
  Kl 9.09 går kund 2 och kund 3 blir betjänad
  Kl 9.12 kommer kund 4 in och blir genast betjänad
  Kl 9.13 kommer kund 5 in och ställer sej i kön som nr 2
  Kl 9.15 kommer kund 6 in och ställer sej i kön som nr 3
  
Programmet använder sig av tkinter för den grafiska delen. Koden är skriven arkitekturmönstret
efter Model-View-Controller, som förkortas MVC. Nedan ser man klass-strukturen i form av ett
UML-diagram
![alt text](https://github.com/gustaf-linder-kth/post-office/blob/main/UML.svg?raw=true)

  
