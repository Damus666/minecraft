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
    tool_types["picaxe"]:   {0:"wood_picaxe",
                            1:"stone_picaxe",
                            2:"iron_picaxe",
                            3:"gold_picaxe",
                            4:"diamond_picaxe"},
    
    tool_types["axe"]:   {0:"wood_axe",
                            1:"stone_axe",
                            2:"iron_axe",
                            3:"gold_axe",
                            4:"diamond_axe"},
    
    tool_types["shovel"]:   {0:"wood_shovel",
                            1:"stone_shovel",
                            2:"iron_shovel",
                            3:"gold_shovel",
                            4:"diamond_shovel"},
    
    tool_types["sword"]:   {0:"wood_sword",
                            1:"stone_sword",
                            2:"iron_sword",
                            3:"gold_sword",
                            4:"diamond_sword"},
}

