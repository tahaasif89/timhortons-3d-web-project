"""Builds data/menu.json (the editable source of truth). Run: python data/build_menu.py
Prices come from public delivery-app listings of Tim Hortons Pakistan and may differ from in-store prices.
Ingredient lists are illustrative compositions used to explain each item in 3D (not official recipes)."""
import json
CATS=[('iced-capps','Iced Capps','Frozen blended coffee'),('iced-coffee','Iced Coffee','Cold espresso drinks'),('matcha','Matcha','Green tea drinks'),('hot','Hot Espresso','Coffee & lattes'),('sandwiches','Sandwiches & Panini','Grilled and toasted'),('donuts','Donuts & Timbits','Fresh baked')]
# ingredient catalogue: slug,name,kind(3D prop),color,info
ING={
'coffee':('Brewed coffee','coffee','#4a2a14','Freshly brewed medium-roast coffee.'),
'espresso':('Espresso shot','espresso','#2a140a','A concentrated shot pulled under pressure, topped with crema.'),
'milk':('Milk','milk','#f6efe2','Cold or steamed milk gives body and sweetness.'),
'cream':('Cream','milk','#fff6e0','Cream makes the drink richer and smoother.'),
'ice':('Ice','ice','#cfe8f5','Crushed ice keeps it cold and gives blended drinks their frosty texture.'),
'whip':('Whipped cream','whip','#fff8ee','Light whipped cream swirled on top.'),
'sugar':('Sugar','sugar','#ffffff','Sweetens the base.'),
'vanilla':('Vanilla syrup','syrup','#efd9a0','Sweet vanilla flavour.'),
'caramel':('Caramel sauce','syrup','#c4762a','Buttery caramel.'),
'hazelnut':('Hazelnut syrup','syrup','#8a5a30','Toasted hazelnut flavour.'),
'chocolate':('Chocolate sauce','syrup','#3b1d10','Rich chocolate.'),
'condensed':('Condensed milk','can','#f1e0b5','Sweet condensed milk, the base of a Spanish latte.'),
'oreo':('OREO pieces','oreo','#2b1b14','Crushed chocolate sandwich cookie.'),
'chips':('Chocolate chips','chips','#3b1d10','Chocolate chips for a java-chip crunch.'),
'strawberry':('Strawberry','strawberry','#d8283c','Strawberry puree and pieces.'),
'mango':('Mango','mango','#f6a81c','Sweet mango puree and cubes.'),
'pistachio':('Pistachio','pistachio','#9dbb62','Pistachio paste and crushed nuts.'),
'biscoff':('Lotus Biscoff','biscoff','#b9772e','Caramelised biscuit spread and crumbs.'),
'pineapple':('Pineapple','pineapple','#f3d03e','Tropical pineapple.'),
'orange':('Orange','orange','#f08a1d','Orange zest and juice.'),
'matcha':('Matcha','matcha','#7ca443','Finely milled green tea powder.'),
'hazelnuts':('Hazelnut pieces','hazelnut','#9a6b3c','Crunchy roasted hazelnuts.'),
'beans':('Coffee beans','beans','#3a1f10','Roasted arabica beans.'),
'bread':('Panini bread','bread','#d9a566','Soft bread, toasted with grill marks.'),
'chicken':('Grilled chicken','chicken','#e4c08e','Tender grilled chicken.'),
'tikka':('Chicken tikka','tikka','#d9531e','Spiced tikka-marinated chicken.'),
'cheese':('Cheese','cheese','#f5c443','Melted cheese slices.'),
'jalapeno':('Jalapeño','jalapeno','#4f8d2c','Pickled jalapeño rings.'),
'lettuce':('Lettuce','lettuce','#79b84a','Crisp lettuce.'),
'onion':('Onion','onion','#d9a8c8','Sliced onion.'),
'caesar':('Caesar dressing','sauce','#efe6cf','Creamy Caesar sauce.'),
'mayo':('Creamy sauce','sauce','#f3ecdd','Creamy spread.'),
'chutney':('Green chutney','sauce','#6fa83a','Fresh mint-coriander chutney.'),
'parmesan':('Parmesan','parmesan','#f2e2a8','Shaved parmesan.'),
'dough':('Donut dough','dough','#d9a15e','Yeast-raised dough, fried until golden.'),
'whitedip':('White chocolate dip','icing','#fff3dc','Smooth white chocolate coating.'),
'glaze':('Sugar glaze','icing','#f7e4b0','A thin sugar glaze.'),
'vandip':('Vanilla dip','icing','#f6e9c9','Vanilla fondant dip.'),
'chocdip':('Chocolate dip','icing','#4a2415','Chocolate fondant dip.'),
'mapledip':('Maple glaze','icing','#a8641e','Sweet maple glaze.'),
'sprinkles':('Sprinkles','sprinkles','#ff6b9a','Colourful sprinkles.'),
'smarties':('Smarties','smarties','#e53935','Colourful candy-coated chocolate.'),
'lotusbis':('Lotus biscuit','biscoff','#b9772e','Crumbled caramel biscuit.'),
'pistacrumb':('Crushed pistachio','pistachio','#9dbb62','Crushed pistachio topping.'),
'oreocrumb':('OREO crumb','oreo','#2b1b14','OREO cookie crumbs.'),
}
items=[]
def add(cat,slug,name,price,desc,builder,params,ings,badge=None):
    items.append(dict(cat=cat,slug=slug,name=name,price=price,desc=desc,builder=builder,params=params,ingredients=[dict(ing=i,role=r) for i,r in ings],badge=badge))
