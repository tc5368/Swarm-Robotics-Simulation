import random

#List of grocery items sourced from: https://www.kaggle.com/heeraldedhia/groceries-dataset?select=Groceries_dataset.csv
#Confirm how to reference this. Items were deduplicated and placed in list.
grocery_items = ["tropical fruit","whole milk","pip fruit","other vegetables","rolls/buns","pot plants","citrus fruit","beef","frankfurter","chicken","butter","fruit/vegetable juice","packaged fruit/vegetables","chocolate","specialty bar","butter milk","bottled water","yogurt","sausage","brown bread","hamburger meat","root vegetables","pork","pastry","canned beer","berries","coffee","misc. beverages","ham","turkey","curd cheese","red/blush wine","frozen potato products","flour","sugar","frozen meals","herbs","soda","detergent","grapes","processed cheese","fish","sparkling wine","newspapers","curd","pasta","popcorn","finished products","beverages","bottled beer","dessert","dog food","specialty chocolate","condensed milk","cleaner","white wine","meat","ice cream","hard cheese","cream cheese ","liquor","pickled vegetables","liquor (appetizer)","UHT-milk","candy","onions","hair spray","photo/film","domestic eggs","margarine","shopping bags","salt","oil","whipped/sour cream","frozen vegetables","sliced cheese","dish cleaner","baking powder","specialty cheese","salty snack","Instant food products","pet care","white bread","female sanitary products","cling film/bags","soap","frozen chicken","house keeping products","spread cheese","decalcifier","frozen dessert","vinegar","nuts/prunes","potato products","frozen fish","hygiene articles","artif. sweetener","light bulbs","canned vegetables","chewing gum","canned fish","cookware","semi-finished bread","cat food","bathroom cleaner","prosecco","liver loaf","zwieback","canned fruit","frozen fruits","brandy","baby cosmetics","spices","napkins","waffles","sauces","rum","chocolate marshmallow","long life bakery product","bags","sweet spreads","soups","mustard","specialty fat","instant coffee","snack products","organic sausage","soft cheese","mayonnaise","dental care","roll products ","kitchen towels","flower soil/fertilizer","cereals","meat spreads","dishes","male cosmetics","candles","whisky","tidbits","cooking chocolate","seasonal products","liqueur","abrasive cleaner","syrup","ketchup","cream","skin care","rubbing alcohol","nut snack","cocoa drinks","softener","organic products","cake bar","honey","jam","kitchen utensil","flower (seeds)","rice","tea","salad dressing","specialty vegetables","pudding powder","ready soups","make up remover","toilet cleaner","preservation products"]

def allocate_items_to_grid(num_cells):
	if num_cells < len(grocery_items):
		grid = grocery_items[0:num_cells]
	else:
		grid = grocery_items + random.choices(grocery_items, k=num_cells-len(grocery_items))
	grid.sort()
	return grid

def generate_order(number_of_items=10,maxStockperItem=3,maxNum=10):
	if maxNum < len(grocery_items):
		items = random.choices(grocery_items[0:maxNum],k=number_of_items)
	else:
		items = random.choices(grocery_items,k=number_of_items)
	items.sort()
	order = {}
	for item in items:
		order.update({item:random.randint(1,maxStockperItem)})

	return(order)