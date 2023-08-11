
def paginate(query, schema, page, per_page):
    result = query.paginate(page=page, per_page=per_page)
   # items = ClienteSchema().dump(result.items, many=True)
    items = schema.dump(result.items, many=True)


    return {
        "items": items,
        "total": result.total,
        "next": result.next_num if result.has_next else None,
        "prev": result.prev_num if result.has_prev else None
    }