# ---- Iced Capps (blended frozen coffee) ----
def capp(slug,name,tint,top,drz,flav,desc,price=990,extra=None,badge=None):
    ings=[('coffee','layer0'),('milk','layer0b'),('ice','ice')]+(extra or [])+[('whip','whip')]
    add('iced-capps',slug,name,price,desc,'cold',dict(kind='capp',layers=[[tint,1.0]],ice=True,whip=True,drizzle=drz,topping=top),ings,badge)
capp('original-iced-capp','Original Iced Capp','#d8b98e',None,None,None,'The classic frozen blended coffee topped with whipped cream.',extra=[('sugar','layer0c')],badge='Classic')
capp('hazelnut-iced-capp','Hazelnut Iced Capp','#c9956a',dict(k='nut',c='#9a6b3c'),'#3b1d10',None,'Iced capp blended with hazelnut syrup and topped with whipped cream and hazelnut pieces.',extra=[('hazelnut','layer0c'),('hazelnuts','topping')],badge='Popular')
capp('oreo-iced-capp','OREO Iced Capp','#b79880',dict(k='crumb',c='#2b1b14'),'#3b1d10',None,'Smooth and creamy iced capp with OREO cookie pieces.',extra=[('oreo','layer0c'),('chocolate','drizzle')])
capp('caramel-iced-capp','Caramel Iced Capp','#d4a26a',None,'#c4762a',None,'Iced capp with buttery caramel and a caramel drizzle.',extra=[('caramel','layer0c'),('caramel','drizzle')],badge='Popular')
capp('java-chip-iced-capp','Java Chip Iced Capp','#9a6a4a',dict(k='chip',c='#3b1d10'),'#3b1d10',None,'Chocolatey iced capp loaded with chocolate chips.',extra=[('chocolate','layer0c'),('chips','topping')],badge='Popular')
capp('strawberry-iced-capp','Strawberry Iced Capp','#e58a98',dict(k='cube',c='#d8283c'),None,None,'Fruity iced capp blended with strawberry.',extra=[('strawberry','layer0c')])
capp('pistachio-iced-capp','Pistachio Iced Capp','#b6c98b',dict(k='nut',c='#9dbb62'),None,None,'Nutty pistachio iced capp with crushed pistachio.',extra=[('pistachio','layer0c'),('pistacrumb','topping')])
capp('tropical-iced-capp','Tropical Iced Capp','#f0c25a',dict(k='cube',c='#f3d03e'),None,None,'Sunny tropical iced capp with pineapple and mango notes.',extra=[('pineapple','layer0c'),('mango','topping')])
capp('mango-iced-capp','Mango Iced Capp','#f3b24a',dict(k='cube',c='#f6a81c'),None,None,'Sweet mango iced capp.',extra=[('mango','layer0c')])
capp('lotus-biscoff-iced-capp','Lotus Biscoff Iced Capp','#c9915a',dict(k='crumb',c='#b9772e'),'#c4762a',None,'Iced capp with caramelised Lotus Biscoff.',extra=[('biscoff','layer0c'),('lotusbis','topping'),('caramel','drizzle')])
capp('strawberry-oreo-iced-capp','Strawberry OREO Iced Capp','#d9918e',dict(k='crumb',c='#2b1b14'),'#d8283c',None,'Strawberry and OREO together in a frozen capp.',extra=[('strawberry','layer0c'),('oreo','topping')])
capp('matcha-iced-capp','Matcha Iced Capp','#a9c47e',None,None,None,'Frozen matcha capp topped with whipped cream.',price=1090,extra=[('matcha','layer0c')])
# ---- Iced coffee ----
def iced(slug,name,price,layers,ings,desc,drz=None,whip=False,badge=None,cat='iced-coffee'):
    add(cat,slug,name,price,desc,'cold',dict(kind='iced',layers=layers,ice=True,whip=whip,drizzle=drz,topping=None),ings,badge)
