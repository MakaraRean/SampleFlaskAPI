
import math
import json

from app.models.baseModel import AlchemyEncoder


def pagging(query, paging_page_no=1, paging_display_records=50):
    paging_page_no = int(paging_page_no)
    paging_display_records = int(paging_display_records)
    if paging_page_no > 0 and paging_display_records > 0:
        items = query.limit(paging_display_records).offset((paging_page_no - 1) * paging_display_records).all()
    else:
        items = query.all()

    total_records = query.count()
    total_pages = int(math.ceil(total_records / float(paging_display_records)))
    # data_result = [json.loads(json.dumps(item, cls=AlchemyEncoder)) for item in items]

    data_result = []
    row_number_offset = (paging_page_no - 1) * paging_display_records
    for item in items:
        tmp_result = json.loads(json.dumps(item, cls=AlchemyEncoder))
        tmp_result['row_num'] = row_number_offset + 1
        row_number_offset += 1
        data_result.append(tmp_result)
    #
    # for index, item in enumerate(items):
    #     tmp_result = json.loads(json.dumps(item, cls=AlchemyEncoder))
    #     tmp_result['row_num'] = index + 1
    #     data_result.append(tmp_result)

    paging_result = dict(
        page_no=paging_page_no,
        total_pages=total_pages,
        total_records=total_records,
        display_records=paging_display_records
    )
    result = dict(data=data_result, paging=paging_result)
    return result

