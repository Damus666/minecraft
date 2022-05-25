from utility.pixel_calculator import medium_calculator

tool_types = {
    "picaxe":0,
    "axe":1,
    "shovel":2,
    "sword":3,
    "thepowerofgod":4,
}

block_ids = {
    "dirt":0,
    "grassblock":1,
    "stone":2,
    "grimstone":3,
    "bedrock":4,
    "grass":5,
    "log":6,
    "leaves":7,
    "crafting":8,
    "planks":9,
    "red_bricks":10,
    "grey_bricks":11,
    "library":12,
    "furnace":13,
    "coal_ore":14,
    "iron_ore":15,
    "gold_ore":16,
    "diamond_ore":17,
    "coal_block":18,
    "iron_block":19,
    "gold_block":20,
    "diamond_block":21,
    "chest":22,
}

ores_data = {
    block_ids["coal_ore"]: {
        "range":[20,40],
        "chances":45,
    },

    block_ids["iron_ore"]: {
        "range":[36,50],
        "chances":25,
    },

    block_ids["gold_ore"]: {
        "range":[40,52],
        "chances":10,
    },

    block_ids["diamond_ore"]: {
        "range":[52,62],
        "chances":5,
    },
}

items_ids = {
    "meat":0,
    "cookedmeat":1,
    "bone":2,
    "brown_fungus":3,
    "white_fungus":4,
    "stick":5,
    "coal":6,
    "raw_iron":7,
    "raw_gold":8,
    "diamond":9,
    "iron_ingot":10,
    "gold_ingot":11
}

items_data = {
    items_ids["meat"]: {"name":"raw_meat",
                        "type":["food","smeltable"],
                        "hunger":2,
                        "result":items_ids["cookedmeat"],
                        "smelt_cooldown":3.5*1000,},

    items_ids["cookedmeat"]: {"name":"cooked_meat",
                             "type":["food"],
                             "hunger":6,},
    
    items_ids["brown_fungus"]: {"name":"brown_mushroom",
                             "type":["food"],
                             "hunger":1,},

    items_ids["white_fungus"]: {"name":"white_mushroom",
                             "type":["food"],
                             "hunger":1,},

    items_ids["bone"]: {"name":"bone",
                             "type":["misc"],
                             },

    items_ids["stick"]: {"name":"stick",
                             "type":["misc"],
                             },
    
    items_ids["coal"]: {"name":"coal",
                             "type":["fuel"],
                             "fuel_points":8,
                             },

    items_ids["raw_iron"]: {"name":"raw_iron",
                             "type":["ore","smeltable"],
                             "fuel":2,
                             "result":items_ids["iron_ingot"],
                             "smelt_cooldown":6*1000,
                             },

    items_ids["raw_gold"]: {"name":"raw_gold",
                             "type":["ore","smeltable"],
                             "fuel":3,
                             "result":items_ids["gold_ingot"],
                             "smelt_cooldown":8*1000,
                             },

    items_ids["diamond"]: {"name":"diamond",
                             "type":["misc"],
                             },

    items_ids["iron_ingot"]: {"name":"iron_ingot",
                             "type":["misc"],
                             },

    items_ids["gold_ingot"]: {"name":"gold_ingot",
                             "type":["misc"],
                             },
}