iced('iced-french-vanilla','Iced French Vanilla',900,[['#efd9a0',.18],['#f6efe2',.42],['#6b3f1d',.40]],[('vanilla','layer0'),('milk','layer1'),('espresso','layer2'),('ice','ice')],'Smooth vanilla coffee over ice.',badge='Popular')
iced('iced-americano','Iced Americano',775,[['#7a5033',1.0]],[('espresso','layer0'),('ice','ice')],'Espresso poured over ice and cold water.')
iced('iced-latte','Iced Latte',825,[['#f6efe2',.62],['#3d2212',.38]],[('milk','layer0'),('espresso','layer1'),('ice','ice')],'Espresso over cold milk and ice.')
iced('caramel-iced-macchiato','Caramel Iced Macchiato',900,[['#c4762a',.12],['#f6efe2',.5],['#3d2212',.38]],[('caramel','layer0'),('milk','layer1'),('espresso','layer2'),('ice','ice'),('caramel','drizzle')],'Layers of milk, espresso and caramel finished with a caramel drizzle.',drz='#c4762a')
iced('mocha-iced-latte','Mocha Iced Latte',900,[['#3b1d10',.2],['#f6efe2',.42],['#3d2212',.38]],[('chocolate','layer0'),('milk','layer1'),('espresso','layer2'),('ice','ice'),('whip','whip')],'Espresso, chocolate and milk over ice with whipped cream.',drz='#3b1d10',whip=True)
iced('spanish-iced-latte','Spanish Iced Latte',900,[['#f1e0b5',.2],['#f6efe2',.42],['#3d2212',.38]],[('condensed','layer0'),('milk','layer1'),('espresso','layer2'),('ice','ice')],'A sweet iced latte made with condensed milk.',badge='Popular')
iced('jaffa-iced-mocha','Jaffa Iced Mocha',None,[['#f08a1d',.18],['#3b1d10',.22],['#f6efe2',.3],['#3d2212',.3]],[('orange','layer0'),('chocolate','layer1'),('milk','layer2'),('espresso','layer3'),('ice','ice'),('whip','whip')],'Chocolate and orange iced mocha.',whip=True)
iced('frozen-french-vanilla','Frozen French Vanilla',990,[['#ecd9ac',1.0]],[('vanilla','layer0'),('milk','layer0b'),('ice','ice'),('whip','whip')],'Frozen blended vanilla coffee with whipped cream.',whip=True)
# ---- Matcha ----
def matcha(slug,name,price,bottom,bc,ings,desc,hot=False):
    add('matcha',slug,name,price,desc,'cold',dict(kind='iced',layers=[[bc,.2],['#f6efe2',.42],['#7ca443',.38]],ice=True,whip=False,drizzle=None,topping=None),ings)
