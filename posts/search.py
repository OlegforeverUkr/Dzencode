from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank,
    SearchHeadline,
)

from posts.models import Post


def search_posts(query):
    vector = SearchVector("title", "body")
    query = SearchQuery(query)

    result = (
        Post.objects.annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .order_by("-rank")
    )

    result = result.annotate(
        headline=SearchHeadline(
            "title",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
    result = result.annotate(
        bodyline=SearchHeadline(
            "body",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel="</span>",
        )
    )
    return result