blocks_data = {
    block_ids["dirt"]:          {"name":"dirt_block",
                                "tool_required":tool_types["shovel"],
                                "mine_cooldown":0.72*1000,
                                "max_cooldown":1.5,
                                "drop":{"id":block_ids["dirt"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["grassblock"]:    {"name":"grass_block",
                                "tool_required":tool_types["shovel"],
                                "mine_cooldown":0.72*1000,
                                "max_cooldown":1.5,
                                "drop":{"id":block_ids["grassblock"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["stone"]:         {"name":"stone_block",
                                "tool_required":tool_types["picaxe"],
                                "mine_cooldown":1.2*1000,
                                "max_cooldown":8,
                                "drop":{"id":block_ids["stone"],"type":"blocks"},
                                "ignore_tool":True,},
    
    block_ids["grimstone"]:     {"name":"grimstone_block",
                                "tool_required":tool_types["picaxe"],
                                "mine_cooldown":1.82*1000,
                                "max_cooldown":8,
                                "drop":{"id":block_ids["grimstone"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["bedrock"]:       {"name":"bedrock",
                                "tool_required":tool_types["thepowerofgod"],
                                "mine_cooldown":999*1000,
                                "max_cooldown":999,
                                "drop":{"id":block_ids["bedrock"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["log"]:           {"name":"log_block",
                                "tool_required":tool_types["axe"],
                                "mine_cooldown":1.05*1000,
                                "max_cooldown":1.5,
                                "drop":{"id":block_ids["log"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["leaves"]:        {"name":"leaves_block",
                                "tool_required":tool_types["axe"],
                                "mine_cooldown":0.4*1000,
                                "max_cooldown":1,
                                "drop":{"id":block_ids["leaves"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["crafting"]:        {"name":"crafting_table",
                                "tool_required":tool_types["axe"],
                                "mine_cooldown":1.0*1000,
                                "max_cooldown":1.5,
                                "drop":{"id":block_ids["crafting"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["chest"]:        {"name":"chest",
                                "tool_required":tool_types["axe"],
                                "mine_cooldown":1.1*1000,
                                "max_cooldown":1.5,
                                "drop":{"id":block_ids["chest"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["planks"]:        {"name":"wood_planks",
                                "tool_required":tool_types["axe"],
                                "mine_cooldown":0.85*1000,
                                "max_cooldown":1.5,
                                "drop":{"id":block_ids["planks"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["red_bricks"]:        {"name":"red_bricks",
                                "tool_required":tool_types["picaxe"],
                                "mine_cooldown":1.2*1000,
                                "max_cooldown":8,
                                "drop":{"id":block_ids["red_bricks"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["grey_bricks"]:        {"name":"dark_bricks",
                                "tool_required":tool_types["picaxe"],
                                "mine_cooldown":1.5*1000,
                                "max_cooldown":8,
                                "drop":{"id":block_ids["grey_bricks"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["library"]:        {"name":"bookshelf",
                                "tool_required":tool_types["axe"],
                                "mine_cooldown":1.0*1000,
                                "max_cooldown":1.5,
                                "drop":{"id":block_ids["library"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["furnace"]:        {"name":"furnace",
                                "tool_required":tool_types["picaxe"],
                                "mine_cooldown":1.3*1000,
                                "max_cooldown":8,
                                "drop":{"id":block_ids["furnace"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["coal_ore"]:        {"name":"coal_ore",
                                "tool_required":tool_types["picaxe"],
                                "level_required":0,
                                "mine_cooldown":1.2*1000,
                                "max_cooldown":8,
                                "drop":{"id":items_ids["coal"],"type":"items"},
                                "ignore_tool":False,},

    block_ids["iron_ore"]:        {"name":"iron_ore",
                                "tool_required":tool_types["picaxe"],
                                "level_required":1,
                                "mine_cooldown":1.3*1000,
                                "max_cooldown":8,
                                "drop":{"id":items_ids["raw_iron"],"type":"items"},
                                "ignore_tool":False,},

    block_ids["gold_ore"]:        {"name":"gold_ore",
                                "tool_required":tool_types["picaxe"],
                                "level_required":2,
                                "mine_cooldown":1.4*1000,
                                "max_cooldown":8,
                                "drop":{"id":items_ids["raw_gold"],"type":"items"},
                                "ignore_tool":False,},

    block_ids["diamond_ore"]:        {"name":"diamond_ore",
                                "tool_required":tool_types["picaxe"],
                                "level_required":2,
                                "mine_cooldown":1.5*1000,
                                "max_cooldown":8,
                                "drop":{"id":items_ids["diamond"],"type":"items"},
                                "ignore_tool":False,},

    block_ids["coal_block"]:        {"name":"coal_block",
                                "tool_required":tool_types["picaxe"],
                                "mine_cooldown":1.2*1000,
                                "max_cooldown":8,
                                "drop":{"id":block_ids["coal_block"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["iron_block"]:        {"name":"iron_block",
                                "tool_required":tool_types["picaxe"],
                                "mine_cooldown":1.3*1000,
                                "max_cooldown":8,
                                "drop":{"id":block_ids["iron_block"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["gold_block"]:        {"name":"gold_block",
                                "tool_required":tool_types["picaxe"],
                                "mine_cooldown":1.4*1000,
                                "max_cooldown":8,
                                "drop":{"id":block_ids["gold_block"],"type":"blocks"},
                                "ignore_tool":True,},

    block_ids["diamond_block"]:        {"name":"diamond_block",
                                "tool_required":tool_types["picaxe"],
                                "mine_cooldown":1.5*1000,
                                "max_cooldown":8,
                                "drop":{"id":block_ids["diamond_block"],"type":"blocks"},
                                "ignore_tool":True,},}

frames = {
    block_ids["grass"]: 4,
    block_ids["furnace"]:2,
    block_ids["coal_ore"]:2,
    block_ids["iron_ore"]:2,
    block_ids["gold_ore"]:2,
    block_ids["diamond_ore"]:2,
}

tools_data = {
    tool_types["picaxe"]:   {0:{"name":"wood_picaxe","damage":1,"durability":50},
                            1:{"name":"stone_picaxe","damage":2,"durability":160},
                            2:{"name":"iron_picaxe","damage":2,"durability":430},
                            3:{"name":"gold_picaxe","damage":3,"durability":710},
                            4:{"name":"diamond_picaxe","damage":4,"durability":1520}},
    
    tool_types["axe"]:   {0:{"name":"wood_axe","damage":2,"durability":50},
                            1:{"name":"stone_axe","damage":3,"durability":160},
                            2:{"name":"iron_axe","damage":4,"durability":430},
                            3:{"name":"gold_axe","damage":5,"durability":710},
                            4:{"name":"diamond_axe","damage":6,"durability":1520}},
    
    tool_types["shovel"]:   {0:{"name":"wood_shovel","damage":1,"durability":50},
                            1:{"name":"stone_shovel","damage":1,"durability":160},
                            2:{"name":"iron_shovel","damage":2,"durability":430},
                            3:{"name":"gold_shovel","damage":2,"durability":710},
                            4:{"name":"diamond_shovel","damage":3,"durability":1520}},
    
    tool_types["sword"]:   {0:{"name":"wood_sword","damage":3,"durability":50},
                            1:{"name":"stone_sword","damage":4,"durability":160},
                            2:{"name":"iron_sword","damage":5,"durability":430},
                            3:{"name":"gold_sword","damage":6,"durability":710},
                            4:{"name":"diamond_sword","damage":8,"durability":1520}},
}

entities_data = {
    "porcupine":{"name":"porcupine",
                "type":"animal",
                "speed":medium_calculator(3),
                "health":10,
                "chances":5},

    "zombie":{"name":"zombie",
                "type":"monster",
                "speed":medium_calculator(3),
                "health":20,
                "chances":5,
                "target_range":20,
                "attack_range":1,
                "attack_damage":1,
                "attack_cooldown":2*1000},

    "skeleton":{"name":"skeleton",
                "type":"monster",
                "speed":medium_calculator(4),
                "health":20,
                "chances":3,
                "target_range":30,
                "attack_range":2,
                "attack_damage":2,
                "attack_cooldown":4*1000},
}



