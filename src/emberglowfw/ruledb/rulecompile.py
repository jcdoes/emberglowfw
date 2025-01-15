import emberglowfw.db.redisdb as redisdb



def create_rule_request(source, dest, port):
    
    rule_values = {}

    rule_values['name'] = ""
    rule_values['source'] = source
    rule_values['dest'] = dest
    rule_values['port'] = port
    rule_values['reviewed'] = ""
    rule_values['reviewed_by'] = ""
    rule_values['approved'] = False

    redis_conn = redisdb.open_redis_con()

    redis_prefix = "Rule_*"

    # Find the next index number for rule
    cursor = 0
    count = 0

    while True:

        cursor, keys = redis_conn.scan(cursor=cursor, match=redis_prefix)
        count += len(keys)

        if cursor == 0:
            break

    redis_conn.json().set('Rule_' + str(count + 1), "$", rule_values)

