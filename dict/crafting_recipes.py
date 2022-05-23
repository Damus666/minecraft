from dict.data import block_ids,tool_types, items_ids

recipes = {
    "blocks":{
        block_ids["planks"]: {
            "amount":4,
            "recipe":[
                {"item":{"id":block_ids["log"],"type":"blocks"},"quantity":1},
            ]
        },
        block_ids["crafting"]: {
            "amount":1,
            "recipe":[
                {"item":{"id":block_ids["planks"],"type":"blocks"},"quantity":4},
            ]
        },
        block_ids["library"]: {
            "amount":1,
            "recipe":[
                {"item":{"id":block_ids["log"],"type":"blocks"},"quantity":1},
                {"item":{"id":block_ids["planks"],"type":"blocks"},"quantity":3},
            ]
        },
        block_ids["red_bricks"]: {
            "amount":1,
            "recipe":[
                {"item":{"id":block_ids["stone"],"type":"blocks"},"quantity":1},
            ]
        },
        block_ids["grey_bricks"]: {
            "amount":2,
            "recipe":[
                {"item":{"id":block_ids["stone"],"type":"blocks"},"quantity":1},
                {"item":{"id":block_ids["grimstone"],"type":"blocks"},"quantity":1},
            ]
        },
        block_ids["furnace"]: {
            "amount":1,
            "recipe":[
                {"item":{"id":block_ids["stone"],"type":"blocks"},"quantity":8},
            ]
        },

        block_ids["coal_block"]: {
            "amount":1,
            "recipe":[
                {"item":{"id":items_ids["coal"],"type":"items"},"quantity":9},
            ]
        },

        block_ids["iron_block"]: {
            "amount":1,
            "recipe":[
                {"item":{"id":items_ids["iron_ingot"],"type":"items"},"quantity":9},
            ]
        },

        block_ids["gold_block"]: {
            "amount":1,
            "recipe":[
                {"item":{"id":items_ids["gold_ingot"],"type":"items"},"quantity":9},
            ]
        },

        block_ids["diamond_block"]: {
            "amount":1,
            "recipe":[
                {"item":{"id":items_ids["diamond"],"type":"items"},"quantity":9},
            ]
        },
    },

    "tools":{ # amount always 1
        tool_types["picaxe"]: {
            0: [
                {"item":{"id":block_ids["planks"],"type":"blocks"},"quantity":3},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":2},
            ],
            1: [
                {"item":{"id":block_ids["stone"],"type":"blocks"},"quantity":3},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":2},
            ],
            2: [
                {"item":{"id":items_ids["iron_ingot"],"type":"items"},"quantity":3},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":2},
            ],
            3: [
                {"item":{"id":items_ids["gold_ingot"],"type":"items"},"quantity":3},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":2},
            ],
            4: [
                {"item":{"id":items_ids["diamond"],"type":"items"},"quantity":3},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":2},
            ],
        },
        tool_types["axe"]: {
            0: [
                {"item":{"id":block_ids["planks"],"type":"blocks"},"quantity":3},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":2},
            ],
            1: [
                {"item":{"id":block_ids["stone"],"type":"blocks"},"quantity":3},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":2},
            ],
            2: [
                {"item":{"id":items_ids["iron_ingot"],"type":"items"},"quantity":3},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":2},
            ],
            3: [
                {"item":{"id":items_ids["gold_ingot"],"type":"items"},"quantity":3},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":2},
            ],
            4: [
                {"item":{"id":items_ids["diamond"],"type":"items"},"quantity":3},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":2},
            ],
        },
        tool_types["shovel"]: {
            0: [
                {"item":{"id":block_ids["planks"],"type":"blocks"},"quantity":1},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":2},
            ],
            1: [
                {"item":{"id":block_ids["stone"],"type":"blocks"},"quantity":1},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":2},
            ],
            2: [
                {"item":{"id":items_ids["iron_ingot"],"type":"items"},"quantity":1},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":2},
            ],
            3: [
                {"item":{"id":items_ids["gold_ingot"],"type":"items"},"quantity":1},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":2},
            ],
            4: [
                {"item":{"id":items_ids["diamond"],"type":"items"},"quantity":1},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":2},
            ],
        },
        tool_types["sword"]: {
            0: [
                {"item":{"id":block_ids["planks"],"type":"blocks"},"quantity":2},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":1},
            ],
            1: [
                {"item":{"id":block_ids["stone"],"type":"blocks"},"quantity":2},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":1},
            ],
            2: [
                {"item":{"id":items_ids["iron_ingot"],"type":"items"},"quantity":2},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":1},
            ],
            3: [
                {"item":{"id":items_ids["gold_ingot"],"type":"items"},"quantity":2},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":1},
            ],
            4: [
                {"item":{"id":items_ids["diamond"],"type":"items"},"quantity":2},
                {"item":{"id":items_ids["stick"],"type":"items"},"quantity":1},
            ],
        },
    },

    "items": {
        items_ids["stick"]: {
            "amount":4,
            "recipe":[
                {"item":{"id":block_ids["planks"],"type":"blocks"},"quantity":2},
            ],
        },
        items_ids["coal"]: {
            "amount":9,
            "recipe":[
                {"item":{"id":block_ids["coal_block"],"type":"blocks"},"quantity":1},
            ],
        },
        items_ids["iron_ingot"]: {
            "amount":9,
            "recipe":[
                {"item":{"id":block_ids["iron_block"],"type":"blocks"},"quantity":1},
            ],
        },
        items_ids["gold_ingot"]: {
            "amount":9,
            "recipe":[
                {"item":{"id":block_ids["gold_block"],"type":"blocks"},"quantity":1},
            ],
        },
        items_ids["diamond"]: {
            "amount":9,
            "recipe":[
                {"item":{"id":block_ids["diamond_block"],"type":"blocks"},"quantity":1},
            ],
        },
    },
}