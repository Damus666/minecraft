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
}

blocks_data = {
    block_ids["dirt"]:          {"name":"dirt_block",
                                "tool_required":tool_types["shovel"],
                                "mine_cooldown":0.72*1000},

    block_ids["grassblock"]:    {"name":"grass_block",
                                "tool_required":tool_types["shovel"],
                                "mine_cooldown":0.72*1000},

    block_ids["stone"]:         {"name":"stone_block",
                                "tool_required":tool_types["picaxe"],
                                "mine_cooldown":1.2*1000},
    
    block_ids["grimstone"]:     {"name":"grimstone_block",
                                "tool_required":tool_types["picaxe"],
                                "mine_cooldown":1.82*1000},

    block_ids["bedrock"]:       {"name":"bedrock",
                                "tool_required":tool_types["thepowerofgod"],
                                "mine_cooldown":999*1000},

    block_ids["log"]:           {"name":"log_block",
                                "tool_required":tool_types["axe"],
                                "mine_cooldown":1.1*1000},

    block_ids["leaves"]:        {"name":"leaves_block",
                                "tool_required":tool_types["axe"],
                                "mine_cooldown":0.4*1000},
}

frames = {
    block_ids["grass"]: 3,
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
                "speed":3,
                "health":10,
                "chances":5}
}

items_ids = {
    "meat":0,
    "cookedmeat":1,
}

items_data = {
    items_ids["meat"]: {"name":"raw_meat",
                        "type":"food",
                        "hunger":2,},

    items_ids["cookedmeat"]: {"name":"cooked_meat",
                             "type":"food",
                             "hunger":6,},
}