matcha('iced-vanilla-bean-matcha-latte','Iced Vanilla Bean Matcha Latte',None,'vanilla','#efd9a0',[('vanilla','layer0'),('milk','layer1'),('matcha','layer2'),('ice','ice')],'Matcha latte with vanilla bean over ice.')
matcha('iced-strawberry-matcha','Iced Strawberry Matcha',None,'strawberry','#d8283c',[('strawberry','layer0'),('milk','layer1'),('matcha','layer2'),('ice','ice')],'Strawberry puree under milk and matcha.')
matcha('iced-mango-matcha','Iced Mango Matcha',None,'mango','#f6a81c',[('mango','layer0'),('milk','layer1'),('matcha','layer2'),('ice','ice')],'Mango puree under milk and matcha.')
add('matcha','hot-matcha-latte','Hot Matcha Latte',None,'Warm matcha whisked with steamed milk.','hot',dict(kind='latte',liquids=[['#7ca443',.45],['#f6efe2',.55]],foam='#eef3dc',syrup=None),[('matcha','layer0'),('milk','layer1')])
# ---- Hot espresso ----
def hot(slug,name,price,liq,foam,syr,ings,desc,badge=None):
    add('hot',slug,name,price,desc,'hot',dict(kind='latte',liquids=liq,foam=foam,syrup=syr),ings,badge)
hot('cappuccino','Cappuccino',675,[['#3d2212',.3],['#f6efe2',.7]],'#fbf3e4',None,[('espresso','layer0'),('milk','layer1')],'Espresso with steamed milk and a thick layer of foam.')
hot('latte','Latte',675,[['#3d2212',.28],['#f6efe2',.72]],'#fbf3e4',None,[('espresso','layer0'),('milk','layer1')],'Espresso with plenty of steamed milk and light foam.')
hot('mocha-latte','Mocha Latte',850,[['#3b1d10',.3],['#3d2212',.2],['#f6efe2',.5]],'#fbf3e4','#3b1d10',[('chocolate','layer0'),('espresso','layer1'),('milk','layer2')],'Rich and velvety coffee with chocolate and a silky microfoam.')
hot('caramel-macchiato','Caramel Macchiato',750,[['#f6efe2',.7],['#3d2212',.3]],'#fbf3e4','#c4762a',[('milk','layer0'),('espresso','layer1'),('caramel','syrup')],'Steamed milk marked with espresso and caramel.')
hot('caramel-latte','Caramel Latte',750,[['#c4762a',.15],['#3d2212',.25],['#f6efe2',.6]],'#fbf3e4','#c4762a',[('caramel','layer0'),('espresso','layer1'),('milk','layer2')],'Latte sweetened with caramel.')
hot('hazelnut-latte','Hazelnut Latte',750,[['#8a5a30',.15],['#3d2212',.25],['#f6efe2',.6]],'#fbf3e4',None,[('hazelnut','layer0'),('espresso','layer1'),('milk','layer2')],'Latte with toasted hazelnut flavour.')
hot('spanish-latte','Spanish Latte',750,[['#f1e0b5',.2],['#3d2212',.25],['#f6efe2',.55]],'#fbf3e4',None,[('condensed','layer0'),('espresso','layer1'),('milk','layer2')],'Hot latte sweetened with condensed milk.')
hot('flat-white','Flat White',850,[['#3d2212',.4],['#f6efe2',.6]],'#fbf3e4',None,[('espresso','layer0'),('milk','layer1')],'Rich and velvety coffee with a silky microfoam.')
hot('french-vanilla-hot','French Vanilla (Hot)',750,[['#efd9a0',.15],['#6b3f1d',.4],['#f6efe2',.45]],'#fbf3e4',None,[('vanilla','layer0'),('coffee','layer1'),('milk','layer2')],'Classic hot French vanilla cappuccino.',badge='Popular')
# ---- Sandwiches ----
def sand(slug,name,layers,ings,desc,badge='Popular'):
    add('sandwiches',slug,name,1090,desc,'sandwich',dict(layers=layers),ings,badge)
