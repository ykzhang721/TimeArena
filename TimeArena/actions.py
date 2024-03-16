
class MetaAction():
    def __init__(self, name = None, usage = None, occupy = None, description = None):
        self.properties = {}
        self.properties['name'] = name
        self.properties['usage'] = usage
        self.description = {
                            "pick": "Pick the unpicked item.",
                            "cook in": "Cook the raw item until it's cooked through.",
                            "chop": "Chop the whole item into sliced pieces.",
                            "fry in": "Fry the raw item until it is fried.",
                            "wash": "Wash the dirty item to make clean.",
                            "bake in": "Bake the raw item in the oven until it's roasted.",
                            "activate": "Activate the inactive device to turn it active.",
                            "pour into": "Pour the liquid in item into the empty container until it is full.",
                            "brew with": "Brew the dry item leaves with the container until they're steeped.",
                            "gather": "Gather the scattered items until it is collected.",
                            "scrape into": "Scrape the contents from the full item into th empty item.",
                            "place into": "Place the unplaced item into the right place.",
                            "fill with": "Fill the container with something.",
                            "hoe": "Hoe the uncultivated item until it is cultivated and ready for planting.",
                            "weed_with": "Weed with the item.",
                            "set_up": "Set up the item that is not set yet until it is already set.",
                            "iron": "Iron the wrinkled item until they are smooth.",
                            "put on": "Put the item on the right place.",
                            "add to": "Add one item to the container.",
                            "rinse": "Rinse the dry item.",
                            "find": "Find the missed item so that it is found and can be used.",
                            "heat": "Heat the cool item until it is hot.",
                            "dilute": "Dilute the concentrated item until it is diluted.",
                            "cut": "Cut the whole item into divided pieces.",
                            "dissolve in": "Dissolve the solid item in the liquid until it is dissolved.",
                            "polish": "Polish the rusty item until it is polished.",
                            "empty": "Empty the full item until it is empty.",
                            "hanging": "Hang the item",
                            "water by": "Water the item by something",
                            "trim": "Trim the overgrown item until it is trimmed",
                            "plant":"Plant the uncultivated item until it is planted",
                            "store": "Store the unstored item",
                            "stir with":"Stir the separate liquid in item with something until it is homogeneous",
                            "soak in": "Soak the dry item in something until it is wet",
                            "mop": "Mop the dirty item until it is clean",
                            "read": "Read the unknown item",
                            "fold": "Fold the spread item until it is tidy",
                            "crush": "Crush the intact item until it is crushed",
                            "cool": "Cool the hot item until it is cool",
                            "dry": "Dry the wet item until it is dry",
                            "wipe": "Wipe the dirty item until it is clean",
                            "put in": "Put the item in something",
                            "label": "Give the ambiguous item a label",
                            "crystallize": "Crystallize the fluid item until it is crystallized",
                            "filter": "Filter the mixed item until it is refined",
                            }
        if name: 
            self.properties['description'] = self.description[name]
        self.properties['occupy'] = occupy
        self.properties['state'] = {"pick":["unpicked", "picked"],
                                    "cook_in_1":["raw", "cooked"],
                                    "chop":["whole","sliced"],
                                    "fry_in_1":["raw","fried"],
                                    "wash": ["dirty", "clean"],
                                    "bake_in_1":["raw", "roasted"],
                                    "bake_in_2":["empty","full"],
                                    "activate":["inactive","done"],
                                    "pour_into_2":["empty","full"],
                                    "pour_into_1":["full","empty"],
                                    "brew_with_1":["dry","steeped"],
                                    "gather": ["scattered","collected"],
                                    "scrape_into_1":["full","empty"],
                                    "scrape_into_2":["empty","full"],
                                    "place_into_1":["unplaced","placed"],
                                    "place_into_2":["empty","full"],
                                    "wash_by_1":["dirty","clean"],
                                    "fill_with_1":["empty","full"],
                                    "fill_with_2":["not added","added"],
                                    "hoe":["uncultivated","cultivated"],
                                    "weed_with":["not used for weeding","used for weeding"],
                                    "set_up": ["not set yet","already set"],
                                    "iron":["wrinkled","smooth"],
                                    "put_on_1":['not put on right place','put on right place'],
                                    "add_to_1":["not added","added"],
                                    "add_to_2":["empty","full"],
                                    "rinse": ["dry","rinsed"],
                                    "find": ["missed","found"],
                                    "heat": ["cool","hot"],
                                    "dilute":["concentrated","diluted"],
                                    "cut":["whole","divided"],
                                    "dissolve_in_1":["solid","dissolved"],
                                    "polish": ["rusty","polished"],
                                    "crush": ['intact','crushed'],
                                    "cool": ["hot","cool"],
                                    "put_in_1": ["not put in right place","put in right place"],
                                    "crystallize": ["fluid","crystallized"],
                                    "filter": ["mixed","refined"],
                                    "cook_in_2": ["empty","full"],
                                    "fry_in_2": ["empty","full"],
                                    "water_by_1": ["dry","wet"],
                                    "plant": ["uncultivated","planted"],
                                    "mop": ["dirty","clean"],
                                    "fold": ["spread","tidy"],
                                    "wipe": ["dirty","clean"],
                                    "empty": ["full","empty"],
                                    "hanging": ["not hung","hung"],
                                    "trim": ["overgrown","trimmed"],
                                    "store": ["unstored","stored"],
                                    "read": ["unknown","known"],
                                    "stir_with_1": ["separate","homogeneous"],
                                    "soak_in_1": ["dry","wet"],
                                    "label":["ambiguous","identified"],
                                    "dry": ["wet","dry"],
                                    }
