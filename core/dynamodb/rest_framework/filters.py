import ast
import logging
from functools import cmp_to_key

from rest_framework_datatables.filters import (
    DatatablesBaseFilterBackend,
    is_valid_regex,
)

logger = logging.getLogger(__name__)


def f_search_q(f, search_value: str, *, search_regex=False):
    """helper function that returns a Q-object for a search value"""
    qs = []

    if search_value and search_value != "false":
        if search_regex:
            if is_valid_regex(search_value):
                qs.extend([f're.match(x.{x}, "{search_value}")' for x in f["name"]])
        else:
            qs.extend(
                [
                    f'str(x.{x}).lower().find("{search_value.lower()}") >= 0'
                    for x in f["name"]
                ]
            )
    if len(qs) > 1:
        return f"({' or '.join(qs)})"
    return " or ".join(qs)


class DynamoDbDatatablesBaseFilterBackend(DatatablesBaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        The filtering itself is done by the DynamoDbFilterBackend
        """
        if not self.check_renderer_format(request):
            return queryset

        total_count = len(queryset)
        self.set_count_before(view, total_count)

        filtered_count_before = total_count

        datatables_query = self.parse_datatables_query(request, view)

        q = self.get_lambda_filter(datatables_query)
        logger.debug("q: %s", q)
        if q:
            queryset = list(filter(q, queryset))
            filtered_count = len(queryset)
        else:
            filtered_count = filtered_count_before
        self.set_count_after(view, filtered_count)

        ordering = self.get_ordering_lambda(request, view, datatables_query["fields"])
        logger.debug("ordering: %s", ordering)
        if ordering:
            queryset = sorted(queryset, key=cmp_to_key(ordering))
        return queryset

    def get_lambda_filter(self, datatables_query):
        """
        Build the filter expression for the DynamoDbFilterBackend
        """
        q = []
        initial_q = []
        for f in datatables_query["fields"]:
            if not f["searchable"]:
                continue
            if datatables_query["search_value"]:
                q.append(
                    f_search_q(
                        f,
                        search_value=datatables_query["search_value"],
                        search_regex=datatables_query["search_regex"],
                    )
                )
            if f.get("search_value"):
                initial_q.append(
                    f_search_q(
                        f,
                        search_value=f.get("search_value"),
                        search_regex=f.get("search_regex", False),
                    )
                )

        logger.debug("q: %s", q)
        logger.debug("initial_q: %s", initial_q)
        lambda_str = ""
        if len(q) > 0 and len(initial_q) > 0:
            lambda_str += (
                f"lambda x: ({' or '.join(q)}) and ({' and '.join(initial_q)})"
            )
        elif len(q) > 0:
            lambda_str += " or ".join(q)
        elif len(initial_q) > 0:
            lambda_str += " and ".join(initial_q)

        return ast.literal_eval(f"lambda x: {lambda_str}") if lambda_str else None

    def get_ordering_lambda(self, request, view, fields):
        order_fields = self.get_ordering_fields(request, view, fields)
        logger.debug("order_fields: %s", order_fields)
        if not order_fields:
            return None

        def compare(dict1, dict2):
            for field, direction in order_fields:
                field1 = dict1.get(field["name"][0], {})
                field2 = dict2.get(field["name"][0], {})
                value1 = field1.get("S", field1.get("N", field1.get("BOOL", "")))
                value2 = field2.get("S", field2.get("N", field2.get("BOOL", "")))
                if direction == "asc":
                    if value1 < value2:
                        return -1
                    if value1 > value2:
                        return 1
                elif value1 < value2:
                    return 1
                elif value1 > value2:
                    return -1
            return 0

        return compare