sand('grilled-chicken-jalapeno','Grilled Chicken Jalapeño',['sauce:#f3ecdd','chicken','jalapeno','cheese','lettuce'],[('bread','bread'),('mayo','f0'),('chicken','f1'),('jalapeno','f2'),('cheese','f3'),('lettuce','f4')],'Grilled chicken with jalapeño, cheese and creamy sauce on toasted bread.',None)
sand('grilled-cheese','Grilled Cheese',['cheese','cheese','cheese'],[('bread','bread'),('cheese','f0'),('cheese','f1'),('cheese','f2')],'Melted layers of cheese on grilled bread.',None)
sand('grilled-cheese-tikka','Grilled Cheese Tikka',['sauce:#6fa83a','tikka','onion','cheese'],[('bread','bread'),('chutney','f0'),('tikka','f1'),('onion','f2'),('cheese','f3')],'Chicken tikka, onion and melted cheese with green chutney.')
sand('chicken-caesar-panini','Chicken Caesar Panini',['sauce:#efe6cf','chicken','lettuce','parmesan'],[('bread','bread'),('caesar','f0'),('chicken','f1'),('lettuce','f2'),('parmesan','f3')],'Grilled chicken, lettuce, parmesan and Caesar dressing in a panini.',None)
# ---- Donuts ----
def donut(slug,name,price,icing,top,ings,desc,badge=None):
    add('donuts',slug,name,price,desc,'donut',dict(icing=icing,topping=top),ings,badge)
donut('white-chocolate-dip','Classic White Chocolate Dip',350,'#fff3dc',None,[('dough','dough'),('whitedip','icing')],'Classic ring donut dipped in white chocolate.')
donut('original-glazed','Original Glazed',None,'#f7e4b0',None,[('dough','dough'),('glaze','icing')],'Soft ring donut with a sugar glaze.')
donut('vanilla-dip','Vanilla Dip',None,'#f6e9c9',dict(k='sprinkles'),[('dough','dough'),('vandip','icing'),('sprinkles','topping')],'Ring donut dipped in vanilla with sprinkles.')
donut('chocolate-dip','Chocolate Dip',None,'#4a2415',None,[('dough','dough'),('chocdip','icing')],'Ring donut dipped in chocolate.')
donut('oreo-dream-donut','Premium OREO Dream Donut',450,'#3a2a22',dict(k='crumb',c='#2b1b14'),[('dough','dough'),('whitedip','icing'),('oreocrumb','topping')],'Premium donut with creamy icing and OREO crumbs.')
donut('lotus-melt','Premium Lotus Melt',450,'#b9772e',dict(k='crumb',c='#c98a3c'),[('dough','dough'),('biscoff','icing'),('lotusbis','topping')],'Premium donut with Lotus Biscoff spread and crumbs.')
donut('pistachio-donut','Premium Pistachio',None,'#b6c98b',dict(k='crumb',c='#7fa13e'),[('dough','dough'),('pistachio','icing'),('pistacrumb','topping')],'Premium donut with pistachio icing and crushed nuts.')
donut('smarties-donut','Premium Smarties',None,'#fff3dc',dict(k='smarties'),[('dough','dough'),('whitedip','icing'),('smarties','topping')],'Premium donut with white icing and colourful Smarties.')
donut('maple-donut','Premium Maple',None,'#a8641e',None,[('dough','dough'),('mapledip','icing')],'Premium donut with sweet maple glaze.')
add('donuts','timbits-box','Timbits (box of 10)',810,'Bite-sized donut holes in assorted flavours.','timbits',dict(count=10,colors=['#fff3dc','#4a2415','#f7e4b0','#f6e9c9','#b6c98b']),[('dough','dough'),('glaze','icing'),('sprinkles','topping')],'Popular')
cats=[dict(slug=s,name=n,blurb=b) for s,n,b in CATS]
ings=[dict(slug=k,name=v[0],kind=v[1],color=v[2],info=v[3]) for k,v in ING.items()]
json.dump(dict(categories=cats,ingredients=ings,items=items),open('data/menu.json','w'),indent=1,ensure_ascii=False)
print(len(items),'items',len(ings),'ingredients')
