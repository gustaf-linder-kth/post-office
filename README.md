# Uppgift
P-uppgift #115. 
> Det gäller att simulera kösituationer på det lilla postombudet i Skruttemåla. Postombudet
> öppnar kl 9.00 och stänger kl 18.00. Kunder anländer i genomsnitt var femte minut, dvs
> sannolikheten för att en ny kund ska komma under en viss minut  ̈ar 20%. För postexpediten,
> fru Franco, tar det exakt två minuter att betjäna ett postärende. Hälften av alla kunder har
> ett enda ärende, en fjärdedel har två ärenden, en åttondel tre ärenden osv.
> Vid stängningsdags låser fru Franco dörren men betjänar plikttroget de kunder som står i
> kö. Därefter för hon dagens kundstatistik (totala antalet kunder, alla kunders sammanlagda
> väntetid och genomsnittliga väntetiden per kund).

# Programstruktur
Programmet använder sig av tkinter för den grafiska delen. Koden är skriven arkitekturmönstret
efter Model-View-Controller, som förkortas MVC. Nedan ser man klass-strukturen i form av ett
UML-diagram (ses inte om du har på dark mode på github pga .svg-filen är genomskinlig).
![UML Diagram](https://github.com/gustaf-linder-kth/post-office/blob/main/UML.svg?raw=true)
MVC bygger på att logik och UI separeras och all interaktion mellan dem sker via klassen
Controller.

# Användargränsnitt
![GUI](https://github.com/gustaf-linder-kth/post-office/blob/main/gui.PNG?raw=true)
Programmet består av två stycken "ScrolledText" som utmatar text. Den stora uppe till vänster är 
för den huvudsakliga utmatningen, medan den undre till höger är för några intressant nyckelvärden.
Nere till vänster visas en tabell över den nuvarande kön. Widgeten är "Treeview".

![GUI](https://github.com/gustaf-linder-kth/post-office/blob/main/chart.PNG?raw=true)
Till höger finns alla parametrar som simulationen beror på. När arbetsdagen är slut och alla
kunder har lämnat butiken skapas ett nytt fönster med ett matplotlib-linjediagram som visar
kölängd över tid.

# Tillägg
För att köra programmet ska man starta programmet i Controller.py. Min VS-code har lagt till
onödiga moduler så om python kräver att man installerar några paket så kan man i många fall 
bara ta bort import-raden. 
